from fastapi import APIRouter, Depends, HTTPException

from app.database.database import get_session
from app.database.models.models import User
from app.schema.request.project.update_project import UpdateProject
from app.security.jwtmanager import get_current_user
from app.schema.request.project.create_project import CreateProject

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.project_service import ProjectService

project_router = APIRouter(
    prefix="/projects",
    tags=["Projects Management"]
)

@project_router.post("/create")
async def create_project(create_project: CreateProject, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    creating = await ProjectService(session).create_project(user.userId, create_project.for_team, create_project.title, create_project.description)
    if not creating.success:
        raise HTTPException(status_code=400, detail=creating.error)
    
    return creating.value

@project_router.put("/update")
async def update_project(project_id: str, update_project: UpdateProject, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    updating = await ProjectService(session).update_project(user.userId, project_id, update_project)
    if not updating.success:
        raise HTTPException(status_code=400, detail=updating.error)
    
    return updating.value