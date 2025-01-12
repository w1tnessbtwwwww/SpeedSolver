
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.models import Team, User
from app.database.repo.team_moderation_repository import TeamModerationRepository
from app.database.repo.team_repository import TeamRepository

from app.security.jwtmanager import JWTManager

from app.schema.request.team.create_team import CreateTeam
from app.schema.request.team.update_team import UpdateTeam
from app.services.user_service import UserService

class TeamService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo = TeamRepository(session)


    async def is_user_moderator(self, user_id: str, team_id: str):
        team_moderation_repo = TeamModerationRepository(self._session)
        team: Team = await self._repo.get_by_filter_one(teamId=team_id)
        if not team:
            return False

        if team.leaderId == user_id:
            return True
        

        team_mod = await team_moderation_repo.get_by_filter_one(userId=user_id, teamId=team_id)
        return True if team_mod else False

    async def is_team_exists(self, team_id: str) -> bool:
        
        team = await self._repo.get_by_filter_one(teamId=team_id)

        return True if team else False

    async def get_team_by_project(self, projectId: str):
        
        return await self._repo.get_team_by_project(projectId)

    async def delete_team(self, team_id: str, leaderId: str):
        
        return await self._repo.delete_team(teamId=team_id, leaderId=leaderId)

    async def create_team(self, createRequest: CreateTeam, leaderId: str):
        return await self._repo.create_team(createRequest.name, 
                                            createRequest.description, 
                                            leaderId, 
                                            createRequest.organizationId)
    
    async def update_team(self, updateRequest: UpdateTeam, leaderId: str, team_id: Optional[str] = None):
        return await self._repo.update_team(teamId=team_id, 
                                            leaderId=leaderId, 
                                            new_title=updateRequest.new_name, 
                                            new_description=updateRequest.new_description, 
                                            new_leader_id=updateRequest.new_leader_id)
        