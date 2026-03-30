# ChiIT Backend

REST API built with FastAPI, PostgreSQL, and Peewee ORM.

## Requirements

- Python 3.10+
- PostgreSQL
- pip

## Setup

1. Clone the repository:
   git clone https://github.com/hexyatina/chi-it-intership-tech-task
    cd chi-it-intership-tech-task

2. Create and activate virtual environment:
   python -m venv .venv
   .venv\Scripts\activate  # Windows


4. Create `.env` file:
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRATION=20

## Running

1. Create tables:
   python creating_tables.py

2. Load initial data:
   python creating_users.py

3. Start the server:
   uvicorn main:app --reload

API available at: http://127.0.0.1:8000
Swagger docs: http://127.0.0.1:8000/docs

## Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | /health | Health check |
| POST | /auth/login | Login, get JWT token |