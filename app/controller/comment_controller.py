import uuid
from app.controller.base import BaseController
from app.db.session import SessionLocal
from app.models.comment import Comment
from app.schemas.comment import CreateComment, UpdateComment


class CommentController(BaseController[Comment, CreateComment, UpdateComment]):
    def get_multi_comments(self, db: SessionLocal, *, post_id: uuid.UUID, skip: int = 0, limit: int = 5000):
        return db.query(Comment).filter(Comment.post_id == post_id).limit(limit).offset(skip).all()


comment = CommentController(Comment)
