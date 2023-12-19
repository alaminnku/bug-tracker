from models.users import User
from pydantic import BaseModel
from lib.utils import utc_now
from datetime import datetime


class Comment(BaseModel):
    text: str


class CommentCreate(Comment):
    user: User
    created_at: datetime = utc_now


class CommentUpdate(Comment):
    updated_at: datetime = utc_now
