from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import OrganizationInvitation

class OrganizationInvitationRepository(AbstractRepository):
    model = OrganizationInvitation