from sqlalchemy.orm import Session
from sqlalchemy.engine import create_engine, Engine

from ..cfg.settings import settings

def get_engine() -> Engine:
    return create_engine(str(settings.db_url))

async def get_session() -> Session:
    return Session(bind=create_engine(str(settings.db_url)))