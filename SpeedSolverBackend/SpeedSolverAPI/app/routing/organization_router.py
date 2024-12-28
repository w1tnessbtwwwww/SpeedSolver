from fastapi import APIRouter, Depends, HTTPException
from app.database.database import get_session
from app.schema.request.organization.create_organization import CreateOrganization
from app.services.organization_service import OrganizationService

from app.routing.security.jwtmanager import oauth2_scheme

from sqlalchemy.ext.asyncio import AsyncSession
organization_router = APIRouter(
    prefix="/organization", 
    tags=["Organization"])


@organization_router.post("/create")
async def create_organization(createRequest: CreateOrganization, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    created = await OrganizationService(session).create_organization(createRequest, token)

    if not created.success:
        raise HTTPException(
            status_code=400, 
            detail=created.error
        )
    
    return created.value