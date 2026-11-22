import httpx
import structlog
from datetime import datetime
from typing import List
from app.config import settings
from app.collectors.base import BaseCollector, RawArticle, normalize_date

log = structlog.get_logger()

class CurrentsCollector(BaseCollector):
    def __init__(self):
        self.api_key = settings.currents_api_key
        self.base_url = "https://api.currentsapi.services/v1/latest-news"

    async def collect(self, start_time: datetime, end_time: datetime) -> List[RawArticle]:
        if not self.api_key:
            log.warning("currents_api_key_missing_skipping")
            return []

        articles: List[RawArticle] = []

        params_list = [
            {"country": "IN", "language": "en"},
            {"language": "en", "category": "world"}
        ]

        async with httpx.AsyncClient(timeout=25.0) as client:
            for p in params_list:
                try:
                    res = await client.get(self.base_url, params={"apiKey": self.api_key, **p})
                    if res.status_code == 200:
                        data = res.json()
                        news_items = data.get("news", [])
                        for item in news_items:
                            url = item.get("url")
                            title = item.get("title")
                            if not url or not title:
                                continue
                            pub_date = normalize_date(item.get("published"))

                            category_list = item.get("category", ["general"])
                            category = category_list[0] if category_list else "general"

                            articles.append(RawArticle(
                                headline=title.strip(),
                                snippet=item.get("description") or "",
                                url=url.strip(),
                                source_name=item.get("author") or "Currents News",
                                source_type="WIRE",
                                published_at=pub_date,
                                category=category,
                                country=p.get("country", "GLOBAL"),
                                language="en"
                            ))
                    else:
                        log.warning("currents_fetch_status_not_200", status=res.status_code)
                except Exception as e:
                    log.error("currents_collector_error", error=str(e))

        log.info("currents_collected", count=len(articles))
        return articles
