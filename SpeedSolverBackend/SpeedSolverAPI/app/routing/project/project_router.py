from uuid import UUID
from fastapi import APIRouter, Depends

from app.database.database import get_session
from app.database.models.models import User
from app.schema.request.project.create_project import CreateProject
from app.security.jwtmanager import get_current_user
from app.services.project_service import ProjectService
from sqlalchemy.ext.asyncio import AsyncSession
from app.routing.project.task_router import task_router
from app.services.team_service import TeamService
project_router = APIRouter(
    prefix="/projects",
    tags=["Проекты"]
)


@project_router.post("/create/{team_id}", summary="Создать проект")
async def create_project(team_id: UUID, project_data: CreateProject, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await ProjectService(session).create_project(user.id, team_id, project_data)

@project_router.post("/invites/invite", summary="Пригласить пользователя в проект")
async def invite_to_project(project_id: UUID, user_id: UUID, moderator: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await ProjectService(session).invite_user(project_id, user_id, moderator.id)

@project_router.post("/invites/accept/{invite_request_id}", summary="Принять приглашение в проект")
async def join_project(invite_request_id: UUID, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await ProjectService(session).accept_invite(invite_request_id, user.id)

@project_router.delete("/invites/decline/{invite_request_id}", summary="Принять приглашение в команду")
async def decline_invite(invite_request_id: UUID, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await ProjectService(session).decline_invite(invite_request_id, user.id)

@project_router.get("/{team_id}/get_all")
async def get_all_team_projects(team_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await TeamService(session).get_all_projects(team_id, user.id)

project_router.include_router(task_router)