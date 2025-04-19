
from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import Team


class TeamRepository(AbstractRepository):
    model = Team
