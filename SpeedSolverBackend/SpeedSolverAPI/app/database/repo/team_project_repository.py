from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import TeamProject

class TeamProjectRepository(AbstractRepository):
    model = TeamProject