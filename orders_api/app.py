from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from confluent_kafka import Producer, Consumer, KafkaError
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakError
from functools import wraps
from flask_cors import CORS
from os import environ
import requests
import logging
import asyncio
import httpx
import time
import threading
import socket
import json


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

producer_conf = {
        'bootstrap.servers': environ.get('KAFKA_URL'),
        'client.id': 'orders_api'
        }
producer = Producer(producer_conf)

consumer_conf = {
        'bootstrap.servers': environ.get('KAFKA_URL'),
        'group.id': 'orders-group',
        'auto.offset.reset': 'earliest'
        }

consumer = Consumer(consumer_conf)

keycloak_openid = KeycloakOpenID(
    server_url= environ.get('KEYCLOAK_URL'),
    client_id="",
    realm_name= environ.get('KEYCLOAK_REALM'),
    client_secret_key=""
)

def keycloak_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return make_response(jsonify({'message': 'Missing Authorization Header'}), 401)

        token = auth_header.split(" ")[1]
        try:
            userinfo = keycloak_openid.userinfo(token)
            request.username = userinfo['preferred_username']
            roles = userinfo.get('realm_access', {}).get('roles', [])
            if 'customer' not in roles:
                return make_response(jsonify({'message': 'User does not have the required role'}), 403)
        except KeycloakError as e:
            return make_response(jsonify({'message': 'Invalid token', 'error': str(e)}), 401)

        return f(*args, **kwargs)
    return decorated_function

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    items = db.relationship('OrderItem', backref='order', cascade="all, delete-orphan", lazy=True)
    username = db.Column(db.String(80), nullable=False)
    def json(self):
        return {
            'id': self.id,
            'products': [item.json() for item in self.items],
            'total_price': self.total_price,
            'status': self.status
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)

    def json(self):
        return {
            'title': self.title,
            'amount': self.amount,
            'product_id': self.product_id
        }


db.create_all()

def consume_messages():
    consumer.subscribe([ environ.get('KAFKA_ORDERS_TOPIC')])
    logger.info(f"Subscribed to topic '{environ.get('KAFKA_ORDERS_TOPIC')}'")

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                logger.error(f"Consumer error: {msg.error()}")
                break

        try:
            message = json.loads(msg.value().decode('utf-8'))
            logger.info(f"Received message: {message}")
            order_id = message['Id']
            status = message['Status']
            order_status = "rejected"
            if bool(status):
                order_status = "approved"
            with app.app_context():
                order = db.session.query(Order).get(int(order_id))
                if order:
                    order.status = order_status
                    db.session.commit()

        except Exception as e:
            print(f"Failed to process message: {e}")

    consumer.close()
    logger.info(f"Consumer closed")

consumer_thread = threading.Thread(target=consume_messages)
consumer_thread.start()

@app.route('/api/orders', methods=['POST'])
@keycloak_required
def create_order():
    try:
        data = request.get_json()
        products = data.get('products')
        total_price = data.get('total_price')
        status = 'pending'

        if not products or not isinstance(products, list) or not all(isinstance(p, dict) for p in products):
            return make_response(jsonify({'message': 'Invalid data: "products" must be a list of product dictionaries'}), 400)
        if not isinstance(total_price, (int, float)) or total_price <= 0:
            return make_response(jsonify({'message': 'Invalid data: "total_price" must be a positive number'}), 400)

        new_order = Order(total_price=total_price, status=status, username=request.username)
        db.session.add(new_order)
        db.session.flush()
        for product in products:
            order_item = OrderItem(
                order_id=new_order.id,
                title=product['title'],
                amount=product['amount'],
                product_id=product['product_id']
            )
            db.session.add(order_item)
        db.session.commit()
        thread = threading.Thread(target=update_product_quantities,args=(new_order.id, products))       
        thread.start()
        return jsonify(new_order.json()), 201
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'message': 'Error creating order', 'error': str(e)}), 500)


@app.route('/api/orders', methods=['GET'])
@keycloak_required
def get_orders():
    try:
        username = request.username
        orders = Order.query.filter_by(username=username).all()
        return jsonify([order.json() for order in orders]), 200
    except Exception as e:
        return make_response(jsonify({'message': 'Error fetching orders', 'error': str(e)}), 500)


@app.route('/api/orders/<int:order_id>', methods=['GET'])
@keycloak_required
def get_order(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return make_response(jsonify({'message': 'Order not found'}), 404)
        return jsonify(order.json()), 200
    except Exception as e:
        return make_response(jsonify({'message': 'Error fetching order', 'error': str(e)}), 500)

def update_product_quantities(order_id, products):   
    product_updates = [
        {'product_id': product['product_id'], 'quantity': -product['amount']}
        for product in products
    ]

    message = {
        'Id': order_id,
        'Products': product_updates
    }
    producer.produce(environ.get('KAFA_PRODUCTS_TOPIC'), key=str(order_id), value=json.dumps(message))



if __name__ == '__main__':
    app.run(debug=True)
