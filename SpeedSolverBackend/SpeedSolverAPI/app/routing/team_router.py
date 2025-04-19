from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.database.models.models import User
from app.schema.request.team.create_team import CreateTeam
from app.security.jwtmanager import get_current_user
from app.services.team_service import TeamService

team_router = APIRouter(
    prefix="/team",
    tags=["Team"]
)

# @team_router.get("/get_all")
# async def get_all_teams(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
#     return await TeamService(session).get_all_teams(user.id)

@team_router.post("/create")
async def create_team(team: CreateTeam, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    return await TeamService(session).create_team(team, user.id)