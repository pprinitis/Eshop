from flask import Flask, request, jsonify, make_response, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  
from os import environ
from io import BytesIO
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakError
from confluent_kafka import Producer, Consumer, KafkaError
from functools import wraps
import uuid
import os
import threading
import json
import socket
import logging
import requests


consumer_conf = {
        'bootstrap.servers': environ.get('KAFKA_URL'),
        'group.id': 'products-group',
        'auto.offset.reset': 'earliest'
        }

consumer = Consumer(consumer_conf)

producer_conf = {
        'bootstrap.servers': environ.get('KAFKA_URL'),
        'client.id': 'products_api'
        }
producer = Producer(producer_conf)

keycloak_openid = KeycloakOpenID(
    server_url= environ.get('KEYCLOAK_URL'),
    client_id="",
    realm_name= environ.get('KEYCLOAK_REALM'),
    client_secret_key=""
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = environ.get('UPLOAD_FOLDER')
ALLOWED_EXTENSIONS = environ.get('ALLOWED_EXTENSIONS')
app = Flask(__name__)
CORS(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

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
            if 'seller' not in roles:
                return make_response(jsonify({'message': 'User does not have the required role'}), 403)
        except KeycloakError as e:
            logger.error(f"Keycloak error: {e}")
            return make_response(jsonify({'message': 'Invalid token', 'error': str(e)}), 401)

        return f(*args, **kwargs)
    return decorated_function

class Product(db.Model):
    __tablename__ = 'products'  
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    img = db.Column(db.String(80), nullable=False) 
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(80), nullable=False)


    def json(self):
        img_url = f"{request.host_url}uploads/{self.img}"

        return {
            'id': self.id,
            'title': self.title,
            'img': img_url,
            'price': self.price,
            'quantity': self.quantity
        }

db.create_all()

def consume_messages():
    consumer.subscribe([environ.get('KAFA_PRODUCTS_TOPIC')])
    logger.info(f"Subscribed to topic '{environ.get('KAFA_PRODUCTS_TOPIC')}'")

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
            product_updates = message['Products']
            logger.info(f"Processing order... {product_updates}")
            if not order_id or not isinstance(product_updates, list):
                    logger.warning(f"Malformed message: {message}")
                    continue
            upsert_outcome = True
            for product_update in product_updates:
                logger.info(f"Processing product... {product_updates}")

                product_id = product_update.get('product_id')
                quantity_change = product_update.get('quantity')

                if not isinstance(product_id, int) or not isinstance(quantity_change, int):
                    upsert_outcome = False
                    break

                product = Product.query.filter_by(id=product_id).first()
                if not product:
                    upsert_outcome = False
                    break
                if product.quantity + quantity_change < 0:
                    upsert_outcome = False
                    break
                product.quantity += quantity_change
            db.session.commit()
            order_msg = {
                'Id': order_id,
                'Status': upsert_outcome
            }
            producer.produce(environ.get('KAFKA_ORDERS_TOPIC'), value=json.dumps(order_msg))
            producer.flush()
        except Exception as e:
            print(f"Failed to process message: {e}")
     

    consumer.close()
    logger.info(f"Consumer closed")

consumer_thread = threading.Thread(target=consume_messages)
consumer_thread.start()

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
@app.route('/api/products', methods=['POST'])
@keycloak_required
def create_product():
    if 'img' not in request.files:
        return make_response(jsonify({'message': 'No image file provided'}), 400)

    file = request.files['img']
    if file.filename == '':
        return make_response(jsonify({'message': 'No selected file'}), 400)

    if file and allowed_file(file.filename):
        filename = generate_unique_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        try:
            data = request.form
            title = data['title']
            price = float(data['price'])
            quantity = int(data['quantity'])
            username = request.username
            new_product = Product(
                title=title,
                img=filename,  
                price=price,
                quantity=quantity,
                username=username
            )
            db.session.add(new_product)
            db.session.commit()

            return jsonify(new_product.json()), 201
        except Exception as e:
            return make_response(jsonify({'message': 'Error creating product', 'error': str(e)}), 500)
    else:
        return make_response(jsonify({'message': 'File type not allowed'}), 400)

@app.route('/api/myproducts', methods=['GET'])
@keycloak_required
def get_myproducts():
    try:
        username = request.username
        title = request.args.get('title', type=str)
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        sort = request.args.get('sort', type=str)

        query = Product.query.filter_by(username=username)
        if title:
            query = query.filter(Product.title.ilike(f"%{title}%"))

        if min_price is not None:
            query = query.filter(Product.price >= min_price)

        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        if sort and len(sort) >0:
            if sort == "price-asc":
                query = query.order_by(Product.price.asc())
            elif sort == "price-desc":
                query = query.order_by(Product.price.desc())
            elif sort == "title-asc":
                query = query.order_by(Product.title.asc())
            elif sort == "title-desc":
                query = query.order_by(Product.title.desc())
            elif sort == "quantity-asc":
                query = query.order_by(Product.quantity.asc())
            elif sort == "quantity-desc":
                query = query.order_by(Product.quantity.desc())

        products = query.all()
        products_data = [product.json() for product in products]
        return jsonify(products_data), 200
    except Exception as e:
        return make_response(jsonify({'message': 'error getting products', 'error': str(e)}), 500)

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        title = request.args.get('title', type=str)
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        sort = request.args.get('sort', type=str)

        query = Product.query
        if title:
            query = query.filter(Product.title.ilike(f"%{title}%"))

        if min_price is not None:
            query = query.filter(Product.price >= min_price)

        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        if sort and len(sort) >0:
            if sort == "price-asc":
                query = query.order_by(Product.price.asc())
            elif sort == "price-desc":
                query = query.order_by(Product.price.desc())
            elif sort == "title-asc":
                query = query.order_by(Product.title.asc())
            elif sort == "title-desc":
                query = query.order_by(Product.title.desc())
            elif sort == "quantity-asc":
                query = query.order_by(Product.quantity.asc())
            elif sort == "quantity-desc":
                query = query.order_by(Product.quantity.desc())

        products = query.all()
        products_data = [product.json() for product in products]
        return jsonify(products_data), 200
    except Exception as e:
        return make_response(jsonify({'message': 'error getting products', 'error': str(e)}), 500)

@app.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    try:
        product = Product.query.filter_by(id=id).first()
        if product:
            return make_response(jsonify({'product': product.json()}), 200)
        return make_response(jsonify({'message': 'product not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting product', 'error': str(e)}), 500)

@app.route('/api/products/<int:id>', methods=['PUT'])
@keycloak_required
def update_product(id):
    try:
        username = request.username
        product = Product.query.filter_by(id=id, username=username).first()
        if product:
            data = request.get_json()
            product.title = data.get('title', product.title)
            product.img = data.get('img', product.img)
            product.price = data.get('price', product.price)
            product.quantity = data.get('quantity', product.quantity)
            db.session.commit()
            return make_response(jsonify({'message': 'product updated'}), 200)
        return make_response(jsonify({'message': 'product not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error updating product', 'error': str(e)}), 500)

@app.route('/api/products/<int:id>', methods=['PATCH'])
@keycloak_required
def patch_product(id):
    try:
        username = request.username
        product = Product.query.filter_by(id=id, username=username).first()
        if not product:
            return make_response(jsonify({'message': 'Product not found'}), 404)
        data = request.form
        if data['price']:
            try:
                price = float(data['price'])
                if price <= 0:
                    return make_response(jsonify({'message': 'Price must be greater than 0'}), 400)
                product.price = price
            except ValueError:
                return make_response(jsonify({'message': 'Invalid price value'}), 400)

        if data['quantity']:
            try:
                quantity = int(data['quantity'])
                if quantity < 0:
                    return make_response(jsonify({'message': 'Quantity cannot be negative'}), 400)
                product.quantity = quantity
            except ValueError:
                return make_response(jsonify({'message': 'Invalid quantity value'}), 400)

        db.session.commit()

        return make_response(jsonify({
            'message': 'Product updated successfully',
            'product': product.json()
        }), 200)
    except Exception as e:
        db.session.rollback()  # Rollback the transaction in case of an error
        return make_response(jsonify({
            'message': 'Error updating product',
            'error': str(e)
        }), 500)

@app.route('/api/products/<int:id>', methods=['DELETE'])
@keycloak_required
def delete_product(id):
    try:
        username = request.username
        product = Product.query.filter_by(id=id, username=username).first()
        if product:
            db.session.delete(product)
            db.session.commit()
            return make_response(jsonify({'message': 'product deleted'}), 200)
        return make_response(jsonify({'message': 'product not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error deleting product', 'error': str(e)}), 500)

@app.route('/health', methods=['GET'])
def health_check():
    try:
        db.session.execute('SELECT 1')
        return make_response(jsonify({'status': 'healthy'}), 200)
    except Exception as e:
        return make_response(jsonify({'status': 'unhealthy', 'error': str(e)}), 500)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    return unique_filename