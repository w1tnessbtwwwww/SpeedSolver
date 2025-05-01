from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.database.models.models import User
from app.schema.response.user.read_user import ReadUser
from app.security.jwtmanager import get_current_user
from app.services.team_service import TeamService

team_members_router = APIRouter(
    prefix="/members"
)


@team_members_router.get("/{team_id}/get_all", response_model=List[ReadUser], summary="Получить всех участников команды")
async def get_all_team_members(team_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await TeamService(session).get_all_members(team_id, user.id)