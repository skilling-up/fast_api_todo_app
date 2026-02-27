from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from database import logger
from models import User

async def add_user(db: AsyncSession, name:str, age:int,email: str):
    """
    Adds a new user to the database.

    Args:
        db (AsyncSession): SQLAlchemy asynchronous session.
        name (str): User's name.
        age (int): User's age.
        email (str): User's email (must be unique).
    
    Returns:
        int or None: The ID of the newly created user if successful,
        otherwise None (if email already exists).
    
    Raises:
        IntegrityError: if an integrity error occurs (e.g.,duplicate email),
                        it is caught and logged, and None is returned.
    """
    
    new_user = User(name = name, age = age, email = email)
    try:
        db.add(new_user)
        await db.flush()
        await db.refresh(new_user)
        await db.commit()
        

        
        return new_user.id
    except IntegrityError:
        await db.rollback()
        logger.error(f"error, user with email: {email} already exists")
        return None


async def get_all_users(db:AsyncSession):
    """
    Retrieves all users from database.
    
    Args:
        db (AsyncSession): SQLAlchemy asynchronous session.
    
    Returns:
        list[User]: A list of all User objects

    """
    result = await db.execute(select(User))
    
    return result.scalars().all()


async def update_user(db: AsyncSession, user_id: int, **update_data):
    """
    Updates an existing user with the provided fields.

    Only fields that  are not None will be updated.

    Args:
        db (AsyncSession):SQLAlchemy asynchronous session.
        user_id (int): ID of the user to update.
        **update_data: Arbitrary keyword arguments representing fields to update (e.g. name ="new_name", age=30)
    
    Returns:
        bool: True if the user was found and updated, False if no data was provided
              or the user was not found.

    Raises:
        SQLAlchemyError: if a database error occurs  during the update  
    """

    
    filtered_data = {k: v for k, v in update_data.items() if v is not None}

    if not filtered_data:
        logger.info(f"No data to update user with ID: {user_id}")
        return False

    try:
        stmt = update(User).where(User.id == user_id).values(**filtered_data)
        result  = await db.execute(stmt)
        if result.rowcount == 0:
            logger.info(f"User with {user_id} not found .")
            await db.rollback()
            return False
        
        logger.info(f"User with ID {user_id} has been updated:{list(filtered_data.keys())}")
        await db.commit()
        return True
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error updating user {user_id}", exc_info=e)
        raise

async def delete_user(db:AsyncSession, user_id:int):
    """
    Deletes a user by their ID.

    Args:
        db (AsyncSession): SQLAlchemy asynchronous session.
        user_id (int): ID of the user to delete.
    
    Returns:
        bool: True if the user was found and deleted, False otherwise.
    
    Raises:
        SQLAlchemyError: if a database occurs during deletion.
        

    """
    try:
        stmt = delete(User).where(User.id == user_id)
        result = await db.execute(stmt)
    
    
        if result.rowcount == 0:
            await db.rollback()
            return False
        await db.commit()
        return True


        
    except SQLAlchemyError as e:
        logger.error(f"Error deleting user with ID: {user_id}, type error {e}")
        await db.rollback()
        raise
    
