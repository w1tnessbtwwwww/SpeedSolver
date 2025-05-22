import re
from typing import Optional
from pydantic import BaseModel, field_validator
from app.exc.bad_email import BadEmail
from app.schema.request.account.updateprofile import UpdateProfile

class RegisterRequest(BaseModel):
    email: str
    password: str

    profile: Optional[UpdateProfile] = None

    @field_validator("email")
    def validate_email(cls, attr):
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", attr):
            raise BadEmail()
        return attr