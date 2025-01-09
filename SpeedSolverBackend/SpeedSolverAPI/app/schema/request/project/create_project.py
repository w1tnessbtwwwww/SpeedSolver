from pydantic import BaseModel

class CreateProject(BaseModel):
    for_team: str
    title: str
    description: str