from typing import Optional
from pydantic import BaseModel

class Team(BaseModel):
    id: str
    title: str
    description: Optional[str]
    leader: str