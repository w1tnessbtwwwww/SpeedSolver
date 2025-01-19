from fastapi import APIRouter, Depends, HTTPException

from app.database.database import get_session
from app.database.models.models import User
from app.schema.request.team.invites.invite_user import InviteUser
from app.security.jwtmanager import get_current_user

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.invite_service import InviteService

inviting_router = APIRouter(
    prefix="/invitations"
)

@inviting_router.post("/invite")
async def invite_user(invite_request: InviteUser, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    invited = await InviteService(session).invite_user(user_id=invite_request.user_id, invited_by=user.userId, team_id=invite_request.team_id)
    if not invited.success:
        raise HTTPException(
            status_code=400,
            detail=invited.error
        )
    
    return invited.value

@inviting_router.get("/myinvites")
async def get_my_invites(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    invites = await InviteService(session).get_all_invites(user_id=user.userId)
    if not invites.success:
        raise HTTPException(
            status_code=400,
            detail=invites.error
        )
    
    return invites.value


@inviting_router.post("/accept")
async def accept_invite(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    raise HTTPException(
        status_code=400,
        detail="Not implemented"
    )

@inviting_router.post("/decline")
async def decline_invite(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    raise HTTPException(
        status_code=400,
        detail="Not implemented"
    )