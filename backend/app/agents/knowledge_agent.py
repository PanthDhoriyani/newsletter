import structlog
from typing import List, Dict, Any
from app.llm.gemini_client import gemini_client
from app.llm.prompts.writer_prompts import KNOWLEDGE_CORNER_SYSTEM, make_knowledge_prompt

log = structlog.get_logger()

async def generate_knowledge_corner(finalized_articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    summary_text = "\n".join([f"- {a.get('headline')}: {a.get('why_it_matters', '')}" for a in finalized_articles[:12]])
    prompt = make_knowledge_prompt(summary_text)

    data = await gemini_client.generate_json(KNOWLEDGE_CORNER_SYSTEM, prompt)
    if isinstance(data, list) and len(data) >= 2:
        log.info("knowledge_corner_generated", count=len(data))
        return data

    # Clean fallback if LLM response format varied
    fallback = [
        {
            "term": "Sovereign Bond Yields",
            "simple_explanation": "The interest rate that a national government pays when it borrows money from investors. When yields rise, government borrowing costs increase, which influences home loans, corporate debt, and market liquidity.",
            "why_relevant_today": "Central bank interest rate decisions and macroeconomic indicators directly influence bond yields.",
            "related_headline": finalized_articles[0].get("headline") if finalized_articles else "Economic Policy"
        },
        {
            "term": "Current Account Deficit (CAD)",
            "simple_explanation": "A measurement of a country's trade where the value of the goods and services it imports exceeds the value of the products it exports. High oil prices typically widen India's CAD.",
            "why_relevant_today": "Import bills and trade movements discussed in today's business coverage.",
            "related_headline": finalized_articles[1].get("headline") if len(finalized_articles) > 1 else "Trade Data"
        },
        {
            "term": "Quantitative Easing vs Tightening",
            "simple_explanation": "Quantitative easing is when central banks create money to buy bonds and stimulate economic activity; quantitative tightening is the opposite process where liquidity is drained to cool inflation.",
            "why_relevant_today": "Monetary policy trajectory followed by central banks worldwide.",
            "related_headline": finalized_articles[2].get("headline") if len(finalized_articles) > 2 else "Monetary Updates"
        }
    ]
    return fallback
