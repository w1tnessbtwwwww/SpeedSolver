from sqlalchemy import select
from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import Objective, ProjectModerator
from app.database.repo.project_moderator_repo import ProjectModeratorRepository
from app.services.project_service import ProjectService
from app.services.team_projects_service import TeamProjectService
from app.services.team_service import TeamService
from app.utils.result import err


class ObjectiveRepository(AbstractRepository):
    model = Objective

    async def is_project_moderator(self, projectId: str, userId: str):
        project_moderator = await ProjectModeratorRepository(self._session).get_by_filter_one(
            projectId=projectId, userId=userId
        )

        team_project_service = TeamProjectService(self._session)

        project_service = ProjectService(self._session)
        team = await team_project_service.get_team_by_project(projectId)
        if not team.success:
            return err(team.error)
        

        return True if (project_moderator or await project_service.can_interract_with_team(userId, team.value.teamId)) else False
        