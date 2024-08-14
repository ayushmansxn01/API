from pydantic import BaseModel,EmailStr,conint
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True



class Post(PostBase):  # Inherit from PostBase
    id: int  # Type annotation
    # created_at: datetime
    owner_id:int
    created_at:datetime
    owner:UserOut
    
    class Config:
        from_attributes = True


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    owner_id: int
    created_at: datetime
    votes: int

    class Config:
        from_attributes = True  # Enable attribute mapping


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


