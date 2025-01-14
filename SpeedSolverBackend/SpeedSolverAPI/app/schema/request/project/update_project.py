from typing import Optional
from pydantic import BaseModel

class UpdateProject(BaseModel):
    new_title: Optional[str]
    new_description: Optional[str]