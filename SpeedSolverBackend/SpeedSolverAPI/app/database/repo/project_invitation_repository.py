from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import ProjectInvitation

class ProjectInvitationRepository(AbstractRepository):
    model = ProjectInvitation