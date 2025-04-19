from typing import Optional
from pydantic import BaseModel


class CreateOrganization(BaseModel):
    title: str
    description: Optional[str]