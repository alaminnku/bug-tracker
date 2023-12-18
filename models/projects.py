from pydantic import BaseModel
from models.users import User
from datetime import datetime
from lib.utils import utc_now
from enum import Enum


class Severity(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'


class Priority(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'


class Status(str, Enum):
    open = 'open'
    in_progress = 'in_progress'
    closed = 'closed'


class Comment(BaseModel):
    user: User
    text: str
    created_at: datetime = utc_now


class Bug(BaseModel):
    title: str
    description: str
    status: Status
    severity: Severity
    priority: Priority
    reported_by: User
    assigned_to: User
    comments: list[Comment] = []


class BugCreate(Bug):
    created_at: datetime = utc_now


class BugUpdate(Bug):
    updated_at: datetime = utc_now


class Project(BaseModel):
    name: str
    description: str
    start_date: str
    end_date: str
    members: list[User] = []
    bugs: list[Bug] = []


class ProjectCreate(Project):
    created_at: datetime = utc_now


class ProjectUpdate(Project):
    updated_at: datetime = utc_now
