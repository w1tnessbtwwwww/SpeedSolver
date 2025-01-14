from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.models import Project, Team, TeamProject
from app.database.repo.project_repository import ProjectRepository

from app.database.repo.team_projects_repository import TeamProjectRepository
from app.schema.request.project.create_project import CreateProject
from app.schema.request.project.update_project import UpdateProject

from app.services.team_projects_service import TeamProjectService
from app.services.team_service import TeamService

from app.utils.result import Result, err, success
from multipledispatch import dispatch

class ProjectService:
    
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo: ProjectRepository = ProjectRepository(session)

    

    async def can_interract_with_team(self, userId: str, teamId: str) -> Result[bool]:
        team = await TeamService(self._session).is_team_exists(team_id=teamId)
        if not team:
            return err("Команда не найдена.")
        
        is_user_moderator = await TeamService(self._session).is_user_moderator(userId, teamId)

        if not is_user_moderator:
            return err("Вы не являетесь модератором данной команды.")

    async def create_project(self, user_sender: str, team_id: str, createProject: CreateProject) -> Result[Project]:
        can_interract = await self.can_interract_with_team(user_sender, team_id)
        if not can_interract.success:
            return err(can_interract.error)

        return await self._repo.create_project(binded_teamId=team_id, title=createProject.title, description=createProject.description)
    
    async def update_project(self, user_sender: str, projectId: str, updateProject: UpdateProject):
        team_project_service = TeamProjectService(self._session)
        team = await team_project_service.get_team_by_project(projectId)
        if not team.success:
            return err(team.error)
        
        is_user_moder = await self.can_interract_with_team(user_sender, team.value.teamId)
        if not is_user_moder:
            return err("Вы не являетесь модератором данной команды.")
        
        upd_proj = await self._repo.update_project(projectId=projectId, new_title=updateProject.new_title, new_desc=updateProject.new_description)
        if not upd_proj:
            return err("Не удалось обновить команду")
        
        await self._session.commit()
        return success(upd_proj)
