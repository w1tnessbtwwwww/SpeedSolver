from uuid import UUID
from fastapi import APIRouter, Depends

from app.database.database import get_session
from app.database.models.models import User
from app.schema.request.objective.create_objective import CreateObjective
from app.schema.request.objective.update_objective import UpdateObjective
from app.security.jwtmanager import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.project_service import ProjectService

task_router = APIRouter(
    prefix="/tasks"
)


@task_router.post("/create/{project_id}", summary="Создать задачу для проекта")
async def create_task(project_id: UUID, task_data: CreateObjective, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await ProjectService(session).create_task(project_id, user.id, task_data)

@task_router.get("/all/{project_id}", summary="Получить все задачи и подзадачи проекта")
async def get_all_tasks(project_id: UUID, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await ProjectService(session).get_all_tasks(project_id, user.id)

@task_router.patch("/{task_id}/update", summary="Обновить информацию о задаче")
async def update_task(task_id: UUID, updates: UpdateObjective, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await ProjectService(session).update_task(task_id, user.id, updates)