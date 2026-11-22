from typing import Dict, Any

INDIA_IMPACT_TRIGGERS = [
    "india", "indian", "rupee", "inr", "nifty", "sensex", "bse", "nse",
    "rbi", "sebi", "modi", "new delhi", "mumbai", "export", "import",
    "crude oil", "opec", "us dollar", "fed", "federal reserve", "china border",
    "pakistan", "trade war", "tariff", "supply chain", "remittance", "it sector",
    "h-1b", "pharmaceutical", "semiconductor", "defence", "isro", "quad", "brics"
]

def score_india_relevance(article: Dict[str, Any]) -> float:
    text = (
        str(article.get("headline", "")) + " " +
        str(article.get("snippet", "")) + " " +
        str(article.get("content", ""))
    ).lower()

    hits = sum(1 for trigger in INDIA_IMPACT_TRIGGERS if trigger in text)
    country = str(article.get("country", "")).lower()
    
    score = hits * 1.5
    if country in ["in", "india"]:
        score += 5.0
        
    return min(10.0, round(score, 1))

def has_india_impact(article: Dict[str, Any], threshold: float = 2.0) -> bool:
    return score_india_relevance(article) >= threshold
