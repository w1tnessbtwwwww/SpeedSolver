from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import CursorResult, and_, delete, select, update, insert

from app.routing.security.hasher import verify_password

from app.utils.result import *
from app.utils.logger.telegram_bot.telegram_logger import logger

from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import Organization

from datetime import datetime




class OrganizationRepository(AbstractRepository):
    model = Organization


    async def create_organization(self, **kwargs) -> Result[Organization]:
        query = (
            select(self.model)
            .where(and_(
                self.model.title == kwargs["title"],
                self.model.leaderId == kwargs["leaderId"]
            ))
        )

        result = await self._session.execute(query)
        organization = result.scalars().first()

        if organization:
            return err("Организация уже существует")

        return success(value = await self.create(**kwargs))
    
    async def update_organization(self, **kwargs) -> Result[Organization]:
        query = (
            update(self.model)
            .where(and_(
                self.model.organizationId == kwargs["organizationId"],
            ))
            .values(**kwargs).returning(self.model)
        )

        result = await self._session.execute(query)
        await self._session.commit()
        organization = result.scalars().first()

        if not organization:
            return err("Организация не найдена")

        return success(organization)