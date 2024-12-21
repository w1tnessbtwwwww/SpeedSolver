
from sqlalchemy.orm import Session

from app.database.models.models import User
from app.database.repo.team_repository import TeamRepository

from app.routing.security.jwtmanager import JWTManager

from app.schema.request.team.create_team import CreateTeam
from app.schema.request.team.update_team import UpdateTeam

class TeamService:
    def __init__(self, session: Session):
        self._session = session
        self._repo = TeamRepository(session)

    async def create_team(self, createRequest: CreateTeam, token: str):
        user = await JWTManager().get_current_user(token, self._session)
        return await self._repo.create_team(createRequest.name, createRequest.description, user.userId, createRequest.organizationId)
    
    async def update_team(self, updateRequest: UpdateTeam, token: str):
        user = await JWTManager().get_current_user(token, self._session)
        return await self._repo.update_team(
            updateRequest.teamId,
            user.userId,
            updateRequest.new_name,
            updateRequest.new_description,
            updateRequest.new_leader_id
        )
        