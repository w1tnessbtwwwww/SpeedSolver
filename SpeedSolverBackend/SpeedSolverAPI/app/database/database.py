from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine, 
    AsyncEngine
)

from sqlalchemy.orm import sessionmaker


from app.cfg.settings import settings
from app.utils.logger.telegram_bot.telegram_logger import logger
from app.database.models.models import Base

async def get_engine() -> AsyncEngine:
    return create_async_engine(str(settings.db_url))

def get_engine_sync() -> AsyncEngine:
    return create_async_engine(str(settings.db_url))

async def get_session():
    async_session = sessionmaker(await get_engine(), class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def create_tables():
    try:
        engine = await get_engine()
        async with engine.begin() as eng:
            await eng.run_sync(Base.metadata.create_all)
            print("migration successfully")
    except Exception as e:
        logger.fatal("Не удалось создать таблицы. ", str(e))