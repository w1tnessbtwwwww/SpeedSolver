from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

class CreateProject(BaseModel):
    title: str
    description: Optional[str] = None
    auto_invite: List[UUID]