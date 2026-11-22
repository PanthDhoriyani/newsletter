from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from app.models.reading_progress import ReadStatus, EditionStatus

class ArticleStatusUpdate(BaseModel):
    status: ReadStatus
    notes: Optional[str] = None

class EditionStatusUpdate(BaseModel):
    status: EditionStatus

class ReadingProgressResponse(BaseModel):
    total_editions: int
    completed_editions: int
    in_progress_editions: int
    unread_editions: int
    total_articles: int
    read_articles: int
    saved_articles: int
    unread_critical: int
    unread_high: int

class CatchupView(BaseModel):
    missed_editions_count: int
    total_unread_articles: int
    critical_unread_count: int
    high_unread_count: int
    missed_editions: List[Dict[str, Any]] = []
    prioritized_articles: List[Dict[str, Any]] = []
