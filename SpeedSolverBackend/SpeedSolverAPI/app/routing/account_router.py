from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.models import User
from app.security.jwtmanager import get_current_user, oauth2_scheme

from app.services.user_profile_service import UserProfileService
from app.services.user_service import UserService

from app.database.database import get_session

from app.schema.request.account.updateprofile import UpdateProfile

account_router = APIRouter(
    prefix="/account",
    tags=["Account"]
)

@account_router.put("/updateprofile")
async def update_profile(updateRequest: UpdateProfile, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
   result = await UserProfileService(session).update_profile(user.userId, updateRequest)

   if not result.success:
       raise HTTPException(
            status_code=400, 
            detail=result.error
        )
   
   return result.value
   
@account_router.delete("/delete")
async def delete_account(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    result = await UserService(session).delete_user(user.userId)

    if not result.success:
        raise HTTPException(
            status_code=400, 
            detail=result.error
        )
    
    return result.value
