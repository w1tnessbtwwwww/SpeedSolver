from sqlalchemy import Result, select
from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import Team, TeamProject
from app.utils.result import err, success

class TeamProjectRepository(AbstractRepository):
    model = TeamProject

    async def get_team_by_project(self, projectId: str) -> Result[Team]:
        try:
            query = (
                select(Team)
                .join(TeamProject, TeamProject.projectId == projectId)
            )
            team = await self._session.execute(query)
            teamProject = team.scalars().all()
            return success(teamProject)
        except Exception as e:
            return err(str(e))