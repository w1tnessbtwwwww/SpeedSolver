from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import EmailVerification, User

from app.utils.result import Result, err, success
from app.utils.verify_codes_generator.code_generator import generate_confirmation_code

from sqlalchemy import and_, select, update, delete, insert
from sqlalchemy.exc import IntegrityError


class VerificationRepository(AbstractRepository):
    model = EmailVerification

    async def insert_verification(self, for_user: str, verification_code: str) -> Result[None]:
        try:
            creating = await self.create(userId=for_user, verification_code=verification_code)
            return success("Код на верификацию почты успешно создан.") if creating else err("Не удалось создать код на верификацию почты.")
        except IntegrityError:
            updating = await self.update(for_user=for_user, verification_code=verification_code)
            return success("Код на подтверждение успешно обновлен.") if updating else err("Не удалось обновить код для подтверждения почты.")
        
    async def confirm_email(self, userId: str, code: str) -> Result[None]:
        try:
            query = (
                select(self.model)
                .where(
                    self.model.userId == userId,
                )
            )

            result = await self._session.execute(query)
            verification = result.scalars().first()
            if code == verification.verification_code:
                await self.delete_by_id(userId)
                return success("Верификация прошла успешно.")
            return err("Код не верный.")
        except Exception as e:
            return err("Проиизошла ошибка. Информация направлена разработчику.")
    async def update(self, for_user: str, **kwargs):
        ...

    async def delete_by_id(self, id) -> Result[int]:
        try:
            result = await self._session.execute(
                delete(self.model).where(self.model.userId == id)
            )
            await self._session.commit()
            return success(result.rowcount)
        except:
            return err(0)