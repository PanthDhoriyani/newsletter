from typing import List, Optional, Any, Dict
from pydantic import BaseModel
from datetime import datetime
from app.models.article import ArticleImportance

class NewsSourceRead(BaseModel):
    id: str
    source_name: str
    source_url: str
    source_type: str
    published_at: Optional[datetime] = None
    snippet: Optional[str] = None

    class Config:
        from_attributes = True

class ArticleListItem(BaseModel):
    id: str
    newsletter_id: str
    headline: str
    section: str
    category: str
    importance: ArticleImportance
    introduction: Optional[str] = None
    published_at: datetime
    read_status: Optional[str] = "UNREAD"
    source_count: Optional[int] = 1

    class Config:
        from_attributes = True

class ArticleRead(BaseModel):
    id: str
    newsletter_id: str
    headline: str
    section: str
    category: str
    importance: ArticleImportance
    introduction: Optional[str] = None
    content: str
    background_context: Optional[str] = None
    key_developments: Optional[str] = None
    why_it_matters: Optional[str] = None
    india_impact: Optional[str] = None
    economic_industry_impact: Optional[str] = None
    what_happens_next: Optional[str] = None
    tags: List[str] = []
    countries: List[str] = []
    market_impact: Optional[Dict[str, Any]] = None
    published_at: datetime
    is_ongoing_story: bool = False
    ongoing_story_id: Optional[str] = None
    sources: List[NewsSourceRead] = []
    read_status: Optional[str] = "UNREAD"

    class Config:
        from_attributes = True

class SearchResult(BaseModel):
    article: ArticleRead
    matched_snippet: str
