from fastapi.security import OAuth2PasswordBearer
import jwt
from app.cfg.settings import settings
from app.database.repo.user_repository import UserRepository
from app.database.database import get_session
from app.utils.result import Result
from app.routing.security.hasher import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class JWTManager:
    
    def __init__(self):
        self.SECRET_KEY = settings.JWT_SECRET_KEY
        self.ALGORITHM = settings.JWT_ALGORITHM
        self.EXPIRES_AT = settings.JWT_EXPIRES_AT

    @classmethod
    def encode_token(self, payload: dict):
        jwt_payload = payload.copy().update({"exp": self.EXPIRES_AT * 60})
        return jwt.encode(jwt_payload, self.SECRET_KEY, algorithm=self.ALGORITHM)
    
    @staticmethod
    def authenticate_user(email: str, password: str) -> Result[None]:
        with get_session() as session:
            user = UserRepository(session).get_by_filter_one(email=email)
            if not user:
                return Result(success=False, error="User not found")
            if not verify_password(password, user.password):
                return Result(success=False, error="Invalid password")
            return Result(success=True, value=user)
        
    
    @staticmethod
    def decode_token(token: str) -> dict:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])