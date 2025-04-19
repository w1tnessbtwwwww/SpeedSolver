from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.database.models.models import User
from app.schema.request.organization.create_organization import CreateOrganization
from app.security.jwtmanager import get_current_user
from app.services.organization_service import OrganizationService

organization_router = APIRouter(
    prefix="/organization",
    tags=["Организации"]
)

@organization_router.post("/create")
async def create_organization(organization: CreateOrganization, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    return await OrganizationService(session).create_organization(user.id, organization)