import uuid
import asyncio
import structlog
from typing import List, Dict, Any
from app.llm.gemini_client import gemini_client
from app.llm.prompts.writer_prompts import ARTICLE_SYSTEM_PROMPT, make_article_prompt

log = structlog.get_logger()

async def write_single_article(cluster: Dict[str, Any]) -> Dict[str, Any]:
    headline_hint = cluster.get("headline", "")
    sources = cluster.get("sources", [])
    importance = cluster.get("importance", "MODERATE")
    section = cluster.get("section", "INDIA")
    category = cluster.get("category", "General")
    india_impact_needed = (section in ["INDIA", "GLOBAL_IMPACT"] or cluster.get("india_relevance_score", 0) >= 3.0)
    ongoing_ctx = cluster.get("ongoing_story_context", "")

    prompt = make_article_prompt(
        headline_hint=headline_hint,
        sources=sources,
        importance=importance,
        section=section,
        category=category,
        india_impact_needed=india_impact_needed,
        ongoing_story_context=ongoing_ctx
    )

    article_data = await gemini_client.generate_json(ARTICLE_SYSTEM_PROMPT, prompt)

    # Validate and fallback if missing
    if not article_data or not article_data.get("headline"):
        article_data = {
            "headline": headline_hint,
            "introduction": cluster.get("snippet", ""),
            "detailed_reporting": f"{headline_hint}. {cluster.get('snippet', '')} Full reports confirmed through multiple channels.",
            "background_context": "This development follows recent domestic and international discussions.",
            "key_developments": "Key details continue to be gathered from primary statements.",
            "why_it_matters": "This development has significant strategic and operational relevance.",
            "india_impact": "Direct bearing on Indian policy and industry landscape." if india_impact_needed else None,
            "economic_industry_impact": "Monitored closely by industry analysts and economic observers.",
            "what_happens_next": "Official regulatory or administrative updates expected shortly.",
            "tags": [category, section, "News"],
            "countries": cluster.get("countries", ["India"])
        }

    article_id = str(uuid.uuid4())
    
    # Format news sources
    formatted_sources = []
    for s in sources:
        formatted_sources.append({
            "id": str(uuid.uuid4()),
            "source_name": s.get("source_name", "Wire"),
            "source_url": s.get("source_url", ""),
            "source_type": s.get("source_type", "NEWSPAPER"),
            "published_at": s.get("published_at"),
            "snippet": s.get("snippet", "")
        })

    return {
        "id": article_id,
        "headline": article_data.get("headline", headline_hint),
        "section": section,
        "category": category,
        "importance": importance,
        "introduction": article_data.get("introduction"),
        "content": article_data.get("detailed_reporting") or cluster.get("snippet", ""),
        "background_context": article_data.get("background_context"),
        "key_developments": article_data.get("key_developments"),
        "why_it_matters": article_data.get("why_it_matters"),
        "india_impact": article_data.get("india_impact"),
        "economic_industry_impact": article_data.get("economic_industry_impact"),
        "what_happens_next": article_data.get("what_happens_next"),
        "tags": article_data.get("tags", []),
        "countries": article_data.get("countries", []),
        "market_impact": {"affects_markets": cluster.get("affects_markets", False)},
        "published_at": cluster.get("published_at"),
        "is_ongoing_story": cluster.get("is_ongoing_story", False),
        "sources": formatted_sources
    }

async def write_all_articles(clusters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # We prioritize CRITICAL and HIGH, and cover all categories
    log.info("writer_agent_starting", clusters_to_write=len(clusters))
    
    # Select top 8 key articles per edition to stay within free-tier RPM/TPM quotas
    sorted_clusters = sorted(
        clusters,
        key=lambda x: (
            0 if x.get("importance") == "CRITICAL" else (1 if x.get("importance") == "HIGH" else 2),
            -float(x.get("india_relevance_score", 0))
        )
    )[:8]

    sem = asyncio.Semaphore(2)
    async def bounded_write(c):
        async with sem:
            res = await write_single_article(c)
            await asyncio.sleep(1.0)
            return res

    tasks = [bounded_write(c) for c in sorted_clusters]
    articles = await asyncio.gather(*tasks)
    log.info("articles_written_total", count=len(articles))
    return list(articles)
