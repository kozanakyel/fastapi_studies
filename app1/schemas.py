from pydantic import BaseModel, EmailStr
from datetime import datetime

"""
class Post(BaseModel): # pydantic model
    title: str
    content: str
    published: bool = True
"""

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
  
class UserCreate(BaseModel):
    email: EmailStr
    password: str



