from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from typing import Optional, List

from app.schema.response.project.read_team_project import ReadProject, ReadTeamProject
from app.schema.response.user.read_user import ReadUser

class ReadTeamMember(BaseModel):
    id: UUID

    user: Optional[ReadUser]
