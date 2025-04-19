from pydantic import BaseModel
from typing import Optional
class AccessToken(BaseModel):
    access_token: str
    refresh_token: Optional[str]
    token_type: str = "Bearer"