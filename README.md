# FastAPI CRUD API

This is a simple CRUD API built with [FastAPI](https://fastapi.tiangolo.com/) and [aiosqlite](https://pypi.org/project/aiosqlite/).

## Features

- Create, Read, Update, Delete (CRUD) operations for users.
- Async database operations using `aiosqlite`.
- Input validation using [Pydantic](https://docs.pydantic.dev/).
- Structured project layout (`database.py`, `crud.py`, `models.py`, `main.py`).
- Comprehensive documentation using docstrings.
- Asynchronous tests using `pytest-asyncio`.

## Technologies Used

- Python
- FastAPI
- aiosqlite
- Pydantic
- pytest
- pytest-asyncio

## Setup

1.  Clone the repository.
2.  (Optional but recommended) Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies: `pip install -r requirements.txt`
4.  Run the server: `uvicorn main:app --reload`

## API Endpoints

- `GET /` - Welcome message.
- `POST /users/create_user` - Create a new user.
- `GET /users/get_users` - Get all users.
- `DELETE /users/delete_user/{user_id}` - Delete a user by ID.
- `PUT /users/user_update/{user_id}` - Update a user by ID.

## Running Tests

Run the tests using pytest: `pytest`

To run tests with more verbose output: `pytest -v`
