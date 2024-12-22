from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine, 
    AsyncEngine
)

from sqlalchemy.orm import sessionmaker


from ..cfg.settings import settings

async def get_engine() -> AsyncEngine:
    return create_async_engine(str(settings.db_url))

async def get_session():
    async_session = sessionmaker(await get_engine(), expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        return session
