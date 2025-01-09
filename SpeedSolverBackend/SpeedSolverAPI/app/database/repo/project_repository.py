from sqlalchemy import and_, select
from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import Project
from app.database.repo.team_projects_repository import TeamProjectRepository
from app.utils.result import Result, err, success
from app.utils.logger.telegram_bot.telegram_logger import logger


class ProjectRepository(AbstractRepository):
    model = Project


    async def create_project(self, binded_teamId: str, title: str, description: str) -> Result[Project]:

        team_project_repository = TeamProjectRepository(self._session)


        project_query = (
            select(self.model)
            .where(
                and_(
                    self.model.title == title,
                    self.model.description == description
                )
            )
        )

        project_result = await self._session.execute(project_query)
        projects = project_result.scalars().all()


        team_projects_query = (
            select(team_project_repository.model)
            .where(
                team_project_repository.model.teamId == binded_teamId
            )
        )

        team_projects_result = await self._session.execute(team_projects_query)
        team_projects = team_projects_result.scalars().all()


        
        