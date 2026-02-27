# FastAPI CRUD API

This is a simple CRUD API built with [FastAPI](https://fastapi.tiangolo.com/), [SQLAlchemy 2.0](https://www.sqlalchemy.org/), and [PostgreSQL](https://www.postgresql.org/).

## Features

- Create, Read, Update, Delete (CRUD) operations for users.
- Asynchronous database operations using SQLAlchemy 2.0 with PostgreSQL.
- Input validation using [Pydantic](https://docs.pydantic.dev/).
- Structured project layout (`database.py`, `models.py`, `schemas.py`, `crud.py`, `main.py`).
- Comprehensive documentation using docstrings.
- Asynchronous tests using `pytest-asyncio`.

## Technologies Used

- Python 3.10+
- FastAPI
- SQLAlchemy 2.0 (asynchronous)
- Pydantic v2
- PostgreSQL (asyncpg driver)
- pytest / pytest-asyncio
- GitHub Actions (CI)

## Setup

1.  Clone the repository.
2.  (Optional but recommended) Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Set up environment variables:
    Create a `.env` file in the project root with the following content:
    ```env
    DATABASE_URL=postgresql+asyncpg://user:password@localhost/main_db
    TEST_DATABASE_URL=postgresql+asyncpg://user:password@localhost/test_db
    ```
    Replace `user`, `password`, `localhost`, and database names with your actual PostgreSQL credentials.
5.  Run the server:
    ```bash
    uvicorn main:app --reload
    ```

## API Endpoints

- `GET /` - Welcome message.
- `POST /users/create_user` - Create a new user.
- `GET /users/get_users` - Get all users.
- `DELETE /users/delete_user/{user_id}` - Delete a user by ID.
- `PATCH /users/user_update/{user_id}` - Partially update a user by ID.

## Running Tests

Run the tests using pytest:
```bash
pytest
