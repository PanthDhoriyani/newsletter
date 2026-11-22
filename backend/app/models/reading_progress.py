import uuid
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Boolean, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.database import Base

class ReadStatus(str, Enum):
    UNREAD = "UNREAD"
    READ = "READ"
    SAVED_FOR_LATER = "SAVED_FOR_LATER"
    SKIPPED = "SKIPPED"

class EditionStatus(str, Enum):
    UNREAD = "UNREAD"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    SKIPPED = "SKIPPED"

class ReadingProgress(Base):
    __tablename__ = "reading_progress"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    article_id = Column(String(36), ForeignKey("articles.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    status = Column(SqlEnum(ReadStatus), default=ReadStatus.UNREAD, nullable=False)
    last_read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    article = relationship("Article", back_populates="reading_progress")

class EditionProgress(Base):
    __tablename__ = "edition_progress"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    newsletter_id = Column(String(36), ForeignKey("newsletters.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    status = Column(SqlEnum(EditionStatus), default=EditionStatus.UNREAD, nullable=False)
    articles_read = Column(Integer, default=0, nullable=False)
    total_articles = Column(Integer, default=0, nullable=False)
    summary_read = Column(Boolean, default=False, nullable=False)
    last_read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    newsletter = relationship("Newsletter", back_populates="edition_progress")
