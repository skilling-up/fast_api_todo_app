from fastapi import FastAPI,HTTPException,Depends
import aiosqlite
from database import init_db, get_db, DATABASE_URL, logger
from models import  User_create
from crud import add_user,get_all_users,delete_user,update_user
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app:FastAPI):
    """
    Lifespan event handler  for the FastAPI application.

    This function runs once when the application starts up.
    It initializes the database by connecting to it and calling init_db.
    it also logs the initialization event.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    async with aiosqlite.connect(DATABASE_URL) as db:
        await init_db(db)
        logger.info("Database initialized")
    yield
    logger.info("Server shutting down")



app = FastAPI(title="My first API!",lifespan=lifespan)



@app.get("/")
async def hello():
    """
    Root endpoint of the API.

    Returns:
        dict: A welcome message.
    """
    return {"message": "Welcome to my first API"}







@app.get("/users/get_users")
async def get_users(db: aiosqlite.Connection = Depends(get_db)):
    """
    Retrieve all users from the database.

    This endpoint depends on the 'get_db' dependency to provide a database connection.

    Args:
        db (aiosqlite.Connection): Database connection provided by the dependency.
    
    Returns:
        list: A list of users retrieved from the database.
    """
    return  await get_all_users(db)


@app.post("/users/creat_user")
async def creat_user(user:User_create, db: aiosqlite.Connection = Depends(get_db)):
    """
    Create a new user.

    This endpoint accepts user data via the 'user' Pydantic model and a database connection
    It attempts to add the user to the database. If a user with the same email already exists,
    it raises an HTTP 400 error.

    Args:
        user (User_create): The user data to create, validated by Pydantic.
        db (aiosqlite.Connection): Database connection provided by the dependency.
    
    Raises:
        HTTPException: 400 error if a user with the provided email already exists.
    
    Returns:
        dict: A success message and the ID of the created user.
    """
    user_id = await add_user(user.name,user.age,user.email,db)
    if user_id is None:
        raise HTTPException(status_code=400,detail="User with this email already exists")
    return {"message": "User created successfully", "user_id": user_id}

@app.delete("/users/delete_user/{user_id}")
async def user_delete(user_id:int, db: aiosqlite.Connection = Depends(get_db)):
    """
    Delete a user by their ID.

    This endpoint takes a user ID path parameter and a database connection.
    It calls the delete_user function from crud and returns the result.

    Args:
        user_id (int): The ID of the user to delete.
        db (aiosqlite.Connection): Database connection provided by the dependency.
    
    Returns:
        bool: True if the user was deleted, False otherwise.
    """
    return  await delete_user(user_id,db)

@app.put("/users/user_update/{user_id}")
async def user_update(user_id:int, new_name:str = None,new_age:int = None,new_email:str= None,db:aiosqlite.Connection = Depends(get_db)):
    """
    Update specific fields of a user.

    This endpoint takes the user ID as a path parameter and optional new values for name, age, and email.
    It also receives a database connection. It calls the update_user function from crud.

    Args:
        user_id (int): The ID of the user to update.
        new_name (str, optional): The new name for the user. Defaults to None.
        new_age (int, optional): The new age for the user. Defaults to None.
        new_email (str, optional): The new email for the user. Defaults to None.
        db (aiosqlite.Connection): Database connection provided by the dependency.
    
    Returns:
        bool: True if the user was updated, False if no fields were provided for update.
    """
    return  await update_user(user_id,db, new_name,new_age,new_email)
