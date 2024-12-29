
from typing import List, Sequence
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.models import User

from app.database.repo.user_repository import UserRepository

from app.schema.request.get_access import authorize, register
from app.schema.request.account.updateprofile import UpdateProfile
from app.schema.response.AccessToken import AccessToken

from app.services.verification_service import VerificationService
from app.utils.email_service.email_service import EmailService
from app.utils.result import Result, err, success

from app.routing.security.hasher import hash_password, verify_password

from app.routing.security.jwtmanager import JWTManager
from app.routing.security.jwttype import JWTType


class UserService:

    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo: UserRepository = UserRepository(session)


    async def update_profile(self, token: str, update_request: UpdateProfile):
        user: User = await JWTManager().get_current_user(token, self._session)
        await self._repo.update_profile()

    async def register(self, register_request: register.RegisterRequest) -> Result[None]:
       try:
           inserted = await self._repo.create(email=register_request.email, password=hash_password(register_request.password))
           await VerificationService(self._session).create_verification(inserted.userId, register_request.email)
       except IntegrityError as e:
           return err("Пользователь с такой почтой уже зарегистрирован.")
       return success("Пользователь успешно зарегистрирован. Проверьте почту.")
        
    async def authorize(self, email: str, password: str):
        ...

    async def delete_profile(self, token: str):
        user: User = await JWTManager().get_current_user(token, self._session)
        return await self._repo.delete_by_id(user.userId)