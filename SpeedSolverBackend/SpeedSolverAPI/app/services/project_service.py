from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import and_, func, select
from sqlalchemy.orm import selectinload, joinedload, aliased
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.models import Objective, Project, ProjectModerator, User, UserProfile

from app.database.repo.objective_repository import ObjectiveRepository
from app.database.repo.project_invitation_repository import ProjectInvitationRepository
from app.database.repo.project_members_repository import ProjectMembersRepository
from app.database.repo.project_repository import ProjectRepository
from app.schema.request.objective.create_objective import CreateObjective
from app.schema.request.project.create_project import CreateProject
from app.services.team_project_service import TeamProjectService
from app.services.team_service import TeamService

class ProjectService:

    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo: ProjectRepository = ProjectRepository(session)
        self._objRepo: ObjectiveRepository = ObjectiveRepository(session)


    async def get_all_tasks(self, project_id: UUID, user_id: UUID):

        if not await self.is_user_project_member(project_id, user_id):
            raise HTTPException(status_code=403, detail="Вы не являетесь участником проекта")

        # query = (
        #     select(Objective)
        #     .where(Objective.projectId == project_id)
        #     .options(selectinload(Objective.child_objectives), selectinload(Objective.author).selectinload(User.profile))
        # )

        print(project_id)

        query = (
            select(Objective.title, Objective.description, Objective.created_at, Objective.deadline_date,
                   UserProfile.name
            )
            .join(User, User.id == Objective.author_id)
            .join(UserProfile, UserProfile.userId == User.id)
            .where(Objective.projectId == project_id)
        )

        exec = await self._session.execute(query)
        result = exec.mappings().all()
        return result

    async def create_task(self, project_id: UUID, author_id: UUID, task_data: CreateObjective):
        if not await self.is_user_project_member(project_id, author_id):
            raise HTTPException(status_code=403, detail="Вы не являетесь участником проекта")
        return await self._objRepo.create(projectId=project_id, author_id=author_id, **task_data.model_dump())
    
    async def delete_task(self, task_id: UUID, member_id: UUID):
        project_query = (
            select(Project)
            .select_from(Objective)
            .where(Project.id == Objective.projectId)
            .join(Project)
        )

        exec = self._session.execute(project_query)
        project = exec.scalars().first()

        if not await self.is_user_project_member(project.id, member_id):
            raise HTTPException(status_code=403, detail="Вы не являетесь участником проекта")

        return await self._objRepo.delete(task_id)


    async def is_user_project_member(self, project_id: UUID, user_id: UUID):
        member = await ProjectMembersRepository(self._session).get_by_filter_one(projectId=project_id, userId=user_id)
        return True if member else False

    async def is_user_project_creator(self, project_id: UUID, user_id: UUID):
        if await TeamService(self._session).is_user_team_moderator(user_id, project_id):
            return True
        
        query = (
            select(Project)
            .where(Project.id == project_id)
        )

        exec = await self._session.execute(query)
        result = exec.scalars().first()

        if result.creator_id == user_id:
            return True

        return False

    async def is_user_project_moderator(self, project_id: UUID, user_id: UUID):
        if await self.is_user_project_creator(project_id, user_id):
            return True

        query = (
            select(ProjectModerator)
            .where(and_(
                ProjectModerator.projectId == project_id,
                ProjectModerator.userId == user_id
            ))
        )

        exec = await self._session.execute(query)
        result = exec.scalars().first()

        if result:
            return True

        return False

    async def create_project(self, creator_id: UUID, for_team: UUID, project_data: CreateProject):
        if await TeamService(self._session).is_user_team_moderator(creator_id, for_team):
            try:
                project = await self._repo.create(creator_id=creator_id, title=project_data.title, description=project_data.description)
                for user_id in project_data.auto_invite:
                    await ProjectInvitationRepository(self._session).create(invited_user_id=user_id, invited_by_leader_id=creator_id, projectId=project.id)
                team_project = await TeamProjectService(self._session).link_project(team_id=for_team, project_id=project.id)
                creator_in_project = await ProjectMembersRepository(self._session).create(projectId=project.id, userId=creator_id)
                return project
            except IntegrityError:
                raise HTTPException(
                    status_code=500,
                    detail="Произошла ошибка внесения данных в базу данных"
                )