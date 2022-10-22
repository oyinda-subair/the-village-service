from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
import uuid

from app.schemas.base import CommentBase, CommentInDBBase, UserInDBBase


class FilteredUserResponse(UserInDBBase):
    ...


class CreateComment(CommentBase):
    ...


class UpdateComment(CommentBase):
    content: Optional[str] = None

    class Config:
        orm_mode = True


class CommentResponse(CommentInDBBase):
    user: FilteredUserResponse
    created_at: datetime
    updated_at: datetime


class ListCommentResponse(BaseModel):
    results: int
    comments: List[CommentResponse]


class Comment(CommentInDBBase):
    ...
