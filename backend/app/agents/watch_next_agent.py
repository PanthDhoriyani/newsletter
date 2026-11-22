import structlog
from typing import List, Dict, Any
from app.llm.groq_client import groq_client
from app.llm.prompts.writer_prompts import WATCH_NEXT_SYSTEM, make_watch_next_prompt

log = structlog.get_logger()

async def generate_what_to_watch_next(finalized_articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    summary_text = "\n".join([f"- [{a.get('category')}]: {a.get('headline')} (Next: {a.get('what_happens_next', '')})" for a in finalized_articles[:12]])
    prompt = make_watch_next_prompt(summary_text)

    data = await groq_client.generate_json(WATCH_NEXT_SYSTEM, prompt)
    if isinstance(data, list) and len(data) >= 2:
        log.info("watch_next_items_extracted", count=len(data))
        return data

    fallback = [
        {
            "event": "RBI Monetary Policy Committee Review & Inflation Projections",
            "expected_date": "Next Scheduled Meeting",
            "category": "Economy & Finance",
            "why_important": "Guides repo rates, liquidity in Indian banking system, and home loan EMIs."
        },
        {
            "event": "Union Parliament Session & Key Legislative Bills",
            "expected_date": "Upcoming Parliamentary Sitting",
            "category": "Politics & Legislation",
            "why_important": "Debates on regulatory frameworks, budget allocations, and tax legislation."
        },
        {
            "event": "US Federal Reserve FOMC Interest Rate Decision",
            "expected_date": "Scheduled Fed Calendar",
            "category": "Global Markets",
            "why_important": "Affects foreign institutional investor (FII) flows into Indian stock markets."
        }
    ]
    return fallback
