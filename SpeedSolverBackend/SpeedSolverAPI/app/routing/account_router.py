from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.routing.security.jwtmanager import oauth2_scheme

from app.services.user_profile_service import UserProfileService
from app.services.user_service import UserService

from app.database.database import get_session

from app.schema.request.account.updateprofile import UpdateProfile

account_router = APIRouter(
    prefix="/account",
    tags=["Account"]
)

@account_router.put("/updateprofile")
async def update_profile(updateRequest: UpdateProfile, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
   result = await UserProfileService(session).update_profile(token, updateRequest)

   if not result.success:
       raise HTTPException(
            status_code=400, 
            detail=result.error
        )
   
   return result.value
   
@account_router.delete("/delete")
async def delete_account(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    result = await UserService(session).delete_profile(token)

    if not result.success:
        raise HTTPException(
            status_code=400, 
            detail=result.error
        )
    
    return result.value
