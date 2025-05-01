from uuid import UUID
from fastapi import APIRouter, Depends

from app.database.database import get_session
from app.database.models.models import User
from app.security.jwtmanager import get_current_user

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.team_invitation_service import TeamInvitationService
from app.services.team_service import TeamService
team_invites_router = APIRouter(
    prefix="/invites"
)


@team_invites_router.post("/invite", summary="Пригласить пользователя в команду")
async def invite_to_team(team_id: UUID, user_id: UUID, moderator: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await TeamInvitationService(session).invite_user(team_id, user_id, moderator.id)

@team_invites_router.post("/accept/{invite_id}", summary="Принять приглашение в команду")
async def accept_invite(invite_id: UUID, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await TeamInvitationService(session).accept_invite(user.id, invite_id)

@team_invites_router.delete("/decline/{invite_id}", summary="Принять приглашение в команду")
async def decline_invite(invite_id: UUID, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await TeamInvitationService(session).decline_invite(user.id, invite_id)