from pydantic import BaseModel

class Project(BaseModel):
    name: str
    description: str
    start_date: str
    end_date: str
    members: list[str] = []