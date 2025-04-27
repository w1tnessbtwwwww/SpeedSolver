from typing import Optional
from pydantic import BaseModel
from uuid import UUID

from app.schema.response.user.read_user_profile import ReadUserProfile

class ReadUser(BaseModel):
    id: UUID
    email: str
    is_mail_verified: bool
    profile: Optional[ReadUserProfile] = None