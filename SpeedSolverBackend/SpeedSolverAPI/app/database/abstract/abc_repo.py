from abc import ABC

from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
class AbstractRepository(ABC):

    def __init__(self, session: AsyncSession):
        self._session = session

    model = None

    async def commit(self):
        try:
            await self._session.commit()
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    def rollback(self):
        self._session.rollback()

    async def get_by_id(self, id):
        return await self._session.get(self.model, id)

    async def get_all(self):
        result = await self._session.execute(select(self.model))
        return result.scalars().all()

    async def create(self, **kwargs):
        query = insert(self.model).values(**kwargs).returning(self.model)
        result = await self._session.execute(query)
        await self.commit()
        return result.scalars().first()

    async def delete_by_id(self, id):
        result = await self._session.execute(delete(self.model).where(self.model.id == id))
        return result.rowcount

    async def get_by_filter_all(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self._session.execute(query)
        return result.scalars().all()

    async def get_by_filter_one(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self._session.execute(query)
        return result.scalars().one_or_none()