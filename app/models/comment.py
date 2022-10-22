from sqlalchemy import String, Column, TIMESTAMP, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.config import Base

import uuid


class Comment(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), index=True, nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey('post.id', ondelete='CASCADE'), index=True, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, default=func.now())

    user = relationship('User', back_populates="comments")
    post = relationship('Post', back_populates='comments')
