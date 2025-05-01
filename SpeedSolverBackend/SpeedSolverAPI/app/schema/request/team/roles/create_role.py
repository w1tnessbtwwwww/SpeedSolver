import re
from typing import Optional
from pydantic import BaseModel, field_validator
from sqlalchemy import UUID

from app.exc.bad_color import BadColor



class CreateRole(BaseModel):
    name: str
    color: Optional[str] = None

    @field_validator("color")
    def validate_color(cls, value):
        HTML_COLOR_PATTERN = re.compile(r'^#(?:[0-9a-fA-F]{3}){1,2}$')
        if not HTML_COLOR_PATTERN.match(value):
            raise BadColor()
        return value

    