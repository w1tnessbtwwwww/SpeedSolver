from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from app.database.database import get_session
from app.schema.request.team.update_team import UpdateTeam
from app.services.team_service import TeamService
from app.routing.security.jwtmanager import JWTManager, oauth2_scheme


from app.schema.request.team.create_team import CreateTeam
team_router = APIRouter(prefix="/team", tags=["Teams management"])


@team_router.post("/create", summary="Создать команду")
async def create_team(createRequest: CreateTeam, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    raise HTTPException(status_code=400, detail="Not implemented")

@team_router.put("/update", summary="Обновить команду")
async def update_team(updateRequest: UpdateTeam, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    raise HTTPException(status_code=400, detail="Not implemented")