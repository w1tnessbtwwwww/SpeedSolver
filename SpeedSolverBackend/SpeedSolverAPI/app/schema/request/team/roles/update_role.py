import re
from pydantic import BaseModel, field_validator
from sqlalchemy import UUID

from app.exc.bad_color import BadColor



class UpdateRole(BaseModel):
    name: str
    color: str = None

    @field_validator("color")
    def validate_color(cls, value):
        HTML_COLOR_PATTERN = re.compile(r'^#(?:[0-9a-fA-F]{3}){1,2}$')
        if not HTML_COLOR_PATTERN.match(value):
            raise BadColor()
        return value

    