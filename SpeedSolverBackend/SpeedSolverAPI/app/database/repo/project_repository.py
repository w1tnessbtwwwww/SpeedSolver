from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import Project

class ProjectRepository(AbstractRepository):
    model = Project