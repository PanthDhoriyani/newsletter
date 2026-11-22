import uuid
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.database import Base

class SourceType(str, Enum):
    OFFICIAL = "OFFICIAL"
    PRIMARY = "PRIMARY"
    WIRE = "WIRE"
    NEWSPAPER = "NEWSPAPER"
    GOVERNMENT = "GOVERNMENT"
    INSTITUTION = "INSTITUTION"

class NewsSource(Base):
    __tablename__ = "news_sources"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    article_id = Column(String(36), ForeignKey("articles.id", ondelete="CASCADE"), nullable=False, index=True)
    
    source_name = Column(String(200), nullable=False)
    source_url = Column(String(2000), nullable=False)
    source_type = Column(SqlEnum(SourceType), default=SourceType.NEWSPAPER, nullable=False)
    
    published_at = Column(DateTime, nullable=True)
    collected_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_updated_at = Column(DateTime, nullable=True)
    
    claims_supported = Column(Text, nullable=True)
    snippet = Column(Text, nullable=True)

    # Relationships
    article = relationship("Article", back_populates="sources")
