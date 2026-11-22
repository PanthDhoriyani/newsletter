import uuid
from datetime import datetime
from sqlalchemy import Column, String, Date, DateTime, Boolean, JSON, Integer
from app.database import Base

class WeeklyReview(Base):
    __tablename__ = "weekly_reviews"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    week_start = Column(Date, nullable=False)
    week_end = Column(Date, nullable=False)
    
    content = Column(JSON, nullable=False)
    weekly_summary = Column(JSON, nullable=False)
    
    published_at = Column(DateTime, nullable=True)
    status = Column(String(50), default="PENDING")
    is_immutable = Column(Boolean, default=False, nullable=False)
    total_editions = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
