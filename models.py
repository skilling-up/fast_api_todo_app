from pydantic import BaseModel, Field, EmailStr
from typing import Optional
class User_create(BaseModel):
    name:str
    age:int = Field(ge=1,lt=150)
    email:str = EmailStr
class User_update(BaseModel):
    new_name:Optional[str] = None
    new_age:Optional[int] = None
    new_email:Optional[EmailStr] = None
