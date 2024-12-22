
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.models import Organization, User
from app.database.repo.organization_repository import OrganizationRepository

from app.routing.security.jwtmanager import JWTManager

from app.schema.request.organization.create_organization import CreateOrganization


class OrganizationService:

    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo = OrganizationRepository(session)

    async def create_organization(self, createRequest: CreateOrganization, token: str):
        user: User = await JWTManager().get_current_user(token, self._session)
        return await self._repo.create_organization(title=createRequest.name, description=createRequest.description, leaderId=user.userId)