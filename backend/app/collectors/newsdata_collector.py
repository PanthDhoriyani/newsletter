import httpx
import structlog
from datetime import datetime
from typing import List
from app.config import settings
from app.collectors.base import BaseCollector, RawArticle, normalize_date

log = structlog.get_logger()

class NewsDataCollector(BaseCollector):
    def __init__(self):
        self.api_key = settings.newsdata_api_key
        self.base_url = "https://newsdata.io/api/1/news"

    async def collect(self, start_time: datetime, end_time: datetime) -> List[RawArticle]:
        if not self.api_key:
            log.warning("newsdata_api_key_missing_skipping")
            return []

        articles: List[RawArticle] = []
        
        # We query India top news and global news
        queries = [
            {"country": "in", "category": "top,business,politics,technology"},
            {"language": "en", "category": "world,business,technology"}
        ]

        async with httpx.AsyncClient(timeout=25.0) as client:
            for q in queries:
                params = {
                    "apikey": self.api_key,
                    "language": "en",
                    **q
                }
                try:
                    res = await client.get(self.base_url, params=params)
                    if res.status_code == 200:
                        data = res.json()
                        results = data.get("results", [])
                        for item in results:
                            link = item.get("link")
                            title = item.get("title")
                            if not link or not title:
                                continue
                            pub_date = normalize_date(item.get("pubDate"))
                            
                            category_list = item.get("category", ["general"])
                            category = category_list[0] if category_list else "general"
                            
                            country_list = item.get("country", ["in"])
                            country = country_list[0].upper() if country_list else "IN"

                            articles.append(RawArticle(
                                headline=title.strip(),
                                snippet=item.get("description") or "",
                                url=link.strip(),
                                source_name=item.get("source_id") or "NewsData",
                                source_type="NEWSPAPER",
                                published_at=pub_date,
                                category=category,
                                country=country,
                                language="en"
                            ))
                    else:
                        log.warning("newsdata_fetch_status_not_200", status=res.status_code, text=res.text[:100])
                except Exception as e:
                    log.error("newsdata_collector_error", error=str(e))

        log.info("newsdata_collected", count=len(articles))
        return articles
