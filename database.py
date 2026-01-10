import aiosqlite
import logging



logging.basicConfig(
    level= logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)

DATABASE_URL = "todo_app.db"

CREATE_TABLE_USERS = """
CREATE TABLE IF NOT  EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL CHECK(age >= 1 AND age < 150),
    email TEXT NOT NULL UNIQUE
);
"""

async def get_db():
    """
    Generator function that yields a database connection.

    This function is designed to be used as a FastAPI dependency with "Depends".
    It opens an asynchronous connection to the database  specified by DATABASE_URL
    using aiosqlite, yieleds the connection object, and then automatically closes
    the connection  after the caller finishes using it (due to 'async with').

    Yields:
        aiosqlite.Connection: The database connection object.
    """
    async with aiosqlite(DATABASE_URL) as db:
        yield db


async def init_db(db: aiosqlite.Connection):
    """
    Initializes the database by creating the 'users' table if it doesn't exist.

    This function executes the CREATE_TABLE_USERS SQL script on the provided
    database connection.

    Args:
        db (aiosqlite.Connection): The database connection object.
    """   
    await db.execute(CREATE_TABLE_USERS)
    await db.commit()
    logger.info("Database initialized")
