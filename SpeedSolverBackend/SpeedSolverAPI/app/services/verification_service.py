from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repo.verification_repository import VerificationRepository
from app.utils.result import Result, err, success
from app.utils.email_service.email_service import EmailService
from app.utils.logger.telegram_bot.telegram_logger import logger
from app.utils.verify_codes_generator.code_generator import generate_confirmation_code
from app.routing.security.jwtmanager import JWTManager
class VerificationService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo: VerificationRepository = VerificationRepository(session)


    async def process_verification(self, userId: str, email: str):
        code = await EmailService().send_verify_code("Подтверждение письма", email)
        if not code.success:
            logger.fatal(code.error)
            return

        verification = await self._repo.process_verification(userId, code.value)
        return verification
    
    async def resend_verification(self, userId: str, email: str):
        return await self._repo.resend_verification(userId, email)
    
    async def confirm_email(self, userId: str, code: str) -> Result[None]:
        return await self._repo.confirm_email(userId, code)