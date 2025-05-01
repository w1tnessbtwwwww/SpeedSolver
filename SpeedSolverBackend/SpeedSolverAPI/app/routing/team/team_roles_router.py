from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.database.models.models import User
from app.schema.request.team.roles.create_role import CreateRole
from app.schema.request.team.roles.update_role import UpdateRole
from app.security.jwtmanager import get_current_user
from app.services.custom_team_role_service import CustomTeamRoleService

team_roles_router = APIRouter(
    prefix="/roles"
)

@team_roles_router.post("/{team_id}/create", summary="Создать роль внутри команды")
async def create_team_role(team_id: str, role_data: CreateRole, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    return await CustomTeamRoleService(session).create_team_role(team_id, user.id, role_data)

@team_roles_router.post("/{role_id}/update", summary="Обновить роль внутри команды")
async def update_team_role(role_id: str, updates: UpdateRole, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    updated = await CustomTeamRoleService(session).update_team_role(role_id, user.id, updates)
    return updated

@team_roles_router.delete("/{role_id}/delete", summary="Удалить роль внутри команды")
async def update_team_role(role_id: str, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    return await CustomTeamRoleService(session).delete_team_role(role_id, user.id)
