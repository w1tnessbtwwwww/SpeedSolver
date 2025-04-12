from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.database.models.models import User
from app.database.repo.user_repository import UserRepository
from app.database.database import get_session

from app.schema.response.AccessToken import AccessToken
from app.schema.request.get_access.register import RegisterRequest

from app.services.user_service import UserService

from app.services.verification_service import VerificationService

from app.utils.result import Result
from app.utils.verify_codes_generator.code_generator import generate_confirmation_code 

from app.security.jwttype import JWTType
from app.security.jwtmanager import JWTManager, get_current_user, oauth2_scheme
from app.security.jwtmanager import oauth2_scheme

from app.exc.bad_email import BadEmail

from sqlalchemy.ext.asyncio import AsyncSession

from app.cfg.settings import settings

auth_router = APIRouter(prefix="/access", tags=["System Access"])



@auth_router.post("/register")
async def register(registerRequest: RegisterRequest, session: AsyncSession = Depends(get_session)):
    registered = await UserService(session).register(registerRequest)
    if not registered.success:
        raise HTTPException(status_code=400, detail=registered.error)
    return {
        "message": registered.value
    }


@auth_router.post("/authorize")
async def authorize(
    response: Response,
    username: str = Form(), 
    password: str = Form(), 
    session: AsyncSession = Depends(get_session)):
    
    user = await UserRepository(session).get_by_filter_one(email=username)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    authorized = await UserService(session).authorize(username, password)
    if not authorized.success:
        raise HTTPException(status_code=401, detail=authorized.error)
    
    jwt_manager = JWTManager()
    access_token = jwt_manager.encode_token({ "userId": str(user.userId) }, token_type=JWTType.ACCESS)
    refresh_token = jwt_manager.encode_token({ "userId": str(user.userId) }, token_type=JWTType.REFRESH)
    
    access_token_expires = (datetime.now(tz=timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_LIFETIME_MINUTES)).strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    refresh_token_expires = (datetime.now(tz=timezone.utc) + timedelta(days=settings.JWT_REFRESH_TOKEN_LIFETIME_DAYS)).strftime("%a, %d-%b-%Y %H:%M:%S GMT")

    access_token = (
        f"access_token={access_token};"
        f" Expires={access_token_expires};"
        " HttpOnly; Path=/; Secure; SameSite=None; Partitioned"
    )

    access_token = (
        f"access_token={refresh_token};"
        f" Expires={refresh_token_expires};"
        " HttpOnly; Path=/; Secure; SameSite=None; Partitioned"
    )

    response.headers.append("Set-Cookie", access_token)
    response.headers.append("Set-Cookie", refresh_token)

    return AccessToken(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer"
    )


async def refresh_access_token(request: Request):
    
    cookies = request.cookies
    refresh_token = cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token is not provided")

    jwt_manager = JWTManager()
    token_data = jwt_manager.decode_token(refresh_token)
    if token_data.error:
        raise HTTPException(status_code=400, detail=token_data.error)


    session: AsyncSession = await get_session()
    user = await UserRepository(session).get_by_filter_one(userId=token_data.value["userId"])
    session.close()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    return jwt_manager.encode_token({ "userId": str(user.userId), "email": user.email }, token_type=JWTType.ACCESS)

@auth_router.get("/refresh")
async def refresh(token: str = Depends(refresh_access_token)):
    response = JSONResponse(content = {
        "access_token": token
    })
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response
