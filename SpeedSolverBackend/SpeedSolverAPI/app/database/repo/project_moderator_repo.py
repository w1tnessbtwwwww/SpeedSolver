from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import ProjectModerator

class ProjectModeratorRepository(AbstractRepository):
    model = ProjectModerator