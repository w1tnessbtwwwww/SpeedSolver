from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class CreateTeam(BaseModel):
    title: str
    description: Optional[str]
    organizationId: Optional[UUID] = None