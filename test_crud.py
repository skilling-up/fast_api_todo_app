"""
Test suite for user CRUD operations.

This module contains asynchronous tests for user creation, reading, updating,
and deletion. It uses the database specified by TEST_DATABASE_URL in settings.
Tests are isolated: each test runs in its own transaction that is rolled back.
"""

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import pytest_asyncio
from config import settings
from crud import add_user, update_user, delete_user, get_all_users
from models import Base

# Use test database URL from settings (should point to a separate test DB)
TEST_DB_URL = settings.test_database_url

# Create an async engine for tests (pooling is handled by SQLAlchemy default)
engine_test = create_async_engine(TEST_DB_URL)

# Create a session factory for tests
TestingSessionLocal = async_sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    """
    Fixture to set up and tear down the database schema before and after each test.

    This fixture runs automatically. It creates all tables before the test
    and drops them after the test, ensuring a clean state for every test case.
    """
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine_test.dispose()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def db_session():
    """
    Fixture that provides a database session for each test function.

    Yields an AsyncSession object. After the test, the session is rolled back
    and closed to prevent any side effects between tests.
    """
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


@pytest.mark.asyncio
async def test_add_user(db_session):
    user_id = await add_user(db_session, "Artem", 16, "artem@gmail.com")
    assert user_id is not None
    all_users = await get_all_users(db_session)
    assert len(all_users) == 1
    added_user = all_users[0]
    assert added_user.name == "Artem"
    assert added_user.age == 16
    assert added_user.email == "artem@gmail.com"


@pytest.mark.asyncio
async def test_update_user(db_session):
    user_id = await add_user(db_session,"name_user", 0, "uw@gmail.com")
    await update_user(db_session,user_id, age = 16, email ="user@gmail.com")
    all_users = await get_all_users(db_session)
    updated_user = next((u for u in all_users if u.id == user_id), None)
    assert updated_user is not None
    assert updated_user.age == 16
    assert updated_user.email =="user@gmail.com"

@pytest.mark.asyncio
async def test_get_all_user(db_session):
    await add_user(db_session,"user1",25,"user1@test.com")
    await add_user(db_session,"user2",23,"user2@test.com")
    await add_user(db_session,"user3",24,"user3@test.com")
    all_users = await get_all_users(db_session)
    assert len(all_users) ==3

    names_in_db = {user.name for user in all_users}
    expected_names = {"user1", "user2", "user3"}

    emails_in_db = {user.email for user in all_users}
    expected_emails ={'user1@test.com','user2@test.com','user3@test.com'}

    assert names_in_db == expected_names
    assert emails_in_db == expected_emails

@pytest.mark.asyncio 
async def test_delete_user(db_session):

    user_id = await add_user(db_session, "user1", 24,"test@gmail.com")
    assert user_id is not None

    deleted = await delete_user(db_session, user_id)
    assert deleted is True

    all_users = await get_all_users(db_session)
    assert len(all_users) == 0
