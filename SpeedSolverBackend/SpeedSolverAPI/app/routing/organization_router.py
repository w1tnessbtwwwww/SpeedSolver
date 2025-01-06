from fastapi import APIRouter, Depends, HTTPException

from app.database.database import get_session
from app.database.models.models import User

from app.schema.request.organization.create_organization import CreateOrganization
from app.schema.request.organization.update_organization import UpdateOrganization

from app.services.organization_service import OrganizationService

from app.routing.security.jwtmanager import oauth2_scheme, get_current_user

from sqlalchemy.ext.asyncio import AsyncSession


organization_router = APIRouter(
    prefix="/organization", 
    tags=["Organization"])


@organization_router.post("/create")
async def create_organization(createRequest: CreateOrganization, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    organization = await OrganizationService(session).create_organization(createRequest, user.userId)

    if not organization.success:
        raise HTTPException(status_code=400, detail=organization.error)
    
    return organization.value

    
@organization_router.put("/update")
async def update_organization(updateRequest: UpdateOrganization, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    updating = await OrganizationService(session).update_organization(updateRequest, user.userId)

    if not updating.success:
        raise HTTPException(status_code=400, detail=updating.error)
    
    return updating.value


@organization_router.delete("/delete")
async def delete_organization(organizationId: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    deleting = await OrganizationService(session).delete_organization(organizationId, user.userId)
    if not deleting.success:
        raise HTTPException(status_code=400, detail=deleting.error)
    
    return deleting.value