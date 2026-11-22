import uuid
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.database import Base

class ArticleImportance(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MODERATE = "MODERATE"

class Article(Base):
    __tablename__ = "articles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    newsletter_id = Column(String(36), ForeignKey("newsletters.id", ondelete="CASCADE"), nullable=False, index=True)
    
    headline = Column(String(500), nullable=False)
    section = Column(String(100), nullable=False)  # INDIA, WORLD, GLOBAL_IMPACT, TRENDING
    category = Column(String(100), nullable=False) # Politics, Economy, Science, Tech, Sports, etc.
    importance = Column(SqlEnum(ArticleImportance), default=ArticleImportance.MODERATE, nullable=False, index=True)
    
    introduction = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    background_context = Column(Text, nullable=True)
    key_developments = Column(Text, nullable=True)
    why_it_matters = Column(Text, nullable=True)
    india_impact = Column(Text, nullable=True)
    economic_industry_impact = Column(Text, nullable=True)
    what_happens_next = Column(Text, nullable=True)
    
    tags = Column(JSON, default=list)
    countries = Column(JSON, default=list)
    market_impact = Column(JSON, nullable=True)
    
    published_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    is_ongoing_story = Column(Boolean, default=False)
    ongoing_story_id = Column(String(36), ForeignKey("ongoing_stories.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    newsletter = relationship("Newsletter", back_populates="articles")
    sources = relationship("NewsSource", back_populates="article", cascade="all, delete-orphan", lazy="selectin")
    ongoing_story = relationship("OngoingStory", back_populates="articles")
    reading_progress = relationship("ReadingProgress", back_populates="article", uselist=False, cascade="all, delete-orphan")
    saved_article = relationship("SavedArticle", back_populates="article", uselist=False, cascade="all, delete-orphan")
