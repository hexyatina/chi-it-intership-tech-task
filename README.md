# ChiIT Backend

REST API built with FastAPI, PostgreSQL, and Peewee ORM

## Requirements

- Python 3.10+
- PostgreSQL
- pip

---

## Setup (Local)

1. Clone the repository:
   git clone https://github.com/hexyatina/chi-it-intership-tech-task
   cd chi-it-intership-tech-task

2. Create and activate virtual environment:
   python -m venv .venv
   .venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Create `.env` file:
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256

5. Load initial data:
   python creating_users.py

6. Start the server:
   uvicorn main:app --reload

API available at: http://127.0.0.1:8000
Swagger docs: http://127.0.0.1:8000/docs

---

## Setup (Docker)

1. Create `.env` file (same as above but with DB_HOST=db)

2. Build and run:
   docker-compose up --build

API available at: http://localhost:8000
Swagger docs: http://localhost:8000/docs

---

## Initial Data

Default users created by `creating_users.py`:

ortem - role: admin(password - admin_pass)
editor - role:editor(password - editor_pass)
user - role: user(password - user_pass)

---

## Endpoints

### Auth
| Method | URL          | Description          | Auth |
|--------|--------------|----------------------|------|
| POST   | /auth/login  | Login, get JWT token | No   |

### Health
| Method | URL     | Description  | Auth |
|--------|---------|--------------|------|
| GET    | /health | Health check | No   |

### Articles
| Method | URL                  | Description           | Auth |
|--------|----------------------|-----------------------|------|
| GET    | /articles            | List articles         | Yes  |
| GET    | /articles/{id}       | Get article by ID     | Yes  |
| POST   | /articles            | Create article        | Yes  |
| PUT    | /articles/{id}       | Update article        | Yes  |
| DELETE | /articles/{id}       | Delete article        | Yes  |

### Users
| Method | URL             | Description      | Auth  |
|--------|-----------------|------------------|-------|
| GET    | /users          | List users       | Yes   |
| GET    | /users/{id}     | Get user by ID   | Yes   |
| PUT    | /users/{id}     | Update user      | Admin |
| DELETE | /users/{id}     | Delete user      | Admin |

## Tests

Install test dependencies:
   pip install pytest pytest-cov httpx

Run tests:
   pytest test_main.py -v

Run with coverage:
   pytest test_main.py --cov=. --cov-report=term-missing