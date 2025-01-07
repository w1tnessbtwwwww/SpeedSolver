from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from app.database.database import get_session

from app.database.models.models import User
from app.schema.request.team.update_team import UpdateTeam
from app.schema.request.team.create_team import CreateTeam

from app.services.team_service import TeamService
from app.routing.security.jwtmanager import JWTManager, oauth2_scheme, get_current_user


team_router = APIRouter(prefix="/team", tags=["Teams management"])


@team_router.post("/create")
async def create_team(createRequest: CreateTeam, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    
    creating = await TeamService(session).create_team(createRequest, user.userId)
    if not creating.success:
        raise HTTPException(status_code=400, detail=creating.error)
    
    return creating.value

@team_router.put("/update")
async def update_team(team_id: str,updateRequest: UpdateTeam, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    updating = await TeamService(session).update_team(updateRequest, user.userId, team_id)
    if not updating.success:
        raise HTTPException(status_code=400, detail=updating.error)
    
    return updating.value

@team_router.delete("/delete")
async def delete_team(team_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    deleting = await TeamService(session).delete_team(team_id, user.userId)
    if not deleting.success:
        raise HTTPException(status_code=400, detail=deleting.error)
    
    return deleting.value