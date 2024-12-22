from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repo.verification_repository import VerificationRepository
from app.utils.result import Result, err, success
from app.utils.email_service.email_service import EmailService

from app.routing.security.jwtmanager import JWTManager
class VerificationService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo: VerificationRepository = VerificationRepository(session)


    async def request_verification(self, token: str, to_user: str) -> Result[None]:
        try:
            user = await JWTManager().get_current_user(token, self._session)
            code = await EmailService.send_verify_code("Подтверждение регистрации", f"{user.email}", f"{code.value.verification_code}")
            await self._repo.insert_verification(to_user, code)
        except Exception as e:
            return err("Произошла ошибка при создании верификации.")
        
    async def confirm_email(self, token: str, code: str) -> Result[None]:
        user = await JWTManager().get_current_user(token, self._session)
        
        return await self._repo.confirm_email(user.userId, code)