import uuid
from sqlalchemy.orm import Session

from app.controller.base import BaseController
from app.models.post import Post
from app.schemas.post import CreatePost, UpdatePost
from sqlalchemy import and_


class PostController(BaseController[Post, CreatePost, UpdatePost]):

    def get_user_post_by_id(self, db: Session, *, post_id: uuid.UUID, user_id: uuid.UUID):
        return db.query(Post).filter(and_(Post.id == post_id, Post.user_id == user_id)).first()

    def get_multi_posts(self, db: Session, *, user_id: uuid.UUID, skip: int = 0, limit: int = 5000):
        return db.query(Post).filter(Post.user_id == user_id).limit(limit).offset(skip).all()

    def search_by_title(self, db: Session, *, title: str, skip: int = 0, limit: int = 5000):
        return db.query(Post).group_by(Post.id).filter(
            Post.title.contains(title)).limit(limit).offset(skip).all()


post = PostController(Post)
