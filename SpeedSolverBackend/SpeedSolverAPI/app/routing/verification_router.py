from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.database.models.models import User


from app.schema.request.email.confirm_email import EmailConfirmation
from app.schema.request.email.resend_code import ResendCode

from app.services.user_service import UserService
from app.services.verification_service import VerificationService

from app.security.jwtmanager import JWTManager, get_current_user, oauth2_scheme

verification_router = APIRouter(
    prefix="/verification",
    tags=["Verification"]
)

@verification_router.post("/resend", summary="Запросить код подтверждения снова")
async def resend_verification(email: ResendCode, session: AsyncSession = Depends(get_session)):
    user = await UserService(session).get_by_email(email.email)
    if not user.success:
        raise HTTPException(status_code=400, detail=user.error)
    
    
    result = await VerificationService(session).resend_verification(user.value.id, user.value.email)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    
    return {
        "message": "Письмо успешно отправлено."
    }
@verification_router.post("/confirm", summary="Подтвердить почту по коду")
async def confirm_verification(confirmRequest: EmailConfirmation, session: AsyncSession = Depends(get_session)):
    user = await UserService(session).get_by_email(confirmRequest.email)
    if not user.success:
        raise HTTPException(status_code=400, detail=user.error)

    result = await VerificationService(session).confirm_email(user.value.id, confirmRequest.code)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    
    verify_user = await UserService(session).confirm_email(user.value.id)

    return {
        "message": "Почта успешно подтверждена."
    }