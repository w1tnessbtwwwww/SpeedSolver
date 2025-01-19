import select
from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import Organization, Team, TeamInvitation
from app.services.team_service import TeamService
from app.utils.result import err, success
from sqlalchemy.exc import IntegrityError

from sqlalchemy import select, update, insert, delete
class InviteRepository(AbstractRepository):
    model = TeamInvitation



    async def get_all_invites(self, user_id: str):
        query = (
            select(Team.title, Team.description)
            .select_from(self.model)
            .where(self.model.invited_user_id == user_id)
            .join(Team, Team.teamId == self.model.teamId)
        )

        try:
            result = await self._session.execute(query)
            return success(result.mappings().all())
        except Exception as e:
            return err(str(e))