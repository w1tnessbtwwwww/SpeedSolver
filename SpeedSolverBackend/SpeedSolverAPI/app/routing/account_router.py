import os
import uuid
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
import glob

from app.database.models.models import User
from app.schema.response.user.read_user_profile import ReadUserProfile
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


@account_router.get("/profile/get")
async def get_profile(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await UserProfileService(session).get_profile(user.id)

@account_router.put("/profile/update")
async def update_profile(updateRequest: UpdateProfile, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await UserProfileService(session).update_profile(user.id, **updateRequest.model_dump())

@account_router.put("/profile/avatar/update", response_model=ReadUserProfile)
async def upload_avatar(avatar: UploadFile = File(...), user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):    
    if not avatar.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"Файл {avatar.filename} не является изображением",
        )
    
    try:
        exists = glob.glob(f"speedsolver-avatars/avatar_{user.id}.*")
        if exists:
            os.remove(exists[0])
        extension = avatar.filename.split(".")[-1] # jpg, png?
        path = f"speedsolver-avatars/avatar_{user.id}.{extension}"
        directory = os.path.dirname(path)
        os.makedirs(directory, exist_ok=True)
        with open(f"{path}", "wb") as f:
            f.write(await avatar.read())

        return await UserProfileService(session).update_profile(user.id, avatar_path=path)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Произошла ошибка во время загрузки файла {avatar.filename}: {str(e)}",
        )

    
   
@account_router.delete("/delete")
async def delete_account(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    result = await UserService(session).delete_user(user.userId)

    if not result.success:
        raise HTTPException(
            status_code=400, 
            detail=result.error
        )
    
    return result.value
