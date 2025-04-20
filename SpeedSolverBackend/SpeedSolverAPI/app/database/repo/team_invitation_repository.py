from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import TeamInvitation

class TeamInvitationRepository(AbstractRepository):
    model = TeamInvitation