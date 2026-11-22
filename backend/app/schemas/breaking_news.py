from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class BreakingNewsCreate(BaseModel):
    headline: str
    summary: str
    content: Optional[str] = None
    importance: str = "CRITICAL"
    sources: List[Dict[str, Any]] = []

class BreakingNewsRead(BaseModel):
    id: str
    headline: str
    summary: str
    content: Optional[str] = None
    importance: str
    sources: List[Dict[str, Any]] = []
    is_verified: bool
    published_at: datetime
    is_active: bool

    class Config:
        from_attributes = True
