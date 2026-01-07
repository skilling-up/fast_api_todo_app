# FastAPI CRUD API

This is a simple CRUD API built with [FastAPI](https://fastapi.tiangolo.com/) and [aiosqlite](https://pypi.org/project/aiosqlite/).

## Features

- Create, Read, Update, Delete (CRUD) operations for users.
- Async database operations using `aiosqlite`.
- Input validation using [Pydantic](https://docs.pydantic.dev/).
- Structured project layout (`database.py`, `crud.py`, `models.py`, `main.py`).

## Technologies Used

- Python
- FastAPI
- aiosqlite
- Pydantic

## Setup

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `uvicorn main:app --reload`

## API Endpoints

- `GET /` - Welcome message.
- `POST /users/create_user` - Create a new user.
- `GET /users` - Get all users.
- `DELETE /users/delete_user/{user_id}` - Delete a user by ID.
- `PUT /users/user_update/{user_id}` - Update a user by ID.
