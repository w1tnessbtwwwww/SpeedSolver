from fastapi import APIRouter, Depends, HTTPException

from app.database.database import get_session
from app.database.models.models import User
from app.security.jwtmanager import get_current_user
from app.schema.request.project.create_project import CreateProject

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.project_service import ProjectService

project_router = APIRouter(
    prefix="/projects",
)

@project_router.post("/create")
async def create_project(create_project: CreateProject, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    creating = await ProjectService(session).create_project(create_project.for_team, create_project.title, create_project.description)