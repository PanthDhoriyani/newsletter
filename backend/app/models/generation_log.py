import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Float, Integer, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class GenerationLog(Base):
    __tablename__ = "generation_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    newsletter_id = Column(String(36), ForeignKey("newsletters.id", ondelete="CASCADE"), nullable=True, index=True)
    phase = Column(String(100), nullable=False)  # COLLECTION, VERIFICATION, DEDUP, WRITING, SUMMARY, PUBLISH
    status = Column(String(50), nullable=False) # SUCCESS, FAILED, RETRYING, RUNNING
    error_message = Column(Text, nullable=True)
    duration_seconds = Column(Float, nullable=True)
    articles_processed = Column(Integer, nullable=True)
    metadata_info = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    newsletter = relationship("Newsletter", back_populates="generation_logs")
