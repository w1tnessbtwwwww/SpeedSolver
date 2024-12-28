from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repo.verification_repository import VerificationRepository
from app.utils.result import Result, err, success
from app.utils.email_service.email_service import EmailService

from app.routing.security.jwtmanager import JWTManager
class VerificationService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo: VerificationRepository = VerificationRepository(session)


    async def create_verification(self, user_id: str):
        verification_code = EmailService().generate_code()
        return await self._repo.insert_verification(user_id, verification_code) 