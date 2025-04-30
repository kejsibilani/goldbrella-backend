# GoldBrella

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)  
[![Django Version](https://img.shields.io/badge/django-4.1-green)](https://www.djangoproject.com/)  
[![DRF Version](https://img.shields.io/badge/djangorestframework-3.14-orange)](https://www.django-rest-framework.org/)  
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

> **GoldBrella** – A comprehensive beach management system to streamline bookings, asset tracking, and on-site operations.

---

## Table of Contents

- [About the Project](#about-the-project)  
- [Key Features](#key-features)  
- [Tech Stack](#tech-stack)  
- [Prerequisites](#prerequisites)  
- [Getting Started](#getting-started)  
  - [Clone the Repo](#clone-the-repo)  
  - [Setup Virtual Environment](#setup-virtual-environment)  
  - [Install Dependencies](#install-dependencies)  
  - [Environment Variables](#environment-variables)  
  - [Database Setup & Migrations](#database-setup--migrations)  
  - [Run the Development Server](#run-the-development-server)  
- [API Documentation](#api-documentation)  
- [Authentication](#authentication)  
- [Running Tests](#running-tests)  
- [Deployment](#deployment)  
- [Contributing](#contributing)  
- [License](#license)  
- [Acknowledgements](#acknowledgements)  

---

## About the Project

GoldBrella is designed for beach resort operators, property managers, and lifeguard teams to:

- Manage umbrella and lounger inventory  
- Handle guest bookings and payments  
- Track real-time occupancy and availability  
- Generate reports on usage, revenue, and maintenance  

Whether you’re running a small private beach or a large resort, GoldBrella helps you stay organized and deliver a seamless guest experience.

---

## Key Features

- **RESTful API** built with Django REST Framework  
- **JWT-based authentication** via Simple JWT  
- **Interactive API docs** with Swagger/OpenAPI  
- **PostgreSQL** for reliable, scalable data storage  
- Modular apps for **Bookings**, **Inventory**, **Users**, and **Analytics**  
- Role-based access control: Admins, Staff, Lifeguards, Customers  

---

## Tech Stack

- **Backend:** Django, Django REST Framework  
- **Auth:** Simple JWT (`djangorestframework-simplejwt`)  
- **Database:** PostgreSQL  
- **API Docs:** drf-yasg (Swagger/OpenAPI)  
- **Testing:** pytest & Django’s test framework  
- **Environment management:** python-decouple or django-environ  

---

## Prerequisites

- Python 3.8 or higher  
- PostgreSQL 12 or higher  
- (Optional) `virtualenv` or `venv` for isolated environments  

---

## Getting Started

### Clone the Repo

```bash
git clone https://github.com/your-org/GoldBrella.git
cd GoldBrella
```

### Setup Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file in the project root (or set your environment) with the following:

```dotenv
# .env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=goldbrella
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432

# JWT
SIMPLE_JWT_ACCESS_TOKEN_LIFETIME=5m
SIMPLE_JWT_REFRESH_TOKEN_LIFETIME=1d
```
> Tip: Never commit your .env to version control.

### Database Setup & Migrations
```bash
# Create the database (adjust to your psql setup):
createdb goldbrella

# Run migrations:
python manage.py migrate
```

### Run the Development Server
```bash
python manage.py runserver
```
Your API will now be accessible at http://127.0.0.1:8000/

## API Documentation
Interactive Swagger docs are available once the server is running:

```bash
http://127.0.0.1:8000/docs/     # Swagger UI
```

## Authentication
GoldBrella uses JSON Web Tokens (JWT).

**1. Obtain tokens**

```bash
POST /api/login/
{
  "username": "user",
  "password": "pass"
}
```
Response:

```json
{
  "access": "<access_token>",
  "refresh": "<refresh_token>"
}
```
**2. Use the access token in the `Authorization` header for protected endpoints:**

```makefile
Authorization: Bearer <access_token>
```

## Running Tests
```bash
# If using pytest:
pytest

# Or Django’s test runner:
python manage.py test
```

## Deployment
A common production setup might include:

- Gunicorn behind Nginx

- Environment variables stored securely (e.g., Docker secrets, AWS Parameter Store)

- HTTPS termination via Let’s Encrypt or your provider

- CI/CD pipeline to run tests & lint before deploy

(Feel free to add your Docker Compose or Kubernetes manifests here.)

## Contributing
Fork the repository

1. Create a feature branch (git checkout -b feature/YourFeature)

2. Commit your changes with clear messages

3. Push to your fork (git push origin feature/YourFeature)

4. Open a Pull Request and describe your changes

Please follow [PEP8]() style and include tests for new features.

## License
This project is licensed under the MIT License. See the [LICENSE]() file for details.

## Acknowledgements
- [Django]()

- [Django REST Framework]()

- [Simple JWT]()

- [drf-yasg (Swagger/OpenAPI)]()

- Icons by [Font Awesome]()
