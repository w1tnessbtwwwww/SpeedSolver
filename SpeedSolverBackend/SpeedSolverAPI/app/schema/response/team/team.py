from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from typing import Optional, List

from app.schema.response.project.read_team_project import ReadProject
from app.schema.response.user.read_user import ReadUser

class ReadTeam(BaseModel):
    id: str
    title: str
    description: Optional[str]
    created_at: datetime
    team_projects: List[ReadProject]
    members: List[ReadUser]