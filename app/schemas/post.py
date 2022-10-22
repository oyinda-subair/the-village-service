from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.base import PostBase, PostInDBBase


class CreatePost(PostBase):
    ...


class PostResponse(PostInDBBase):
    created_at: datetime
    updated_at: datetime


class UpdatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    updated_at: Optional[datetime] = datetime

    class Config:
        orm_mode = True


class ListPostResponse(BaseModel):
    results: int
    posts: List[PostResponse]


class Post(PostInDBBase):
    ...
