from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repo.verification_repository import VerificationRepository
from app.utils.result import Result, err, success
from app.utils.email_service.email_service import EmailService

from app.routing.security.jwtmanager import JWTManager
class VerificationService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo: VerificationRepository = VerificationRepository(session)


    async def request_verification(self, email: str, to_user: str) -> Result[None]:
        try:
            code = await self._repo.insert_verification(to_user)
            await EmailService().send_verify_code("Подтверждение регистрации", email, f"{code.value.verification_code}")
        except Exception as e:
            return err("Произошла ошибка при создании верификации.")
        
    async def confirm_email(self, email: str, code: str) -> Result[None]:
        return await self._repo.confirm_email(email, code)