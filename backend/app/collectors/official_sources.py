import structlog
from datetime import datetime
from typing import List
from app.collectors.base import BaseCollector, RawArticle

log = structlog.get_logger()

class OfficialSourcesCollector(BaseCollector):
    """Fetches high-integrity primary institutional releases (PIB, RBI, UN, IMF)."""

    async def collect(self, start_time: datetime, end_time: datetime) -> List[RawArticle]:
        # Handled primarily via PIB/RBI RSS feeds and official channels in RSSCollector
        log.info("official_sources_collector_active")
        return []
