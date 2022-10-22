from enum import Enum
from typing import Optional
import uuid
from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    USER = 'user'
    ADMIN = 'admin'


class UserBase(BaseModel):
    first_name: Optional[str]
    surname: Optional[str]
    email: Optional[EmailStr] = None
    is_superuser: bool = False
    role: Optional[UserRole] = UserRole.USER


class UserInDBBase(UserBase):
    id: Optional[uuid.UUID] = None

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: Optional[str] = None
    category: str
    image_url: str
    user_id: Optional[uuid.UUID] = None


class PostInDBBase(PostBase):
    id: uuid.UUID
    user_id: uuid.UUID

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    content: str
    user_id: Optional[uuid.UUID] = None
    post_id: Optional[uuid.UUID] = None


class CommentInDBBase(CommentBase):
    id: uuid.UUID
    user_id: uuid.UUID
    post_id: uuid.UUID

    class Config:
        orm_mode = True
