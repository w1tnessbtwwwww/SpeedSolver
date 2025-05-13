
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.models import CustomTeamRole
from app.database.repo.link_team_role_repository import LinkTeamRoleRepository
from app.database.repo.custom_team_role_repository import CustomTeamRoleRepository
from app.services.team_service import TeamService

class LinkTeamRoleSerivce:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo: LinkTeamRoleRepository = LinkTeamRoleRepository()


    async def link_role(self, role_id: UUID, user_id: UUID):
        role: CustomTeamRole = await CustomTeamRoleRepository(self._session).get_by_id(role_id)
        if not role:
            raise HTTPException(
                status_code=400,
                detail="Роль не найдена"
            )
        if not await TeamService(self._session).is_user_team_moderator(user_id, role.team_id):
            raise HTTPException(
                status_code=403,
                detail="У вас нет доступа к добавлению ролей"
            )
        
        return await self._repo.create(team_id=role.team_id, user_id=user_id, role_id=role_id)
    
    async def unlink_role(self, role_id: UUID, user_id: UUID):
        role: CustomTeamRole = await CustomTeamRoleRepository(self._session).get_by_id(role_id)
        if not role:
            raise HTTPException(
                status_code=400,
                detail="Роль не найдена"
            )
        if not await TeamService(self._session).is_user_team_moderator(user_id, role.team_id):
            raise HTTPException(
                status_code=403,
                detail="У вас нет доступа к удалению ролей"
            )
        
        return await self._repo.delete_by_id(role.id)
        