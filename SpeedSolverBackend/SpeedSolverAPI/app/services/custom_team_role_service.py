from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repo.custom_team_role_repository import CustomTeamRoleRepository
from app.schema.request.team.roles.create_role import CreateRole
from app.schema.request.team.roles.update_role import UpdateRole
from app.services.team_service import TeamService


class CustomTeamRoleService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo: CustomTeamRoleRepository = CustomTeamRoleRepository(session)

    async def delete_team_role(self, role_id, user_id: UUID):
        role = await self._repo.get_by_id(role_id)
        if not role:
            raise HTTPException(
                status_code=400,
                detail="Такая роль не найдена :("
            )

        if not await TeamService(self._session).is_user_team_moderator(user_id, role.team_id):
            raise HTTPException(
                status_code=403,
                detail="У вас нет доступа удалению ролей"
            )
        
        deleted_rows = await self._repo.delete_by_id(role_id)
        await self._repo.commit()
        return deleted_rows

    async def create_team_role(self, team_id: UUID, user_id: UUID, role_data: CreateRole):
        if not await TeamService(self._session).is_user_team_moderator(user_id, team_id):
            raise HTTPException(
                status_code=403,
                detail="У вас нет доступа на создание ролей в команде"
            )
        
        return await self._repo.create(team_id=team_id, **role_data.model_dump())


    async def update_team_role(self, role_id: UUID, user_id: UUID, updates: UpdateRole):
        role = await self._repo.get_by_id(role_id)

        if not await TeamService(self._session).is_user_team_moderator(user_id, role.team_id):
            raise HTTPException(
                status_code=403,
                detail="У вас нет доступа на обновление этой роли"
            )
        
        query = (
            update(self._repo.model)
            .where(self._repo.model.id == role_id)
            .values(**updates.model_dump())
            .returning(self._repo.model)
        )

        result = await self._session.execute(query)
        await self._session.commit()
        updated = result.scalars().first()
        return updated

