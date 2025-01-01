from fastapi import APIRouter, Depends

from app.routing.security.jwtmanager import JWTManager, oauth2_scheme

email_router = APIRouter(
    prefix="/email",
    tags=["Email"]
)

@email_router.post("/confirm")
async def confirm_email(user_id: str, code: str, token: str = Depends(oauth2_scheme)):
    user = JWTManager().get_current_user()

@email_router.post("/change")
async def change_email(user_id: str, email: str):
    ...
