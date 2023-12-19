from enum import Enum
from pydantic import BaseModel
from models.users import User
from models.comments import Comment
from datetime import datetime
from lib.utils import utc_now


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
