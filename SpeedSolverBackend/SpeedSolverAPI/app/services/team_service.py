from uuid import UUID

from sqlalchemy import select

from app.database.models.models import TeamMember, User
from app.database.repo.team_repository import TeamRepository
from app.schema.request.team.create_team import CreateTeam


class TeamService:
    def __init__(self, session):
        self.session = session
        self.repo = TeamRepository(session)
        

    async def create_team(self, team: CreateTeam, leader_id: UUID):
        return await self.repo.create(leaderId=leader_id, **team.model_dump())

    async def get_all_user_teams(self, user_id: UUID):
        query = (
            select(self.repo.model)
            .join_from(TeamMember, User, TeamMember.userId == user_id)
        )
        exec = await self.session.execute(query)
        result = exec.scalars().all()
        return result