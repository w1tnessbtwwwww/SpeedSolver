
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.models import User

from app.database.repo.user_repository import UserRepository

from app.schema.request.get_access import authorize, register
from app.schema.request.account.updateprofile import UpdateProfile
from app.schema.response.AccessToken import AccessToken

from app.utils.result import Result, err, success

from app.routing.security.hasher import hash_password, verify_password

from app.routing.security.jwtmanager import JWTManager
from app.routing.security.jwttype import JWTType


class UserService:

    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo: UserRepository = UserRepository(session)


    async def update_profile(self, token: str, update_request: UpdateProfile):
        user: User = await JWTManager().get_current_user(token, self._session)
        await self._repo.update_profile()

    async def register(self, register_request: register.RegisterRequest) -> Result[None]:
        try:
            user = await self._repo.create(email=register_request.email, password=hash_password(register_request.password))
            return success(user)
        except IntegrityError:
            return err("Такой пользователь уже есть.")
        except Exception as e: 
            return success("Что-то пошло не так. Информация уже направлена разработчику.")
        
    async def authorize(self, email: str, password: str) -> Result[AccessToken]:
        authenticated: Result = await self._repo.authenticate_user(email, password)
        if authenticated.error:
            return err(authenticated.error)
        
        payload: dict = {
            "userId": str(authenticated.value.userId),
            "email": authenticated.value.email
        }

        jwt_manager = JWTManager()
        return success(AccessToken(
            access_token=jwt_manager.encode_token(payload, token_type=JWTType.ACCESS),
            refresh_token=jwt_manager.encode_token(payload, token_type=JWTType.REFRESH),
            token_type="Bearer"
        ))

    async def delete_profile(self, token: str):
        user: User = await JWTManager().get_current_user(token, self._session)
        return await self._repo.delete_by_id(user.userId)