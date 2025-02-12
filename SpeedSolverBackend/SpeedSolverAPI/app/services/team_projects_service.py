from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.models import Team
from app.database.repo.team_projects_repository import TeamProjectRepository
from app.utils.result import err, success

class TeamProjectService:

    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo = TeamProjectRepository(session)

    async def get_team_by_project(self, projectId: str) -> Result[Team]:
        return await self._repo.get_team_by_project(projectId)
        
    