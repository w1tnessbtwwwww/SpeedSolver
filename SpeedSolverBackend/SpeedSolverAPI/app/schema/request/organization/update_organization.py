from uuid import UUID
from pydantic import BaseModel
from typing import Optional


class UpdateOrganization(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    leaderId: Optional[UUID] = None
