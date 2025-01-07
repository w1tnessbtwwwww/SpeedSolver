from pydantic import BaseModel
from typing import Optional


class UpdateTeam(BaseModel):
    new_name: str
    new_description: Optional[str]
    new_leader_id: Optional[str]
    new_organization_id: Optional[str]