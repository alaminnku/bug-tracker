from pydantic import BaseModel
from models.users import User
from datetime import datetime
from lib.utils import utc_now
from enum import Enum


class Project(BaseModel):
    name: str
    description: str
    start_date: str
    end_date: str
    members: list[User] = []


class ProjectCreate(Project):
    created_at: datetime = utc_now


class ProjectUpdate(Project):
    updated_at: datetime = utc_now
