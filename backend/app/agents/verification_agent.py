import structlog
from typing import List, Dict, Any

log = structlog.get_logger()

async def verify_clusters(raw_clusters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Verifies claims across independent sources.
    - If official/government source (PIB/RBI): automatically verified as Primary.
    - If >= 2 independent reporting sources: marked VERIFIED.
    - If 1 source: marked SINGLE_SOURCE.
    """
    verified: List[Dict[str, Any]] = []

    for item in raw_clusters:
        sources = item.get("sources", [])
        source_names = {s.get("source_name") for s in sources if s.get("source_name")}
        source_types = {s.get("source_type") for s in sources if s.get("source_type")}

        is_official = ("GOVERNMENT" in source_types or "OFFICIAL" in source_types or "INSTITUTION" in source_types)
        independent_count = len(source_names)

        if is_official:
            verification_status = "OFFICIAL_VERIFIED"
            confidence = 1.0
        elif independent_count >= 2:
            verification_status = "VERIFIED"
            confidence = min(0.95, 0.70 + (independent_count * 0.1))
        else:
            verification_status = "SINGLE_SOURCE"
            confidence = 0.65

        item_copy = dict(item)
        item_copy["verification_status"] = verification_status
        item_copy["confidence"] = confidence
        item_copy["independent_source_count"] = independent_count
        verified.append(item_copy)

    log.info("verification_completed", verified_count=len(verified))
    return verified
