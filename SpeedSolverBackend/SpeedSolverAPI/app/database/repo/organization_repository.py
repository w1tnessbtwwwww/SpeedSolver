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


    async def delete_organization(self, **kwargs) -> Result[int]:
        query = (
            delete(self.model)
            .where(and_(
                self.model.organizationId == kwargs["organizationId"],
                self.model.leaderId == kwargs["leaderId"]
            ))
        )

        try:
            result = await self._session.execute(query)
            await self._session.commit()

            if result.rowcount < 1:
                return err("Организация не найдена")

            return success(result.rowcount)
        except Exception as e:
            logger.error(f"Не удалось удалить организацию OrganizationRepository.", str(e))
            return err("Произошла ошибка при удалении организации. Информация направлена разработчику.")

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
    
    async def update_organization(self,
                                  organizationId: str,
                                  new_title: Optional[str] = None, 
                                  new_description: Optional[str] = None) -> Result[Organization]:

        query = (
            select(self.model)
            .where(and_(
                self.model.organizationId == organizationId,
                self.model.leaderId == self.model.leaderId
            ))
        )
        result = await self._session.execute(query)
        await self._session.commit()
        organization = result.scalars().first()

        if not organization:
            return err("Организация не найдена")

        update_query = (
            update(self.model)
            .where(self.model.organizationId == organizationId)
            .values(
                title = new_title if new_title else organization.title,
                description = new_description if new_description else organization.description
            )
            .returning(self.model)
        )        

        try:            
            updating = await self._session.execute(update_query)
            await self._session.commit()
            organization = updating.scalars().first()
        except Exception as e:
            logger.error(f"Не удалось обновить организацию OrganizationRepository.", str(e))
            return err("Произошла ошибка при обновлении организации. Информация направлена разработчику.")
        return success(organization)