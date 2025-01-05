from pydantic import BaseModel

class ResendCode(BaseModel):
    email: str