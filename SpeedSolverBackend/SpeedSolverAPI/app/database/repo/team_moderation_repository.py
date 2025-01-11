from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import TeamModerator

class TeamModerationRepository(AbstractRepository):

    model = TeamModerator

