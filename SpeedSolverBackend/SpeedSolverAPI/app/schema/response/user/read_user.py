from datetime import date
from typing import Optional
from pydantic import BaseModel, field_validator
from app.cfg.settings import settings
class ReadUserProfile(BaseModel):
    surname: Optional[str]
    name: Optional[str]
    patronymic: Optional[str]
    about: Optional[str]
    birthdate: Optional[date]
    avatar_path: Optional[str]

    @field_validator("avatar_path")
    def prepare_path(cls, value):
        return f"{settings.SPEEDSOLVER_BASE_URL}/{value}" if value is not None else None