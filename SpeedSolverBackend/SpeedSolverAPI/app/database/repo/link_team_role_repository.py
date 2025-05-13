from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import LinkTeamRole


class LinkTeamRoleRepository(AbstractRepository):
    model = LinkTeamRole