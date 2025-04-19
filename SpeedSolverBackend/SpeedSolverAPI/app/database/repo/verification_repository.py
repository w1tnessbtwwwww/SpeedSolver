import datetime
from typing import Annotated, Callable, Optional
from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import EmailVerification, User

from app.utils.email_service.email_service import EmailService
from app.utils.result import Result, err, success
from app.utils.verify_codes_generator.code_generator import generate_confirmation_code
from app.utils.logger.telegram_bot.telegram_logger import logger

from sqlalchemy import and_, desc, select, update, delete, insert
from sqlalchemy.exc import IntegrityError


class VerificationRepository(AbstractRepository):
    model = EmailVerification

    async def resend_verification(self, userId: str, verification_code: str) -> Result[Optional[EmailVerification]]:

        clear_query = (
            delete(self.model)
            .where(self.model.id == userId)
        )

        await self._session.execute(clear_query)
        await self._session.commit()

        try:
            return success(await self.create(id=userId, verification_code=verification_code))
        except Exception as e:
            logger.error("Произшла ошибка в репозитории верификации.")
            return err("Произошла ошибка. Информация уже направлена разработчику")

    async def process_verification(self, userId: str, verification_code: str) -> Result[None]:
        last_verification_query = (
            select(self.model)
            .order_by(desc(self.model.created_at))
            .where(self.model.userId == userId)
        )

        result = await self._session.execute(last_verification_query)
        last_verification = result.scalars().first()
        if not last_verification:
            verification = await self.create(userId=userId, verification_code=verification_code)
            return success(verification)
        
        return err("Верификация уже была пройдена.")


    async def confirm_email(self, userId: str, code: str) -> Result[None]:
        logger.info(str(datetime.datetime.now(datetime.timezone.utc)))
        try:
            query = (
                select(self.model)
                .where(
                    self.model.userId == userId,
                )
                .order_by(desc(self.model.created_at))
            )

            result = await self._session.execute(query)
            verification = result.scalars().first()

            if datetime.datetime.now() > verification.created_at + datetime.timedelta(minutes=15):
                return err("Время верификации истекло. Запросите верификацию повторно.")

            if code == verification.verification_code:
                await self.delete_by_id(userId)
                return success("Верификация прошла успешно.")
            return err("Код не верный.")
        except Exception as e:
            logger.error(e)
            return err("Проиизошла ошибка в сервисе верификации. Информация направлена разработчику.")

    async def delete_by_id(self, id) -> Result[int]:
        try:
            result = await self._session.execute(
                delete(self.model).where(self.model.id == id)
            )
            await self._session.commit()
            return success(result.rowcount)
        except:
            return err(0)