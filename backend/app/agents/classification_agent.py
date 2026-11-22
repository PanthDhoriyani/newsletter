import asyncio
import structlog
from typing import List, Dict, Any
from app.llm.groq_client import groq_client
from app.llm.prompts.classifier_prompts import CLASSIFIER_SYSTEM, make_classifier_prompt
from app.utils.india_impact import score_india_relevance, has_india_impact
from app.utils.market_impact import detect_market_impact

log = structlog.get_logger()

async def classify_single_cluster(cluster: Dict[str, Any]) -> Dict[str, Any]:
    headline = cluster.get("headline", "")
    snippet = cluster.get("snippet", "")
    sources = cluster.get("sources", [])
    
    sources_text = "\n".join([f"- {s.get('source_name')}: {s.get('snippet', '')}" for s in sources[:3]])
    
    prompt = make_classifier_prompt(headline, snippet, sources_text)
    data = await groq_client.generate_json(CLASSIFIER_SYSTEM, prompt)
    
    # Fallback heuristic if LLM JSON fails or returns empty
    if not data or not data.get("importance"):
        india_score = score_india_relevance(cluster)
        section = "INDIA" if india_score >= 3.0 else "WORLD"
        importance = "HIGH" if india_score >= 6.0 else "MODERATE"
        category = cluster.get("category", "General")
        countries = ["India"] if section == "INDIA" else ["Global"]
        affects_markets = detect_market_impact(cluster)["has_market_impact"]
    else:
        importance = data.get("importance", "MODERATE").upper()
        if importance not in ["CRITICAL", "HIGH", "MODERATE"]:
            importance = "MODERATE"
        section = data.get("section", "INDIA").upper()
        if section not in ["INDIA", "WORLD", "GLOBAL_IMPACT", "TRENDING"]:
            section = "INDIA"
        category = data.get("category", cluster.get("category", "General"))
        countries = data.get("countries", [])
        affects_markets = data.get("affects_markets", False)
        india_score = float(data.get("india_relevance_score", 5.0))

    classified = dict(cluster)
    classified["importance"] = importance
    classified["section"] = section
    classified["category"] = category
    classified["countries"] = countries
    classified["affects_markets"] = affects_markets
    classified["india_relevance_score"] = india_score
    return classified

async def classify_clusters(clusters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Classifies story importance, section, and relevance.
    Uses high-precision domain scoring heuristics with LLM enhancement for top ambiguity cases,
    avoiding rate limit exhaustion (TPM/RPM limits on free tier).
    """
    classified = []
    for c in clusters:
        india_score = score_india_relevance(c)
        sources = c.get("sources", [])
        src_types = {s.get("source_type") for s in sources}
        is_official = ("GOVERNMENT" in src_types or "OFFICIAL" in src_types)
        
        # Section classification
        if india_score >= 4.0:
            section = "INDIA"
        elif any(w in c.get("headline", "").lower() for w in ["market", "sensex", "nifty", "economy", "gdp", "rbi", "inflation", "stock"]):
            section = "BUSINESS"
        elif india_score >= 2.0:
            section = "GLOBAL_IMPACT"
        else:
            section = "WORLD"

        # Importance classification
        if is_official or india_score >= 7.0 or len(sources) >= 3:
            importance = "CRITICAL"
        elif india_score >= 4.0 or len(sources) >= 2:
            importance = "HIGH"
        else:
            importance = "MODERATE"

        market_info = detect_market_impact(c)
        
        item = dict(c)
        item["importance"] = importance
        item["section"] = section
        item["category"] = c.get("category", "General")
        item["countries"] = ["India"] if section == "INDIA" else ["Global"]
        item["affects_markets"] = market_info.get("has_market_impact", False)
        item["india_relevance_score"] = india_score
        classified.append(item)

    log.info("classification_completed", total_classified=len(classified))
    return classified
