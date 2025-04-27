
from typing import List, Sequence
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload, defer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.models import Organization, Team, TeamMember, User, UserProfile

from app.database.repo.user_repository import UserRepository

from app.schema.request.get_access import authorize, register
from app.schema.request.account.updateprofile import UpdateProfile
from app.schema.response.AccessToken import AccessToken

from app.services.verification_service import VerificationService
from app.utils.email_service.email_service import EmailService
from app.utils.result import Result, err, success

from app.security.hasher import hash_password, verify_password

from app.security.jwtmanager import JWTManager
from app.security.jwttype import JWTType


class UserService:

    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo: UserRepository = UserRepository(session)


    async def get_all_teams(self, user_id: UUID):
        query = (
            select(Team)
            .join_from(Team, TeamMember, Team.id == TeamMember.teamId)
            .where(TeamMember.userId == user_id)       
        )

        exec = await self._session.execute(query)
        result = exec.scalars().all()
        return result

    async def get_moderation_teams(self, userId: str):
        return await self._repo.get_moderation_teams(userId)

    async def delete_account(self, userId: str):
        return await self._repo.delete_by_id(userId)

    async def get_by_email(self, email: str):
        user = await self._repo.get_by_email(email)
        return success(user) if user else err("Пользователь не найден.")

    async def confirm_email(self, userId: str):
        return await self._repo.update_by_id(userId, is_mail_verified=True)

    async def update_profile(self, token: str, update_request: UpdateProfile):
        raise NotImplementedError

    async def register(self, register_request: register.RegisterRequest) -> Result[None]:
       try:
            inserted = await self._repo.create(email=register_request.email, password=hash_password(register_request.password))
            is_verification_inserted = await VerificationService(self._session).process_verification(inserted.id, inserted.email)
            if not is_verification_inserted.success:
                await self._repo.rollback()
                return err(is_verification_inserted.error)
            
            await self._repo.commit()
       except IntegrityError as e:
            return err(str(e))
       return success("Пользователь успешно зарегистрирован. Проверьте почту.")
        
    async def authorize(self, email: str, password: str):
        authenticated = await self._repo.authenticate_user(email, password)
        if not authenticated.success:
            return err("Неправильный логин или пароль")
        
        if not authenticated.value.is_mail_verified:
            return err("Почта не подтверждена. Если кода нет, запросите его повторно")
        return success(authenticated.value)
        
    async def is_email_verified(self, username: str) -> Result[None]:
        user = await self._repo.get_by_filter_one(email=username)
        if not user:
            return err("Пользователь не найден.")
        if not user.is_mail_verified:
            return err("Почта не подтверждена. Если кода нет, запросите его повторно")
        return success("Почта подтверждена.")


    async def delete_profile(self, token: str):
        user: User = await JWTManager().get_current_user(token, self._session)
        return await self._repo.delete_by_id(user.userId)