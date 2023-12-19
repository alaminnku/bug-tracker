from models.users import User
from pydantic import BaseModel
from lib.utils import utc_now
from datetime import datetime


class Comment(BaseModel):
    user: User
    text: str
    created_at: datetime = utc_now
