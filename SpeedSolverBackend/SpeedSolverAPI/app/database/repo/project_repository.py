from sqlalchemy import and_, select
from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import Project
from app.database.repo.team_projects_repository import TeamProjectRepository
from app.utils.result import Result, err, success
from app.utils.logger.telegram_bot.telegram_logger import logger


class ProjectRepository(AbstractRepository):
    model = Project


    async def create_project(self, binded_teamId: str, title: str, description: str) -> Result[Project]:
        team_project_repo = TeamProjectRepository(self._session)
        team_projects = await team_project_repo.get_by_filter_all(teamId=binded_teamId)

        project_query = (
            select(self.model)
            .where(
                self.model.projectId.in_([team_project.projectId for team_project in team_projects])
            )
        )

        project = await self._session.execute(project_query)
        project = project.scalars().one_or_none()

        if project:
            return err("Проект с таким названием уже существует.")

        project = await self.create(title=title, description=description)

        created = await team_project_repo.create(teamId=binded_teamId, projectId=project.projectId)
        return success(created)



        
        