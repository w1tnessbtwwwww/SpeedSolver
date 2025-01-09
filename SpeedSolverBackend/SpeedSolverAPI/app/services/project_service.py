from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.models import Project
from app.database.repo.project_repository import ProjectRepository
from app.services.team_service import TeamService
from app.utils.result import Result, err, success


class ProjectService:
    
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo: ProjectRepository = ProjectRepository(session)


    async def create_project(self, team_id: str, title: str, description: str) -> Result[Project]:
        team = await TeamService(self._session).is_team_exists(team_id)

        return err("Такой команды не найдено.") if not team else success("Команда есть")
    