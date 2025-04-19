


from sqlalchemy import select
from fastapi import HTTPException
from app.database.models.models import Organization, TeamMember
from app.database.repo.organization_repository import OrganizationRepository
from app.schema.request.organization.create_organization import CreateOrganization


class OrganizationService:
    def __init__(self, session):
        self.session = session
        self.repo = OrganizationRepository(session)


    async def get_all_user_organizations(self, user_id: int):
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
        