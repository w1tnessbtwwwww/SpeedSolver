
import datetime
from typing import List, Sequence
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import and_, delete, select
from sqlalchemy.orm import selectinload, defer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.models import Organization, Project, ProjectModerator, Team, TeamInvitation, TeamMember, User, UserProfile

from app.database.repo.project_invitation_repository import ProjectInvitationRepository
from app.database.repo.project_members_repository import ProjectMembersRepository
from app.database.repo.project_repository import ProjectRepository
from app.database.repo.team_invitation_repository import TeamInvitationRepository
from app.database.repo.team_member_repository import TeamMemberRepository
from app.schema.request.project.create_project import CreateProject
from app.services.team_project_service import TeamProjectService
from app.services.team_service import TeamService

class TeamInvitationService:

    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo: TeamInvitationRepository = TeamInvitationRepository(session)

    async def decline_invite(self, user_id: UUID, invite_id: UUID):

        current_member = await TeamMemberRepository(self._session).get_by_filter_one(invited_by_request_id=invite_id)

        if current_member:
            raise HTTPException (
                status_code=400,
                detail="Вы не можете отклонить принятое приглашение в команду."
            )

        query = (
            delete(self._repo.model)
            .where(and_(
                self._repo.model.id == invite_id,
                self._repo.model.invited_user_id == user_id
            ))
        )

        result = await self._session.execute(query)
        await self._session.commit()
        return result.rowcount

    async def accept_invite(self, user_id: UUID, invite_id: UUID):
        
        current_invite = (
            select(self._repo.model)
            .where(and_(
                self._repo.model.id == invite_id,
                self._repo.model.invited_user_id == user_id
            ))
            .order_by(self._repo.model.created_at.desc())
        )

        exec = await self._session.execute(current_invite)
        invite = exec.scalars().first()

        if not invite:
            raise HTTPException (
                status_code=400,
                detail="Приглашение не найдено."
            )
        
        now = datetime.datetime.now(tz=datetime.timezone.utc)

        if invite.created_at + datetime.timedelta(days=1) < now:
            raise HTTPException (
                status_code=400,
                detail="Приглашение более не действительно."
            )
        
        current_member = await TeamMemberRepository(self._session).get_by_filter_one(invited_by_request_id=invite.id)
        if current_member:
            raise HTTPException (
                status_code=400,
                detail="Вы уже состоите в команде."
            )

        return await TeamMemberRepository(self._session).create(teamId=invite.teamId, userId=user_id, invited_by_request_id=invite.id)


    async def invite_user(self, team_id: UUID, user_id: UUID, moderator_id: UUID):
        current_member = await TeamMemberRepository(self._session).get_by_filter_one(teamId=team_id, userId=user_id)

        if current_member:
            raise HTTPException (
                status_code=400,
                detail="Пользователь уже состоит в команде."
            )

        if not await TeamService(self._session).is_user_team_moderator(moderator_id, team_id):
            raise HTTPException (
                status_code=403,
                detail="У вас нет прав на приглашение в команду."
            )
        
        last_invite_query = (
            select(TeamInvitation)
            .where(and_(TeamInvitation.invited_user_id == user_id, TeamInvitation.teamId == team_id))
            .order_by(TeamInvitation.created_at.desc())
        )

        exec = await self._session.execute(last_invite_query)
        last_invite = exec.scalars().first()

        now = datetime.datetime.now(tz=datetime.timezone.utc)

        if not last_invite:
            return await self._repo.create(invited_user_id=user_id, invited_by_leader_id=moderator_id, teamId=team_id)
        if last_invite.created_at + datetime.timedelta(days=1) > now:
            raise HTTPException (
                status_code=400,
                detail="Приглашение уже было отправлено"
            )

        return await self._repo.create(invited_user_id=user_id, invited_by_leader_id=moderator_id, teamId=team_id)
        