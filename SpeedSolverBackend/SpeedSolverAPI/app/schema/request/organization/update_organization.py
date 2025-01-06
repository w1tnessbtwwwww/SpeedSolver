from pydantic import BaseModel
from typing import Optional


class UpdateOrganization(BaseModel):
    organizationId: str
    new_title: Optional[str] = None
    new_description: Optional[str] = None
