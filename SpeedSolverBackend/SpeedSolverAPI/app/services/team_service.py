from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import and_, select

from app.database.models.models import TeamMember, TeamModerator, User
from app.database.repo.team_invitation_repository import TeamInvitationRepository
from app.database.repo.team_member_repository import TeamMemberRepository
from app.database.repo.team_repository import TeamRepository
from app.schema.request.team.create_team import CreateTeam
from app.schema.request.team.update_team import UpdateTeam
from sqlalchemy.exc import IntegrityError
from app.utils.logger.telegram_bot.telegram_logger import logger
class TeamService:
    def __init__(self, session):
        self.session = session
        self.repo = TeamRepository(session)
        
    async def invite_user(self, team_id: UUID, user_id: UUID, moderator_id: UUID):
        if not await self.is_user_team_moderator(moderator_id, team_id):
            raise HTTPException(
                status_code=403,
                detail="У вас нет прав на приглашение в команду."
            )
        
    

    async def is_user_leader(self, user_id: UUID, team_id: UUID) -> bool:
        team = await self.repo.get_by_id(team_id)
        if team.leaderId == user_id:
            return True
        return False

    async def is_user_team_moderator(self, user_id: UUID, team_id: UUID) -> bool:

        if await self.is_user_leader(user_id, team_id):
            return True

        moderator_query = (
            select(TeamModerator)
            .where(and_(
                TeamModerator.userId == user_id,
                TeamModerator.teamId == team_id
            ))
        )

        exec = await self.session.execute(moderator_query)
        moderator_row = exec.scalars().first()

        if moderator_row:
            return True
        
        return False

    async def update_team(self, team_id: UUID, updates: UpdateTeam):
        return await self.repo.update_by_id(team_id, **updates.model_dump())

    async def create_team(self, team: CreateTeam, leader_id: UUID):
        try:
            created_team = await self.repo.create(leaderId=leader_id, **team.model_dump())
            await TeamMemberRepository(self.session).create(teamId=created_team.id, userId=leader_id)
            return created_team
        except IntegrityError as e:
            logger.error("Произошла ошибка внесения данных в базу данных", str(e))
            raise HTTPException(
                status_code=500,
                detail="Произошла ошибка внесения данных в базу данных"
            )



    async def get_all_user_teams(self, user_id: UUID):
        query = (
            select(self.repo.model)
            .join_from(TeamMember, User, TeamMember.userId == user_id)
        )
        exec = await self.session.execute(query)
        result = exec.scalars().all()
        return result