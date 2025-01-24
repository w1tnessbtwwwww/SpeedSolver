from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.database.models.models import User
from app.schema.request.objective.create_objective import CreateObjective
from app.security.jwtmanager import get_current_user
from app.services.objective_service import ObjectiveService


objective_router = APIRouter(
    prefix="/objectives",
)


@objective_router.get("/all")
async def get_all_tasks(project_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    raise HTTPException(status_code=400, detail="Not implemented")

@objective_router.post("/create")
async def create_task(project_id: str, create_request: CreateObjective, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    creating = await ObjectiveService(session).create_objective(
        project_id=project_id,
        author_id=user.userId,
        create_objective=create_request
    )

    if not creating.success:
        raise HTTPException(status_code=400, detail=creating.error)
    
    return creating.value
