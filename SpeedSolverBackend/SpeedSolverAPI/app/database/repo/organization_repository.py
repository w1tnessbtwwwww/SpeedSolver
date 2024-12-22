from sqlalchemy.ext.asyncio import AsyncSession

from app.routing.security.hasher import verify_password
from app.utils.result import *
from ..abstract.abc_repo import AbstractRepository
from app.database.models.models import Organization
from datetime import datetime
from sqlalchemy import CursorResult, and_, delete, select, update, insert



class OrganizationRepository(AbstractRepository):
    model = Organization


    async def create_organization(self, **kwargs) -> Result[None]:
        try:
            query = (
                select(self.model)
                .where(and_(
                    self.model.leaderId == kwargs['leaderId'],
                    self.model.title == kwargs['title']
                ))
            )
            result = self._session.execute(query)
            organization = result.scalars().first()
            if organization:
                return err("Organization already exists")
            return success(value=await self.create(**kwargs))
        except Exception as e:
            return err(str(e))