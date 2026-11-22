import uuid
from enum import Enum
from datetime import datetime, date
from sqlalchemy import Column, String, Date, DateTime, Integer, Boolean, JSON, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.database import Base

class NewsletterStatus(str, Enum):
    PENDING = "PENDING"
    GENERATING = "GENERATING"
    PUBLISHED = "PUBLISHED"
    FAILED = "FAILED"

class Newsletter(Base):
    __tablename__ = "newsletters"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    edition_date = Column(Date, unique=True, index=True, nullable=False)
    coverage_start = Column(DateTime, nullable=False)
    coverage_end = Column(DateTime, nullable=False)
    published_at = Column(DateTime, nullable=True)
    status = Column(SqlEnum(NewsletterStatus), default=NewsletterStatus.PENDING, nullable=False)
    
    total_articles = Column(Integer, default=0, nullable=False)
    critical_count = Column(Integer, default=0, nullable=False)
    high_count = Column(Integer, default=0, nullable=False)
    moderate_count = Column(Integer, default=0, nullable=False)
    
    # Mandatory Final Section & Extra Editions
    daily_summary = Column(JSON, nullable=True)
    summary_status = Column(String(50), default="PENDING")
    knowledge_corner = Column(JSON, nullable=True)
    what_to_watch_next = Column(JSON, nullable=True)
    
    is_immutable = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    articles = relationship("Article", back_populates="newsletter", cascade="all, delete-orphan", lazy="selectin")
    generation_logs = relationship("GenerationLog", back_populates="newsletter", cascade="all, delete-orphan")
    edition_progress = relationship("EditionProgress", back_populates="newsletter", uselist=False, cascade="all, delete-orphan")
