from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.database.models.models import User
from app.schema.request.organization.create_organization import CreateOrganization
from app.schema.request.organization.update_organization import UpdateOrganization
from app.security.jwtmanager import get_current_user
from app.services.organization_service import OrganizationService

organization_router = APIRouter(
    prefix="/organizations",
    tags=["Организации"]
)

@organization_router.post("/create", summary="Создать организацию")
async def create_organization(organization: CreateOrganization, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    return await OrganizationService(session).create_organization(user.id, organization)

@organization_router.put("/update/{organization_id}", summary="Обновить организацию")
async def update_organization(upd_organization: UpdateOrganization, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    return await OrganizationService(session).update_organization(user.id, upd_organization)

@organization_router.get("/get_all", summary="Получить все организации в которых администратор или состоишь")
async def get_all_organizations(session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    return await OrganizationService(session).get_all_user_organizations(user.id)

@organization_router.post("/{organization_id}/invite/{user_id}")
async def invite_user(organization_id: UUID, user_id: UUID, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    return await OrganizationService(session).invite_user(organization_id, user_id, user.id)