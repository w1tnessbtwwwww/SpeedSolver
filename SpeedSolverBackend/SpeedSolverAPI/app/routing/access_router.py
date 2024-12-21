from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.database.models.models import User
from app.database.repo.user_repository import UserRepository
from app.database.database import get_session

from app.schema.response.AccessToken import AccessToken
from app.schema.request.get_access.register import RegisterRequest


from app.services.user_service import UserService


from app.utils.result import Result
from app.utils.logger.logger import logger

from app.routing.security.jwttype import JWTType
from app.routing.security.jwtmanager import JWTManager, oauth2_scheme



from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/access", tags=["System Access"])

@auth_router.post("/register")
async def register(registerRequest: RegisterRequest, session: Session = Depends(get_session)):
    registered: Result = await UserService(session).register(registerRequest)
    if not registered.success:
        raise HTTPException(status_code=400, detail=registered.error)
    
    logger.info(f"User {registered.value.email} registered")
    return {
        "register": "User registered successfully"        
    }


@auth_router.post("/authorize")
async def authorize(username: str = Form(), password: str = Form(), session: Session = Depends(get_session)):
    
    authorized: Result[AccessToken] = await UserService(session).authorize(username, password)
    if not authorized.success:
        raise HTTPException(status_code=400, detail=authorized.error)
    
    response = JSONResponse(
        content = {
            "access_token": authorized.value.access_token,
            "refresh_token": authorized.value.refresh_token,
            "token_type": "Bearer"
        }
    )
    response.set_cookie(key="access_token", value=authorized.value.access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=authorized.value.refresh_token, httponly=True)
    return response


async def refresh_access_token(request: Request):
    
    cookies = request.cookies
    refresh_token = cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token is not provided")

    jwt_manager = JWTManager()
    token_data = jwt_manager.decode_token(refresh_token)
    if token_data.error:
        raise HTTPException(status_code=400, detail=token_data.error)

    with await get_session() as session:
        user = await UserRepository(session).get_by_filter_one(userId=token_data.value["userId"])
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
