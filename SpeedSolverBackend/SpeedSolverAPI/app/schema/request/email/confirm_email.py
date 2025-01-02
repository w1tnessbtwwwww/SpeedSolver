from pydantic import BaseModel

class EmailConfirmation(BaseModel):
    code: str
    email: str