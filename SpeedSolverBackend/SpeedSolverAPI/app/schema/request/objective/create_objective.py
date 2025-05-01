import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class CreateObjective(BaseModel):
    title: Optional[str]
    description: Optional[str]
    parent_objectiveId: Optional[UUID] = None
    deadline_date: Optional[datetime.datetime] = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=7)