from uuid import UUID
from fastapi import APIRouter, Depends

from app.database.database import get_session
from app.database.models.models import User
from app.security.jwtmanager import get_current_user

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.team_service import TeamService
team_invites_router = APIRouter(
    prefix="/invites",
    tags=["Team Invites"]
)


@team_invites_router.post("/invite")
async def invite_to_team(team_id: UUID, user_id: UUID, moderator: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await TeamService(session).invite_user(team_id, user_id, moderator.id)