from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import EmailVerification
from sqlalchemy import select, update, delete, insert

from app.database.models.models import User

from app.utils.result import Result, err, success
from app.utils.verify_codes_generator.code_generator import generate_confirmation_code
class VerificationRepository(AbstractRepository):
    model = EmailVerification

    async def insert_verification(self, for_user: str, verification_code: str) -> Result[None]:
        query = (
            select(self.model)
            .where(self.model.userId == for_user)
            .join(User, User.userId == self.model.userId)
        )

        result = await self._session.execute(query)
        verification = result.scalars().first()
        if not verification:
            creating = await self.create(userId=for_user, verification_code=verification_code)
            return success("Код успешно добавленн") if creating else err("Не удалось добавить код верификации.")
        
        replacing = await self.update(userId=for_user, verification_code=verification_code)
        return success(f"Новый код успешно отправлен на почту {verification.user.email}") if replacing else err("Не удалось обновить код верификации.")
    

    async def confirm_email(self, userId: str, code: str) -> Result[None]:
        query = (
            select(self.model)
            .where(self.model.userId == userId)
            .join(User, User.userId == self.model.userId)
        )


        result = await self._session.execute(query)
        verify = result.scalars().first()
        if not verify:
            return err("Пользователь не найден или почта уже подтверждена.")
        
        if (code == verify.verification_code):
            verify.user.is_mail_verified = True
            await self.session.execute(delete(self.model).where(self.model.userId == verify.userId))
            await self._session.commit()
            return success("Почта успешно подтверждена.")
        
        return err("Неверный код.")