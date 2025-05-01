from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import CustomTeamRole


class CustomTeamRoleRepository(AbstractRepository):
    model = CustomTeamRole