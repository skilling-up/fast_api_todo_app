from fastapi import FastAPI,HTTPException
from database import init_db
from models import  User_create
from crud import add_user,get_all_users,delete_user,update_user
from contextlib import asynccontextmanager
from database import logger


@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    yield
    logger.info("Сервер отключен")



app = FastAPI(title="my first API!",lifespan=lifespan)



@app.get("/")
async def hello():
    return {"message": "Welcome to my first API"}




@app.get("/users/get_users")
async def get_users():
    return  await get_all_users()


@app.post("/users/creat_user")
async def creat_user(user:User_create):
    user_id = await add_user(user.name,user.age,user.email)
    if user_id is None:
        raise HTTPException(status_code=400,detail="User with this email already exists")
    return {"message": "User created successfully", "user_id": user_id}

@app.delete("/users/delete_user/{user_id}")
async def user_delete(user_id:int):
    return  await delete_user(user_id)

@app.put("/users/user_update/{user_id}")
async def user_update(user_id:int, new_name:str = None,new_age:int = None,new_email:str= None):
    return  await update_user(user_id,new_name,new_age,new_email)
