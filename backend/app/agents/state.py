from typing import TypedDict, List, Dict, Any, Optional

class NewsState(TypedDict):
    coverage_window: Dict[str, str]  # {"start": ISO, "end": ISO}
    raw_clusters: List[Dict[str, Any]]
    verified_clusters: List[Dict[str, Any]]
    classified_clusters: List[Dict[str, Any]]
    final_articles: List[Dict[str, Any]]
    knowledge_corner: List[Dict[str, Any]]
    what_to_watch_next: List[Dict[str, Any]]
    daily_summary: Optional[Dict[str, Any]]
    edition_id: Optional[str]
    generation_errors: List[str]
    generation_phase: str
    retry_count: int
    is_valid: bool
