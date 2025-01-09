
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.models import User
from app.database.repo.user_profile_repository import UserProfileRepository

from app.schema.request.get_access import authorize, register
from app.schema.request.account.updateprofile import UpdateProfile

from app.security.hasher import hash_password, verify_password
from app.security.jwtmanager import JWTManager

from app.utils.result import Result, err, success

class UserProfileService:
    
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo: UserProfileRepository = UserProfileRepository(session)


    async def update_profile(self, userId: str, update_request: UpdateProfile):
        return await self._repo.update_profile(
            userId,
            update_request.surname,
            update_request.name,
            update_request.patronymic,
            update_request.birthdate
        )