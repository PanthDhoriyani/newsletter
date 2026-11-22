import httpx
import structlog
from datetime import datetime
from typing import List
from app.config import settings
from app.collectors.base import BaseCollector, RawArticle, normalize_date

log = structlog.get_logger()

class GNewsCollector(BaseCollector):
    def __init__(self):
        self.api_key = settings.gnews_api_key
        self.base_url = "https://gnews.io/api/v4/top-headlines"

    async def collect(self, start_time: datetime, end_time: datetime) -> List[RawArticle]:
        if not self.api_key:
            log.warning("gnews_api_key_missing_skipping")
            return []

        articles: List[RawArticle] = []
        queries = [
            {"country": "in", "category": "general"},
            {"country": "in", "category": "business"},
            {"category": "world"}
        ]

        async with httpx.AsyncClient(timeout=25.0) as client:
            for q in queries:
                try:
                    params = {
                        "apikey": self.api_key,
                        "lang": "en",
                        "max": 10,
                        **q
                    }
                    res = await client.get(self.base_url, params=params)
                    if res.status_code == 200:
                        data = res.json()
                        items = data.get("articles", [])
                        for item in items:
                            url = item.get("url")
                            title = item.get("title")
                            if not url or not title:
                                continue
                            pub_date = normalize_date(item.get("publishedAt"))
                            source_info = item.get("source", {})
                            source_name = source_info.get("name") or "GNews"

                            articles.append(RawArticle(
                                headline=title.strip(),
                                snippet=item.get("description") or "",
                                url=url.strip(),
                                source_name=source_name,
                                source_type="NEWSPAPER",
                                published_at=pub_date,
                                category=q.get("category", "general"),
                                country=q.get("country", "GLOBAL").upper(),
                                language="en"
                            ))
                    else:
                        log.warning("gnews_fetch_status_not_200", status=res.status_code)
                except Exception as e:
                    log.error("gnews_collector_error", error=str(e))

        log.info("gnews_collected", count=len(articles))
        return articles
