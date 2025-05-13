from typing import List
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.schema.response.user.read_user import ReadUser
from app.services.user_service import UserService

search_router = APIRouter(
    prefix="/search",
    tags=["Поиск"]
)

@search_router.get("/user/find/{param}", response_model=List[ReadUser])
async def search_user(param: str, session: AsyncSession = Depends(get_session)):
    return await UserService(session).find_user(param)