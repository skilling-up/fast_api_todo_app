from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
class UserBase(BaseModel):
    """
    Base Pydantic model for user data.

    Contains common fields shared by create, update, read operations.
    All fields are required and validated.
    """
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., ge=1, le=120)
    email: EmailStr


class UserCreate(UserBase):
    """
    Pydantic model for creating a new user.

    Inherits all fields from UserBase.
    No additional fields are needed for creation.

    """
    pass

class UserUpdate(BaseModel):
    """
    Pydantic model for updating an existing user.

    All fields are optional. Only provided fields will updated.
    Each fields retains its validation rules when present.

    Attributes:
        name (Optional[str]): New name (if provided). Must be 2-50 chars.
        age (Optional[int]): New age (if provided). Must be 1-120.
        email (Optional[EmailStr): New email (if provided). Must be valid format.
    """
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    age: Optional[int] = Field(None, ge=1, le=120)
    email: Optional[EmailStr] = None

class UserRead(UserBase):
    """
    Pydantic model for reading user data (response model).

    Inherits all fields from UserBase  and adds the 'id' fields.
    Used to serialize database User objects to JSON responses.

    Attributes:
        id (int): Unique identifier  of the user.
    """
    id:int
    model_config = ConfigDict(from_attributes=True)
    