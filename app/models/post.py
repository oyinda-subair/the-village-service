from sqlalchemy import String, Column, TIMESTAMP, func, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.config import Base

import uuid


class Post(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), index=True, nullable=False)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, default=func.now())

    user = relationship('User', back_populates='posts')
    comments = relationship("Comment", back_populates="post")
