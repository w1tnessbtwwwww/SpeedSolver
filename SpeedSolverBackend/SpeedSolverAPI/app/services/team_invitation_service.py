
from typing import List, Sequence
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.orm import selectinload, defer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.models import Organization, Project, ProjectModerator, Team, TeamMember, User, UserProfile

from app.database.repo.project_invitation_repository import ProjectInvitationRepository
from app.database.repo.project_members_repository import ProjectMembersRepository
from app.database.repo.project_repository import ProjectRepository
from app.database.repo.team_invitation_repository import TeamInvitationRepository
from app.schema.request.project.create_project import CreateProject
from app.services.team_project_service import TeamProjectService
from app.services.team_service import TeamService

class ProjectService:

    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo: TeamInvitationRepository = TeamInvitationRepository(session)

    async def invite_user(self, team_id: UUID, user_id: UUID, moderator_id: UUID):
        if not await TeamService(self._session).is_user_team_moderator(moderator_id, team_id):
            raise HTTPException (
                status_code=403,
                detail="У вас нет прав на приглашение в команду."
            )
        
        