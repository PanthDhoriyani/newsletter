import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class OngoingStory(Base):
    __tablename__ = "ongoing_stories"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    keywords = Column(JSON, default=list)
    status = Column(String(50), default="ACTIVE")  # ACTIVE, RESOLVED, DORMANT
    
    first_seen = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    article_count = Column(Integer, default=1, nullable=False)

    # Relationships
    articles = relationship("Article", back_populates="ongoing_story")
    updates = relationship("StoryUpdate", back_populates="ongoing_story", cascade="all, delete-orphan")

class StoryUpdate(Base):
    __tablename__ = "story_updates"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id = Column(String(36), ForeignKey("ongoing_stories.id", ondelete="CASCADE"), nullable=False)
    article_id = Column(String(36), nullable=False)
    what_changed = Column(Text, nullable=False)
    update_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    ongoing_story = relationship("OngoingStory", back_populates="updates")
