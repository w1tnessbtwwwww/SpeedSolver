from datetime import datetime, timezone
from pydantic import BaseModel
from typing import Optional

class UpdateProfile(BaseModel):
    surname: Optional[str] = None
    name: Optional[str] = None
    patronymic: Optional[str] = None
    about: Optional[str] = None
    birthdate: Optional[datetime] = datetime.now(tz=timezone.utc)