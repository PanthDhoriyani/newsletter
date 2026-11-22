import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import dateutil.parser

def compute_url_hash(url: str) -> str:
    cleaned = url.split("?")[0].strip().lower()
    return hashlib.md5(cleaned.encode("utf-8")).hexdigest()

def normalize_date(date_val: Optional[str]) -> datetime:
    if not date_val:
        return datetime.utcnow()
    try:
        dt = dateutil.parser.parse(date_val)
        if dt.tzinfo is not None:
            from datetime import timezone
            dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
        return dt
    except Exception:
        return datetime.utcnow()

@dataclass
class RawArticle:
    headline: str
    snippet: str
    url: str
    source_name: str
    source_type: str  # OFFICIAL, PRIMARY, WIRE, NEWSPAPER, GOVERNMENT
    published_at: datetime
    category: str = "general"
    country: str = "IN"
    language: str = "en"
    raw_content: str = ""
    url_hash: str = field(init=False)

    def __post_init__(self):
        self.url_hash = compute_url_hash(self.url)

class BaseCollector(ABC):
    @abstractmethod
    async def collect(self, start_time: datetime, end_time: datetime) -> List[RawArticle]:
        pass
