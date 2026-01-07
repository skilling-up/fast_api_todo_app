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

async def init_db():
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute(CREATE_TABLE_USERS)
        await db.commit()
        logger.info("База данных инцилизирована")
