import asyncio
import structlog
import xml.etree.ElementTree as ET
import httpx
from datetime import datetime
from typing import List, Tuple
from app.collectors.base import BaseCollector, RawArticle, normalize_date

log = structlog.get_logger()

# Established credible Indian and International RSS feeds
RSS_FEEDS: List[Tuple[str, str, str, str, str]] = [
    # (Source Name, URL, Source Type, Country, Category)
    ("The Hindu", "https://www.thehindu.com/feeder/default.rss", "NEWSPAPER", "IN", "Politics & National"),
    ("The Hindu BusinessLine", "https://www.thehindubusinessline.com/feeder/default.rss", "NEWSPAPER", "IN", "Economy & Finance"),
    ("NDTV Top Stories", "https://feeds.feedburner.com/ndtvnews-top-stories", "NEWSPAPER", "IN", "National News"),
    ("Economic Times", "https://economictimes.indiatimes.com/rssfeedsdefault.cms", "NEWSPAPER", "IN", "Business & Markets"),
    ("ET Markets", "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms", "NEWSPAPER", "IN", "Indian Stock Market"),
    ("LiveMint", "https://www.livemint.com/rss/news", "NEWSPAPER", "IN", "Economy & Finance"),
    ("PIB National", "https://pib.gov.in/RssMain.aspx", "GOVERNMENT", "IN", "Government Announcements"),
    ("BBC World News", "http://feeds.bbci.co.uk/news/world/rss.xml", "WIRE", "GLOBAL", "International Affairs"),
    ("BBC Business", "http://feeds.bbci.co.uk/news/business/rss.xml", "WIRE", "GLOBAL", "Global Economy"),
    ("Al Jazeera", "https://www.aljazeera.com/xml/rss/all.xml", "NEWSPAPER", "GLOBAL", "Geopolitics"),
    ("Google News India Top", "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en", "WIRE", "IN", "National News"),
    ("Google News India Business", "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-IN&gl=IN&ceid=IN:en", "WIRE", "IN", "Economy & Finance"),
    ("Google News India Technology", "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-IN&gl=IN&ceid=IN:en", "WIRE", "IN", "Science & Technology"),
    ("Google News World", "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en", "WIRE", "GLOBAL", "International Affairs")
]

class RSSCollector(BaseCollector):
    async def _fetch_single_feed(self, name: str, url: str, source_type: str, country: str, category: str) -> List[RawArticle]:
        try:
            results = []
            # Try feedparser if available
            try:
                import feedparser
                loop = asyncio.get_event_loop()
                feed = await loop.run_in_executor(None, feedparser.parse, url)
                entries = getattr(feed, "entries", [])
                for entry in entries[:15]:
                    title = entry.get("title")
                    link = entry.get("link")
                    if not title or not link:
                        continue
                    pub_str = entry.get("published") or entry.get("updated")
                    pub_date = normalize_date(pub_str)
                    snippet = entry.get("summary") or entry.get("description") or ""

                    results.append(RawArticle(
                        headline=title.strip(),
                        snippet=snippet.strip(),
                        url=link.strip(),
                        source_name=name,
                        source_type=source_type,
                        published_at=pub_date,
                        category=category,
                        country=country,
                        language="en"
                    ))
                return results
            except ImportError:
                # Built-in xml.etree fallback
                async with httpx.AsyncClient(timeout=15.0, headers={"User-Agent": "Mozilla/5.0"}) as client:
                    res = await client.get(url)
                    if res.status_code == 200:
                        root = ET.fromstring(res.text)
                        for item in root.findall(".//item")[:15]:
                            title = item.findtext("title")
                            link = item.findtext("link")
                            if not title or not link:
                                continue
                            snippet = item.findtext("description") or ""
                            pub_str = item.findtext("pubDate")
                            pub_date = normalize_date(pub_str)

                            results.append(RawArticle(
                                headline=title.strip(),
                                snippet=snippet.strip(),
                                url=link.strip(),
                                source_name=name,
                                source_type=source_type,
                                published_at=pub_date,
                                category=category,
                                country=country,
                                language="en"
                            ))
                return results
        except Exception as e:
            log.warning("rss_feed_fetch_failed", feed=name, error=str(e))
            return []

    async def collect(self, start_time: datetime, end_time: datetime) -> List[RawArticle]:
        tasks = [
            self._fetch_single_feed(name, url, stype, ctry, cat)
            for (name, url, stype, ctry, cat) in RSS_FEEDS
        ]
        
        feed_results = await asyncio.gather(*tasks, return_exceptions=True)
        all_articles: List[RawArticle] = []
        for r in feed_results:
            if isinstance(r, list):
                all_articles.extend(r)

        log.info("rss_collected_total", count=len(all_articles))
        return all_articles
