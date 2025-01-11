from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.database.models.models import User
from app.security.jwtmanager import get_current_user
from app.services.project_service import ProjectService
from app.services.user_service import UserService

test_router = APIRouter(
    prefix="/test"
)
