from pydantic import BaseModel, EmailStr
from lib.utils import utc_now
from datetime import datetime


class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    created_at: datetime = utc_now


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    updated_at: datetime = utc_now


class UserGeneral(BaseModel):
    id: str
    name: str
    email: EmailStr
