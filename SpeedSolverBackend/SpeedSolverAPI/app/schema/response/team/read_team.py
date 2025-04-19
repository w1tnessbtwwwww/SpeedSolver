from pydantic import BaseModel
from typing import List, Optional



class ReadTeam(BaseModel):
    team: str