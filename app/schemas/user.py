from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr
from app.schemas.base import UserBase, UserInDBBase

from app.schemas.post import *


class UserResponse(UserInDBBase):
    created_at: datetime
    updated_at: datetime
# Properties to receive via API on creation


class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    updated_at: datetime = datetime.now()


# Additional properties stored in DB but not returned by API
class UserInDB(UserInDBBase):
    hashed_password: str


# Additional properties to return via API
class User(UserInDBBase):
    ...


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None


class ShortUserResponse(UserBase):
    email: EmailStr
