import datetime
from uuid import UUID
from pydantic import BaseModel

from app.schema.response.project.read_project import ReadProject


class ReadProjectInvitation(BaseModel):
    id: UUID
    created_at: datetime.datetime
    project: ReadProject