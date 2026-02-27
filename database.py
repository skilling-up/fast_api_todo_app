from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column
from config import settings
import logging
import os



logging.basicConfig(
    level= logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)



class Base(DeclarativeBase):
    pass



engine = create_async_engine(settings.database_url, echo = True)
async_session =  async_sessionmaker(engine, expire_on_commit= False, class_ = AsyncSession)

async def get_db():
   async with async_session() as session:
        try:
            yield session
            
        except Exception:
            await session.rollback()
            raise 
        finally:
            await session.close()

async def init_db( ):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database initialized with SQLAlchemy")
