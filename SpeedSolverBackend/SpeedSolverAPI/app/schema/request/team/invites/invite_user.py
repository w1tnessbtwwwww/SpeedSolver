from pydantic import BaseModel


class InviteUser(BaseModel):
    user_id: str
    team_id: str