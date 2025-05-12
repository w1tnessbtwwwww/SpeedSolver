from uuid import UUID
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.schema.response.user.read_user import ReadUser

class ReadProject(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    created_at: datetime

    creator: Optional[ReadUser]
    