from pydantic import BaseModel
from models.users import UserGeneral
from datetime import datetime
from lib.utils import utc_now


class Project(BaseModel):
    name: str
    description: str
    start_date: str
    end_date: str
    members: list[UserGeneral] = []


class ProjectCreate(Project):
    created_at: datetime = utc_now


class ProjectUpdate(Project):
    updated_at: datetime = utc_now
