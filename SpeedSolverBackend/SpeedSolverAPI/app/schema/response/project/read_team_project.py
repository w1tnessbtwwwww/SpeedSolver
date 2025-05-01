from uuid import UUID
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.schema.response.project.read_project import ReadProject
from app.schema.response.user.read_user import ReadUser

class ReadTeamProject(BaseModel):
    id: UUID

    project: Optional[ReadProject]
    