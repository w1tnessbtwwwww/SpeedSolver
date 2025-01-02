from fastapi import APIRouter, Depends, HTTPException

from app.database.database import get_session
from app.routing.security.jwtmanager import JWTManager, oauth2_scheme

from sqlalchemy.ext.asyncio import AsyncSession

email_router = APIRouter(
    prefix="/email",
    tags=["Email"]
)

@email_router.post("/change")
async def change_email(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    raise HTTPException(status_code=400, detail="Not implemented")
