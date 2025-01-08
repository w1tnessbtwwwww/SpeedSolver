from sqlalchemy import and_, select
from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import Project
from app.database.repo.team_projects_repository import TeamProjectRepository
from app.utils.result import Result, err, success


class ProjectRepository(AbstractRepository):
    model = Project


    async def create_project(self, title: str, description: str) -> Result[Project]:
        project_query = (
            select(self.model)
            .where(and_(
                self.model.title == title,
                self.model.decsription == description
            ))
        )

        project_result = await self._session.execute(project_query)
        project = project_result.scalars().first()

        if not project:
            return success(value = await self.create(title=title, description=description))
        
        team_project_repo = TeamProjectRepository(self._session)

        project_assign_query = (
            select(team_project_repo.model)
            .where(and_(
                team_project_repo.model.projectId == project.projectId
            ))
        )

        project_assign_result = await self._session.execute(project_assign_query)
        project_assign = project_assign_result.scalars().first()

        if not project_assign:
            return success(value = await self.create(title=title, description=description))
        
        return err("Проект с таким названием у команды уже существует")