


from uuid import UUID
from sqlalchemy import select, update
from fastapi import HTTPException
from app.database.models.models import Organization, TeamMember
from app.database.repo.organization_repository import OrganizationRepository
from app.schema.request.organization.create_organization import CreateOrganization


class OrganizationService:
    def __init__(self, session):
        self.session = session
        self.repo = OrganizationRepository(session)

    async def is_user_organization_leader(self, user_id: UUID, organization_id: UUID):
        query = (
            select(self.repo.model)
            .where(self.repo.model.leaderId == user_id)
        )

        result = await self.session.execute(query)
        return True if result.scalars().first() is not None else False
    async def is_user_organization_moderator(self, user_id: UUID, organization_id: UUID):
        if self.is_user_organization_leader(user_id, organization_id):
            return True

    async def update_organization(self, user_id: UUID, organization_id: UUID):
        ...

    async def get_all_user_organizations(self, user_id: UUID):
        query = (
            select(self.repo.model)
            .join_from(TeamMember, Organization, TeamMember.userId == user_id)
        )
        exec = await self.session.execute(query)
        result = exec.scalars().all()
        return result

    async def create_organization(self, leader_id: int, organization: CreateOrganization):
        try:
            return await self.repo.create(leaderId=leader_id, **organization.model_dump())
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )
        