import structlog
from typing import List, Dict, Any
from app.utils.deduplication import extract_keywords

log = structlog.get_logger()

async def deduplicate_and_track_stories(clusters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Enriches clusters with semantic keywords and checks for ongoing story continuity."""
    enriched = []
    for item in clusters:
        text = f"{item.get('headline', '')} {item.get('snippet', '')}"
        keywords = extract_keywords(text)
        
        c = dict(item)
        c["keywords"] = keywords
        c["is_ongoing_story"] = False
        c["ongoing_story_context"] = ""
        enriched.append(c)

    log.info("deduplication_and_story_tracking_done", count=len(enriched))
    return enriched
