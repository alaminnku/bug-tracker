from pydantic import BaseModel, EmailStr

class User(BaseModel): 
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: str
    email: EmailStr


class UserGeneral(UserUpdate):
    id: str