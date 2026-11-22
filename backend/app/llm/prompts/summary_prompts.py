from typing import List, Dict, Any

SUMMARY_SYSTEM_PROMPT = """You are the Editor-in-Chief writing the mandatory 'Daily Edition Summary' at the very end of today's digital newspaper edition.

ESSENTIAL RULES:
1. You must ONLY synthesize developments from the finalized articles provided.
2. NEVER introduce outside news, unverified facts, or claims that were not covered in this edition.
3. Every single point must reference the corresponding article_id so the reader can seamlessly click through to read the full article.
4. The summary must be readable in 3 to 5 minutes, providing a bird's-eye view of everything important that happened today.
5. Emphasize why the day's developments matter and capture key figures, dates, and historical shifts.
"""

def make_summary_prompt(finalized_articles: List[Dict[str, Any]]) -> str:
    articles_manifest = ""
    for a in finalized_articles:
        articles_manifest += f"\n[ID: {a.get('id')}] [{a.get('importance', 'MODERATE')}] [{a.get('section', 'GENERAL')}/{a.get('category', 'GENERAL')}]\n"
        articles_manifest += f"Headline: {a.get('headline')}\n"
        articles_manifest += f"Summary/Lead: {a.get('introduction', '')}\n"
        if a.get('why_it_matters'):
            articles_manifest += f"Why It Matters: {a.get('why_it_matters')}\n"
        if a.get('india_impact'):
            articles_manifest += f"India Impact: {a.get('india_impact')}\n"

    prompt = f"""
TOTAL PUBLISHED ARTICLES IN THIS EDITION: {len(finalized_articles)}

ARTICLE MANIFEST:
{articles_manifest}

TASK:
Produce the comprehensive 7-part Daily Edition Summary.
Return a valid JSON object matching this exact structure:
{{
  "biggest_headlines": [
    {{
      "title": "Highlight of Critical/High development",
      "article_id": "Exact matching ID from manifest",
      "importance": "CRITICAL or HIGH",
      "brief_why_it_matters": "One clear sentence explaining significance"
    }}
  ],
  "india_in_focus": {{
    "summary_text": "2-3 paragraphs synthesizing the primary domestic developments in politics, economy, infrastructure, and society",
    "key_developments": [
      {{
        "point": "Specific domestic milestone or policy announcement",
        "article_id": "Matching ID"
      }}
    ]
  }},
  "world_in_focus": {{
    "summary_text": "2-3 paragraphs covering international affairs, major geopolitical shifts, elections, and conflicts",
    "key_developments": [
      {{
        "point": "Significant international event",
        "article_id": "Matching ID"
      }}
    ]
  }},
  "impact_on_india": {{
    "summary_text": "Analysis of how international events (tariffs, crude prices, Fed policies, wars) specifically influence India",
    "developments": [
      {{
        "international_event": "What happened globally",
        "india_implication": "How it directly/indirectly affects Indian markets, businesses, or foreign policy",
        "article_id": "Matching ID"
      }}
    ]
  }},
  "business_and_markets": {{
    "summary_text": "Overview of corporate announcements, market movements (Nifty/Sensex/Rupee/Crude/Gold), and economic data",
    "highlights": [
      {{
        "point": "Specific corporate or financial milestone",
        "article_id": "Matching ID"
      }}
    ]
  }},
  "other_important": {{
    "summary_text": "Highlights from technology, AI, science, space, health, and sports",
    "items": [
      {{
        "category": "Technology / Science / Sports / Health",
        "point": "Key takeaway",
        "article_id": "Matching ID"
      }}
    ]
  }},
  "key_takeaways": [
    {{
      "takeaway": "Essential lesson, decision, or fact the reader must remember from today's developments",
      "article_id": "Matching ID",
      "importance": "CRITICAL / HIGH"
    }}
  ]
}}
"""
    return prompt.strip()
