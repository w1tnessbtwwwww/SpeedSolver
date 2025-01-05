from pydantic import BaseModel
from typing import Optional


class UpdateOrganization(BaseModel):
    organizationId: str
    title: Optional[str] = None
    description: Optional[str] = None