from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.models import Project
from app.database.repo.project_repository import ProjectRepository
from app.services.team_service import TeamService
from app.utils.result import Result, err, success


class ProjectService:
    
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo: ProjectRepository = ProjectRepository(session)


    async def create_project(self, user_sender: str, team_id: str, title: str, description: str) -> Result[Project]:
        team = await TeamService(self._session).is_team_exists(team_id=team_id)
        if not team:
            return err("Команда не найдена.")
        
        is_user_moderator = await TeamService(self._session).is_user_moderator(user_sender, team_id=team_id)

        if not is_user_moderator:
            return err("Вы не являетесь модератором данной команды.")
        
        return await self._repo.create_project(binded_teamId=team_id, title=title, description=description)
    