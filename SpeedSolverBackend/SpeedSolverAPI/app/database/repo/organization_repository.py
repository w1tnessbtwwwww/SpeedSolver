from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import Organization

class OrganizationRepository(AbstractRepository):
    model = Organization

    