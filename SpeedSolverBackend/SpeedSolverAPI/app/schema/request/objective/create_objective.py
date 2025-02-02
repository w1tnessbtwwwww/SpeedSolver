import datetime
from typing import Optional
from pydantic import BaseModel

class CreateObjective(BaseModel):
    title: Optional[str]
    description: Optional[str]
    depends_on: Optional[str]
    deadline: Optional[datetime.datetime] = datetime.datetime.now() + datetime.timedelta(days=7)