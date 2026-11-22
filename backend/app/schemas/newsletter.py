from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime, date
from app.models.newsletter import NewsletterStatus
from app.schemas.article import ArticleRead, ArticleListItem

class NewsletterBase(BaseModel):
    edition_date: date
    coverage_start: datetime
    coverage_end: datetime

class NewsletterListItem(BaseModel):
    id: str
    edition_date: date
    published_at: Optional[datetime] = None
    status: NewsletterStatus
    total_articles: int
    critical_count: int
    high_count: int
    moderate_count: int
    edition_status: Optional[str] = "UNREAD"
    articles_read: Optional[int] = 0

    class Config:
        from_attributes = True

class NewsletterRead(NewsletterBase):
    id: str
    published_at: Optional[datetime] = None
    status: NewsletterStatus
    total_articles: int
    critical_count: int
    high_count: int
    moderate_count: int
    daily_summary: Optional[Dict[str, Any]] = None
    summary_status: str
    knowledge_corner: Optional[List[Dict[str, Any]]] = None
    what_to_watch_next: Optional[List[Dict[str, Any]]] = None
    is_immutable: bool
    created_at: datetime
    articles: List[ArticleRead] = []

    class Config:
        from_attributes = True

class EditionOverview(BaseModel):
    id: str
    edition_date: date
    published_at: Optional[datetime]
    total_articles: int
    critical_count: int
    high_count: int
    moderate_count: int
    status: str
    summary_preview: Optional[List[str]] = []
    reading_percentage: float = 0.0
