from typing import Optional
from pydantic import BaseModel

class UpdateProject(BaseModel):
    for_team: str
    new_title: Optional[str]
    new_description: Optional[str]