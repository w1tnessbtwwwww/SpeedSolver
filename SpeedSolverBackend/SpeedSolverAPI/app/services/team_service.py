
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.models import User
from app.database.repo.team_repository import TeamRepository

from app.routing.security.jwtmanager import JWTManager

from app.schema.request.team.create_team import CreateTeam
from app.schema.request.team.update_team import UpdateTeam

class TeamService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo = TeamRepository(session)

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
        