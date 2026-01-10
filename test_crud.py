import pytest
import aiosqlite
import pytest_asyncio
import os
from crud import add_user, update_user,delete_user,get_all_users
from database import init_db
TEST_DB_PATH = "test_todo_app.db"

@pytest_asyncio.fixture
async def test_db():
    """
    Fixture that provides a clean temporary database for each test.

    This fixture creates a new temporary SQLite database file before the test runs,
    initializes its schema, yields the database connection to the test,
    and then closes the connection and removes the file after the test completes.
    """
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    


    db = await aiosqlite.connect(TEST_DB_PATH)
    await init_db(db)

    yield db
    await db.close()
    if  os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

@pytest.mark.asyncio
async def test_add_user(test_db):
    """
    Test that the add_user function adds a user to the database correctly.

    Verifies that add_user returns a valid user ID and that the user appears
    in the list returned by get_all_users.
    """
    db = test_db 

    user_id = await add_user("Alice",30,"alice@gmail.com",db)
    assert user_id is not None , "add_user should return  a user ID"
    all_users =  await get_all_users(db)

    assert len(all_users) == 1, f"Expected 1 user,got {len(all_users)}"


    added_user = all_users[0]
    assert added_user[1] == "Alice", f"Expected name 'Alice', got '{added_user[1]}'"
    assert added_user[2] == 30, f"Expected age 30, got {added_user[2]}"
    assert added_user[3] == "alice@gmail.com", f"Expected email 'alice@gmail.com', got '{added_user[3]}'"
@pytest.mark.asyncio
async def test_get_all_users(test_db):
    """
    Test that the get_all_users function retrieves all users from the database.

    Adds multiple users to the database and verifies that get_all_users returns
    a list containing all of them.
    """
    db = test_db
    user_id_1 = await add_user("user1",25,"user1@test.com", db)
    user_id_2 = await add_user("user2",22,"user2@test.com", db)
    user_id_3 = await add_user("user3",24,"user3@test.com", db)

    assert user_id_1 is not None , "First user should be added"
    assert user_id_2 is not None , "Second user should be added"
    assert user_id_3 is not None, "Third user should be added"

    all_user = await get_all_users(db)

    assert len(all_user) == 3 , f"Expected 3 users, got {len(all_user)}"

    names_in_db = {user[1] for user in all_user}
    expected_names = {'user1', 'user2','user3'}

    emails_in_db = {user[3] for user in all_user}
    expected_emails = {"user1@test.com","user2@test.com","user3@test.com"}
    ages_in_db = {user[2] for user in all_user}
    expected_ages = {25,22,24}

    assert names_in_db == expected_names, f"Names mismatch, Expected {expected_names}, got {names_in_db}"
    assert emails_in_db == expected_emails, f"Emails mismatch, Expected {expected_emails}, got {emails_in_db}"
    assert ages_in_db == expected_ages , f" Ages mismatch, Expected {expected_ages}, got {ages_in_db}"

@pytest.mark.asyncio
async def test_update_user(test_db):
    """
    Test that the update_user function updates specific fields of a user.

    Adds a user, updates its age and email, and then verifies that the changes
    are reflected in the database when retrieving the user again.
    """
    db = test_db
    user_id = await add_user("name_user",17, "uw@gmil.com", db)

    assert user_id is not None, "User should be added successfully for update test"

    await update_user(user_id,db,None,18,"user1_update@gmail.com")
    all_users = await get_all_users(db)

    updated_user = None
    for user in all_users:
        if user[0] == user_id:
            updated_user = user 
            break
    assert updated_user is not None, f"User with ID {user_id} not found after update"
    


    assert updated_user[1] == "name_user", f"Expected name 'name_user', got '{updated_user[1]}'" 
    assert updated_user[2] == 18, f"Expected age 18, got {updated_user[2]}" 
    assert updated_user[3] == "user1_update@gmail.com", f"Expected email 'user1_update@gmail.com', got '{updated_user[3]}'" 

    assert len(all_users) == 1, f"Expected 1 user after update , got {len(all_users)}"

@pytest.mark.asyncio
async def test_delete_user(test_db):
    """
    Test that the delete_user function removes a user from the database.

    Adds a user, deletes it, and them verifies that get_all_users returns
    an empty list.
    """
    db = test_db

    user_id = await add_user("user1", 24, "test@gmail.com", db)

    assert user_id is not None, "User should be added successfully for delete test"


    await  delete_user(user_id, db)
    all_users = await get_all_users(db)
    assert  len(all_users) == 0, f"the user was not deleted from the database"
