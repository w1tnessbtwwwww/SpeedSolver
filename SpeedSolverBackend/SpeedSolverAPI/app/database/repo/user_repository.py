from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.security.hasher import verify_password

from app.utils.result import Result, err, success
from app.utils.logger.telegram_bot.telegram_logger import logger

from app.database.models.models import User, TeamModerator
from app.database.abstract.abc_repo import AbstractRepository

from sqlalchemy import delete, select, update, insert

class UserRepository(AbstractRepository):
    model = User

    async def get_moderation_teams(self, userId: str):
        query = (
            select(self.model)
            .where(self.model.id == userId)
            .join(TeamModerator, TeamModerator.id == self.model.id)
        )

        result = await self._session.execute(query)
        user = result.mappings().all()
        return user

    async def create(self, **kwargs):
        query = insert(self.model).values(**kwargs).returning(self.model)
        result = await self._session.execute(query)
        return result.scalars().first()

    async def authenticate_user(self, email: str, password: str) -> Result:
        user = await UserRepository(self._session).get_by_filter_one(email=email)
        if not user:
            return err("User not found")
        if not verify_password(password, user.password):
            return err("Invalid password")
        return success(user)
    
    async def get_by_email(self, email) -> Optional[User]:
        try:

            result = await self._session.execute(select(self.model).where(self.model.email == email))
            user = result.scalars().first()
            if not user:
                return None
            return user

        except Exception as e:
            logger.error(f"Произошла ошибка в UserRepository.", str(e))
    
    async def delete_by_id(self, id) -> Result[int]:
        try:
            result = await self._session.execute(delete(self.model).where(self.model.userId == id))
            await self._session.commit()
            return success(result.rowcount)
        except Exception as e:
            return err(str(e))
