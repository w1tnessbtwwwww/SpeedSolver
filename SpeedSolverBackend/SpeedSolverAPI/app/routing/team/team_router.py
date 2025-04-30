from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.database.models.models import User
from app.schema.request.team.create_team import CreateTeam
from app.schema.request.team.update_team import UpdateTeam
from app.schema.response.team.team import ReadTeam
from app.security.jwtmanager import get_current_user
from app.services.team_service import TeamService

from app.routing.team.team_invites_router import team_invites_router
from app.routing.team.team_members_router import team_members_router
team_router = APIRouter(
    prefix="/teams",
    tags=["Team"]
)

team_router.include_router(team_invites_router)
team_router.include_router(team_members_router)


@team_router.get("/about/{team_id}")
async def team_about(team_id: str, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    return await TeamService(session).get_team(team_id, user.id)

@team_router.post("/create")
async def create_team(team: CreateTeam, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    return await TeamService(session).create_team(team, user.id)

@team_router.patch("/edit/{team_id}")
async def edit_team(team_id: UUID, updates: UpdateTeam, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    if not await TeamService(session).is_user_team_moderator(user.id, team_id):
        raise HTTPException(
            status_code=403,
            detail="У вас нет прав на редактирование данной команды."
        )
    return await TeamService(session).update_team(team_id, updates)

@team_router.delete("/delete/{team_id}")
async def delete_team(team_id: UUID, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    if not await TeamService(session).is_user_leader(user.id, team_id):
        raise HTTPException(
            status_code=403,
            detail="У вас нет прав на удаление данной команды."
        )
    return await TeamService(session).repo.delete_by_id(team_id)
