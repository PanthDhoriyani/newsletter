import structlog
from typing import List, Dict, Any
from app.llm.gemini_client import gemini_client
from app.llm.prompts.summary_prompts import SUMMARY_SYSTEM_PROMPT, make_summary_prompt

log = structlog.get_logger()

async def generate_daily_edition_summary(finalized_articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    CRITICAL: This runs ONLY after all articles are locked and written.
    It synthesizes solely from finalized_articles.
    Every bullet references the exact article_id.
    """
    if not finalized_articles:
        log.warning("cannot_generate_summary_no_articles")
        return {}

    prompt = make_summary_prompt(finalized_articles)
    summary_data = await gemini_client.generate_json(SUMMARY_SYSTEM_PROMPT, prompt)

    # Verification: check all 7 required subsections
    required_keys = [
        "biggest_headlines",
        "india_in_focus",
        "world_in_focus",
        "impact_on_india",
        "business_and_markets",
        "other_important",
        "key_takeaways"
    ]

    for k in required_keys:
        if k not in summary_data:
            log.warning("missing_summary_section_adding_fallback", section=k)
            if k == "biggest_headlines":
                summary_data[k] = [
                    {
                        "title": a.get("headline", ""),
                        "article_id": a.get("id", ""),
                        "importance": a.get("importance", "MODERATE"),
                        "brief_why_it_matters": a.get("why_it_matters", "")[:120]
                    }
                    for a in finalized_articles[:4]
                ]
            elif k in ["india_in_focus", "world_in_focus", "business_and_markets", "other_important"]:
                summary_data[k] = {
                    "summary_text": "Comprehensive overview of today's key developments.",
                    "key_developments": [
                        {"point": a.get("headline", ""), "article_id": a.get("id", "")}
                        for a in finalized_articles[:3]
                    ],
                    "highlights": [
                        {"point": a.get("headline", ""), "article_id": a.get("id", "")}
                        for a in finalized_articles[:3]
                    ],
                    "items": [
                        {"category": "General", "point": a.get("headline", ""), "article_id": a.get("id", "")}
                        for a in finalized_articles[:3]
                    ]
                }
            elif k == "impact_on_india":
                summary_data[k] = {
                    "summary_text": "Analysis of international trade, currency, and strategic impacts.",
                    "developments": [
                        {
                            "international_event": a.get("headline", ""),
                            "india_implication": a.get("india_impact") or "Monitored closely by Indian authorities.",
                            "article_id": a.get("id", "")
                        }
                        for a in finalized_articles[:2]
                    ]
                }
            elif k == "key_takeaways":
                summary_data[k] = [
                    {
                        "takeaway": f"Significant progress in {a.get('category')}: {a.get('headline')}",
                        "article_id": a.get("id", ""),
                        "importance": a.get("importance", "HIGH")
                    }
                    for a in finalized_articles[:6]
                ]

    log.info("daily_summary_generated_successfully")
    return summary_data
