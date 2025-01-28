# Eshop

![My Eshop](./spa/src/assets/My_Eshop.png) 

Eshop is an example project showcasing modern e-commerce architecture using a variety of integrated technologies. It demonstrates interactions between customers and sellers in a containerized environment.


![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue%20js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08)
![Kafka](https://img.shields.io/badge/Apache_Kafka-231F20?style=for-the-badge&logo=apache-kafka&logoColor=white)
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)

## Features

- **Frontend:** Vue.js SPA
- **Backend:** Two Python APIs (Products API and Orders API)
- **Databases:** Two PostgreSQL databases (for Products and Orders APIs) and one MySQL database for Keycloak
- **Local Storage:** Cart data is stored in the browser's local storage
- **Authentication:** Keycloak
- **Messaging System:** Apache Kafka (with Zookeeper and Kafka Control Center)
- **Containerization:** Docker Compose

---

## System Architecture

The architecture includes:

- **Frontend**: Vue.js SPA interacting with Keycloak and two APIs.
- **Products API**: Connected to PostgreSQL and Apache Kafka.
- **Orders API**: Connected to PostgreSQL and Apache Kafka.
- **Inter-API Communication:** Kafka is used for two-way communication between the Products API and Orders API
- **Keycloak**: Used for authentication and permttions, with a MySQL database.


---

## Requirements

- Docker Compose

---

## Installation

Clone the repository:
```bash
git clone <repository-url>  
cd eshop
```

Create a `.env` file based on the provided `.env.example` file and configure environment variables if needed.

 Start the services:
```bash
docker compose up
```

---

## Usage

- Access the SPA (frontend) at: `http://localhost:5173`
- Access Keycloak at: `http://localhost:8080`
- Access Kafka Control Center at:`http://localhost:9021`

---



## Services Overview

### Frontend (SPA)
- Built with Vue.js.
- Communicates with APIs and Keycloak.

### Products API
- Handles product-related operations.
- Publishes events to Apache Kafka.
- Connected to a PostgreSQL database.

### Orders API
- Manages orders.
- Publishes events to Apache Kafka.
- Connected to a PostgreSQL database.

### Keycloak
- Provides authentication and user management.
- Uses a MySQL database.

### Apache Kafka
- Manages messaging between services.
- Includes Zookeeper and Kafka Control Center.

---

## Contribution

    This project does not accept contributions.

---

## License

    This project is not licensed.