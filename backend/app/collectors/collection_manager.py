import asyncio
import structlog
from datetime import datetime
from typing import List, Dict, Any
from app.collectors.base import RawArticle
from app.collectors.newsdata_collector import NewsDataCollector
from app.collectors.currents_collector import CurrentsCollector
from app.collectors.gnews_collector import GNewsCollector
from app.collectors.rss_collector import RSSCollector
from app.utils.deduplication import fuzzy_headline_similarity

log = structlog.get_logger()

class CollectionManager:
    def __init__(self):
        self.collectors = [
            RSSCollector(),         # Free, high reliability, no rate limits, immediate
            NewsDataCollector(),    # 200 credits/day
            CurrentsCollector(),    # 250 req/day
            GNewsCollector(),       # 100 req/day
        ]

    async def collect_all(self, start_time: datetime, end_time: datetime) -> List[Dict[str, Any]]:
        log.info("collection_starting", start=start_time.isoformat(), end=end_time.isoformat())

        tasks = [c.collect(start_time, end_time) for c in self.collectors]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        raw_list: List[RawArticle] = []
        for res in results:
            if isinstance(res, list):
                raw_list.extend(res)
            elif isinstance(res, Exception):
                log.error("collector_failed", error=str(res))

        log.info("raw_collected_pre_dedup", count=len(raw_list))

        # 1. Exact URL deduplication
        seen_urls = set()
        deduped_by_url: List[RawArticle] = []
        for item in raw_list:
            if item.url_hash not in seen_urls:
                seen_urls.add(item.url_hash)
                deduped_by_url.append(item)

        # 2. Headline fuzzy deduplication (>85% similarity merged into cluster)
        final_clusters: List[Dict[str, Any]] = []
        used = set()

        for i, a in enumerate(deduped_by_url):
            if i in used:
                continue
            
            cluster_sources = [{
                "source_name": a.source_name,
                "source_url": a.url,
                "source_type": a.source_type,
                "published_at": a.published_at.isoformat(),
                "snippet": a.snippet,
                "headline": a.headline
            }]

            for j, b in enumerate(deduped_by_url[i+1:], i+1):
                if j not in used:
                    if fuzzy_headline_similarity(a.headline, b.headline) >= 0.82:
                        cluster_sources.append({
                            "source_name": b.source_name,
                            "source_url": b.url,
                            "source_type": b.source_type,
                            "published_at": b.published_at.isoformat(),
                            "snippet": b.snippet,
                            "headline": b.headline
                        })
                        used.add(j)

            used.add(i)

            final_clusters.append({
                "headline": a.headline,
                "snippet": a.snippet,
                "url": a.url,
                "category": a.category,
                "country": a.country,
                "published_at": a.published_at.isoformat(),
                "sources": cluster_sources,
                "source_count": len(cluster_sources)
            })

        log.info("collection_completed", clusters_count=len(final_clusters))
        return final_clusters

collection_manager = CollectionManager()
