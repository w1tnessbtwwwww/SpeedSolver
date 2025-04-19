from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import ProjectMember

class ProjectMembersRepository(AbstractRepository):
    model = ProjectMember