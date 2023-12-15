from pydantic import BaseModel
from models.users import UserGeneral

class Project(BaseModel):
    name: str
    description: str
    start_date: str
    end_date: str
    members: list[UserGeneral] = []
