
from sqlalchemy import UUID, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.models import User
from app.database.repo.user_profile_repository import UserProfileRepository

from app.database.repo.user_repository import UserRepository
from app.schema.request.get_access import authorize, register
from app.schema.request.account.updateprofile import UpdateProfile

from app.security.hasher import hash_password, verify_password
from app.security.jwtmanager import JWTManager

from app.utils.result import Result, err, success

class UserProfileService:
    
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo: UserProfileRepository = UserProfileRepository(session)


    async def get_profile(self, userId: UUID):
        return await UserRepository(self._session).get_by_id_with_profile(userId)

    async def update_profile(self, userId: UUID, **kwargs):

        current_profile = await self._repo.get_by_filter_one(userId=userId)
        if current_profile is None:
            insert_query = (
                insert(self._repo.model)
                .values(userId=userId, **kwargs)
                .returning(self._repo.model)
            )

            exec = await self._session.execute(insert_query)
            await self._session.commit()
            result = exec.scalars().one_or_none()
            return result

        query = (
            update(self._repo.model)
            .where(self._repo.model.userId == userId)
            .values(**kwargs)
            .returning(self._repo.model)
        )

        exec = await self._session.execute(query)
        await self._session.commit()
        result = exec.scalars().one_or_none()
        return result
        