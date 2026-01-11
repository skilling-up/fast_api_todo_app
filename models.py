from pydantic import BaseModel, Field, EmailStr
from typing import Optional
class User_create(BaseModel):
    """
    Pydantic model for creating a new user.

    Defines the schema and validation rules for user data received during creation.
    """
    name:str
    age:int = Field(ge=1,lt=150)
    email:EmailStr
class User_update(BaseModel):
    """
    Pydantic model for updating an existing user.

    Defines the optional fields that can be modified during an update operation.
    All fields are optional, allowing partial updates.
    """
    new_name:Optional[str] = None
    new_age:Optional[int] = None
    new_email:Optional[EmailStr] = None
