from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.routing.security.hasher import verify_password
from app.utils.result import Result, err, success
from ..abstract.abc_repo import AbstractRepository
from app.database.models.models import User

from sqlalchemy import CursorResult, delete, select, update, insert

class UserRepository(AbstractRepository):
    model = User

    async def update_by_id(self, userId: str, **kwargs):
        query = update(self.model).where(self.model.userId == userId).values(**kwargs).returning(self.model)
        result = await self._session.execute(query)
        await self._session.commit()
        return result.scalars().first()

    async def authenticate_user(self, email: str, password: str) -> Result:
        user = await UserRepository(self._session).get_by_filter_one(email=email)
        if not user:
            return err("User not found")
        if not verify_password(password, user.password):
            return err("Invalid password")
        return success(user)
    
    async def get_by_email(self, email) -> Optional[User]:
        result = await self._session.execute(select(self.model).where(self.model.email == email))
        user = result.scalars().first()
        if not user:
            return None
        
        return user
    async def delete_by_id(self, id):
        try:
            result = await self._session.execute(delete(self.model).where(self.model.userId == id))
            await self._session.commit()
            return success(result.rowcount)
        except Exception as e:
            return err(str(e))
