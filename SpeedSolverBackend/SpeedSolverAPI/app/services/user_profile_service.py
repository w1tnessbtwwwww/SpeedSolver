
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.models.models import User
from app.database.repo.user_profile_repository import UserProfileRepository

from app.schema.request.get_access import authorize, register
from app.schema.request.account.updateprofile import UpdateProfile

from app.routing.security.hasher import hash_password, verify_password
from app.routing.security.jwtmanager import JWTManager

from app.utils.result import Result, err, success

class UserProfileService:
    
    def __init__(self, session: Session):
        self._session = session
        self._repo: UserProfileRepository = UserProfileRepository(session)


    async def update_profile(self, token: str, update_request: UpdateProfile):
        user: User = await JWTManager().get_current_user(token, self._session)
        return await self._repo.update_profile(
            user.userId,
            update_request.surname,
            update_request.name,
            update_request.patronymic,
            update_request.birthdate
        )