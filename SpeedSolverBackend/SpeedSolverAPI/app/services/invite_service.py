from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repo.invite_repository import InviteRepository
from app.services.team_service import TeamService
from app.utils.result import err, success
from sqlalchemy.exc import IntegrityError
class InviteService:

    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo = InviteRepository(session)

    async def invite_user(self, user_id: str, invited_by: str, team_id: str):
        team_service = TeamService(self._session)

        if not await team_service.is_user_moderator(invited_by, team_id):
            return err("Вы не являетесь модератором данной команды.")
        
        try:
            return success(await self._repo.create(invited_user_id=user_id, invited_by_leader_id=invited_by, teamId=team_id))
        except IntegrityError:
            return err("Пользователь уже приглашен в команду.")
        
    async def get_all_invites(self, user_id: str):
        return await self._repo.get_all_invites(user_id=user_id)