from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import TeamMember

class TeamMemberRepository(AbstractRepository):
    model = TeamMember