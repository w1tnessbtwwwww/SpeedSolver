from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_session
from app.database.models.models import User
from app.security.jwtmanager import get_current_user
from app.services.link_team_role_service import LinkTeamRoleSerivce

team_link_roles_router = APIRouter(
    prefix="/link"
)


@team_link_roles_router.post("/{role_id}")
async def link_team_role_to_user(role_id: str, 
                                 link_to: str = Depends(),
                                 session: AsyncSession = Depends(get_session),
                                 user: User = Depends(get_current_user)):
    return await LinkTeamRoleSerivce(session).link_role(role_id, link_to)
