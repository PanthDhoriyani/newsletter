from typing import Dict, Any

MARKET_KEYWORDS = {
    "nifty": "Nifty 50 Index",
    "sensex": "BSE Sensex",
    "rupee": "Indian Rupee (INR)",
    "inr": "Indian Rupee (INR)",
    "crude oil": "Crude Oil Prices & Import Bill",
    "gold": "Gold & Precious Metals",
    "export": "Indian Merchandise & Services Exports",
    "import": "Indian Import Bill & CAD",
    "interest rate": "RBI Monetary Policy & Capital Flows",
    "federal reserve": "US Fed Rates & FII Flows",
    "inflation": "Domestic Inflation & Consumer Prices"
}

def detect_market_impact(article: Dict[str, Any]) -> Dict[str, Any]:
    text = (
        str(article.get("headline", "")) + " " +
        str(article.get("snippet", "")) + " " +
        str(article.get("content", ""))
    ).lower()

    affected = []
    for keyword, label in MARKET_KEYWORDS.items():
        if keyword in text:
            affected.append(label)

    return {
        "has_market_impact": len(affected) > 0,
        "affected_markets": list(set(affected))
    }
