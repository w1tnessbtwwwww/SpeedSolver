from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from ..cfg.settings import settings

async def get_engine() -> AsyncEngine:
    return create_async_engine(str(settings.db_url))

async def get_session() -> Session:
    return Session(bind=await get_engine())