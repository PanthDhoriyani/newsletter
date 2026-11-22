import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON, ForeignKey
from app.database import Base

class BreakingNews(Base):
    __tablename__ = "breaking_news"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    headline = Column(String(500), nullable=False)
    summary = Column(Text, nullable=False)
    content = Column(Text, nullable=True)
    importance = Column(String(50), default="CRITICAL")
    
    sources = Column(JSON, default=list)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    published_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    newsletter_id = Column(String(36), ForeignKey("newsletters.id", ondelete="SET NULL"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
