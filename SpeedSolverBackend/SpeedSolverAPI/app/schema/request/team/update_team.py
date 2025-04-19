from pydantic import BaseModel
from typing import Optional


class UpdateTeam(BaseModel):
    title: str
    description: Optional[str] = None
    leaderId: Optional[str] = None
    organizationId: Optional[str] = None