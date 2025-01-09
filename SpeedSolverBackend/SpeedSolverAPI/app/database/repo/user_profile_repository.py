from sqlalchemy.ext.asyncio import AsyncSession

from app.security.hasher import verify_password
from app.utils.result import *
from ..abstract.abc_repo import AbstractRepository
from app.database.models.models import UserProfile
from datetime import datetime
from sqlalchemy import CursorResult, delete, select, update, insert
from typing import Optional

class UserProfileRepository(AbstractRepository):
    model = UserProfile

    async def update(self, userId: str, **kwargs):
        query = update(self.model).where(self.model.userId == userId).values(**kwargs).returning(self.model)
        result = await self._session.execute(query)
        await self._session.commit()
        return result.scalars().first()

    async def update_profile(self, 
                             userId: str,
                             surname: Optional[str],
                             name: Optional[str],
                             patronymic: Optional[str],
                             birthdate: Optional[datetime]
                             ) -> Result[None]:
        
        query = (
            select(self.model)
            .where(self.model.userId == userId)
        )

        result = await self._session.execute(query)
        profile = result.scalars().one_or_none()
        if not profile:
            creating = await self.create(userId=userId, surname=surname, name=name, patronymic=patronymic, birthdate=birthdate)  
            return success(creating) if creating else err("Some error while attemping resource.")
        return success(await self.update(userId=userId, surname=surname, name=name, patronymic=patronymic, birthdate=birthdate))

