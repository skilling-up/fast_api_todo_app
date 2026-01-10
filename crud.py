import aiosqlite
from database import logger
async def add_user(name:str, age:int, email:str, db: aiosqlite.Connection):
        """
        Adds a new user to the database.

        Args:
            name (str): The name of the user.
            age (int): The age of the user (must be between 1 and 149).
            email (str): The email address of the user(must be unique).
            db (aiosqlite.Connection): The database connection object.
        
        Returns:
            int | None: The ID of the newly inserted user if successful, otherwise None
                    if a user with the same email already exists.
        """
    
        try:
            insert_query = "INSERT INTO users (name,age,email) VALUES (?,?,?)"  
            cursor = await db.execute(insert_query, (name,age,email))
            await db.commit()
            return cursor.lastrowid
        except aiosqlite.IntegrityError:
            logger.info(f"Error, user with email:{email} alredy exists")
            return None
async def get_all_users(db):
        """
        Retrieves all users from the database.

        Args:
            db (aiosqlite.Connection): The database connection object.
        
        Returns:
            list[tuple]: A list of tuples representing users.
                          Each tuple  contains(id, name, age, email).
        """
    
        
        select_query = "SELECT id, name, age, email FROM users"

       
        async with db.execute(select_query) as cursor:
           
            rows = await cursor.fetchall()
            return rows



async def  update_user(user_id:int,db, new_name:str = None, new_age: int =None,new_email:str = None):
    """
    Updates specific fields of a user in the database.

    Only the fields provided (Not None) will be updated.

    Args:
    user_id (int): The ID of user to update.
    db (aiosqlite.Connection): The database connection object.
    new_name (str | None):  The new name for the user. Defaults to None.
    new_age (int | None): The new age for the user. Defaults to None.
    new_email (str | None): The new email of the user. Defaults to None.


    Returns:
        bool: True if the user was updated, False if no were provided or user was not found.
    """
    update_data = {}
    if new_name is not None:
        update_data["name"] = new_name
    if new_age is not None:
        update_data["age"] = new_age
    if new_email is not None:
        update_data["email"] = new_email
         
    if not update_data:
        logger.info(f"no data to update user with ID: {user_id}.")
        return False
    

       
    
    set_clause = ", ".join([f"{field} = ?" for field in update_data.keys()])

    
    sql_query = f"UPDATE users SET {set_clause} WHERE id = ?"

    
    values = list(update_data.values()) + [user_id]

    
    await db.execute(sql_query, values)
    await db.commit()
    logger.info(f"User with ID {user_id} has been updated. Variables have been updated.: {list(update_data.keys())}")
    return True
       



async def delete_user(user_id:int,db):
        """
        Deletes a user from the database by their  ID.

        Args:
            user_id (int): The user to delete.
            db (aiosqlite.Connection): The database connection object.

        Returns:
            bool: True if the was deleted (1 row affected), False otherwise (0 rows affected.)

        """
        
        delete_query = "DELETE FROM users WHERE id = ?"
        cursor = await db.execute(delete_query, (user_id,))
        await db.commit()
        rows_affected = cursor.rowcount
        if rows_affected > 0:
             logger.info(f"User with Id {user_id} deleted")
             return True
        else:
             logger.info(f"User with Id {user_id} don't found")
             return False
