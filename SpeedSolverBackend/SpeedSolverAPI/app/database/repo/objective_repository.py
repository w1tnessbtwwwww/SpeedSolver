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

    

        
        