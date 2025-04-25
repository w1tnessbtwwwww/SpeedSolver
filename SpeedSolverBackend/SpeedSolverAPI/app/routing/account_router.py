from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.models import User
from app.security.jwtmanager import get_current_user, oauth2_scheme

from app.services.organization_service import OrganizationService
from app.services.team_service import TeamService
from app.services.user_profile_service import UserProfileService
from app.services.user_service import UserService

from app.database.database import get_session

from app.schema.request.account.updateprofile import UpdateProfile

account_router = APIRouter(
    prefix="/account",
    tags=["Account"]
)

# @account_router.get("/my_organizations/get_all")
# async def get_my_organizations(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
#    return await OrganizationService(session).get_all_user_organizations(user.id)

@account_router.get("/teams/get_all")
async def get_my_teams(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await UserService(session).get_all_teams(user.id)

@account_router.put("/profile/update")
async def update_profile(updateRequest: UpdateProfile, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
   result = await UserProfileService(session).update_profile(user.id, updateRequest)
   return result
   
@account_router.delete("/delete")
async def delete_account(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    result = await UserService(session).delete_user(user.userId)

    if not result.success:
        raise HTTPException(
            status_code=400, 
            detail=result.error
        )
    
    return result.value
