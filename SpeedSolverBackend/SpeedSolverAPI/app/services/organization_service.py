
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.models import Organization, User
from app.database.repo.organization_repository import OrganizationRepository

from app.security.jwtmanager import JWTManager

from app.schema.request.organization.create_organization import CreateOrganization
from app.schema.request.organization.update_organization import UpdateOrganization
from app.utils.logger.telegram_bot.telegram_logger import logger
from app.utils.result import Result, err, success


class OrganizationService:

    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo = OrganizationRepository(session)

    async def delete_organization(self, organizationId: str, leaderId: str) -> Result[int]:
        try:
            deleting = await self._repo.delete_organization(organizationId=organizationId, leaderId=leaderId)
            if not deleting.success:
                return err(deleting.error)
            return success(deleting.value)
        except Exception as e:
            logger.error(f"Произошла ошибка в OrganizationService. при удалении организации.", str(e))
            return err("Произошла ошибка при удалении организации. Информация направлена разработчику.")
        

    async def create_organization(self, createRequest: CreateOrganization, userId: str) -> Result[Organization]:
        return await self._repo.create_organization(title=createRequest.name, description=createRequest.description, leaderId=userId)
    
    async def update_organization(self, updateRequest: UpdateOrganization, userId: str) -> Result[Organization]:
        organization = await self._repo.get_by_filter_one(organizationId=updateRequest.organizationId, leaderId=userId)

        if not organization:
            return err("Организация не найдена.")
    
        organization_upd = await self._repo.update_organization(organizationId=updateRequest.organizationId, new_title=updateRequest.new_title, new_description=updateRequest.new_description)
        if not organization_upd.success:
            return err(organization_upd.error)
        
        return success(organization_upd.value)
        