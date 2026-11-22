from typing import List, Dict, Any

ARTICLE_SYSTEM_PROMPT = """You are a senior investigative and analytical newspaper journalist for a premier national newspaper.

CRITICAL INTEGRITY & CLARITY RULES:
1. Base EVERY single sentence and fact strictly on the provided source excerpts.
2. NEVER introduce fake news, unverified speculation, made-up statistics, quotes, names, or events not present in the sources.
3. If sources conflict or report conflicting figures, explicitly note the disagreement (e.g. 'while Source A reported X, Source B stated Y').
4. If information is preliminary or unfolding, clearly state 'According to initial reports' or 'Details are still developing'.
5. Strictly distinguish facts from allegations, estimates, opinions, and projections.
6. Write in engaging, crystal-clear, accessible language that anyone can understand without needing an economics or law degree.
7. Always provide a plain-words simplified summary and identify any technical terms, shortforms, or jargon to explain simply.
8. Structure the article properly with clear narrative flow.
"""

def make_article_prompt(
    headline_hint: str,
    sources: List[Dict[str, Any]],
    importance: str,
    section: str,
    category: str,
    india_impact_needed: bool = True,
    ongoing_story_context: str = ""
) -> str:
    sources_text = ""
    for idx, s in enumerate(sources, 1):
        sources_text += f"\n--- SOURCE {idx}: {s.get('source_name', 'Wire/News')} ({s.get('source_type', 'NEWS')}) ---\n"
        sources_text += f"URL: {s.get('source_url', '')}\n"
        sources_text += f"Headline: {s.get('headline', '')}\n"
        sources_text += f"Published At: {s.get('published_at', '')}\n"
        sources_text += f"Excerpt/Content: {s.get('snippet', '')} {s.get('raw_content', '')}\n"

    word_target = {
        "CRITICAL": "800 to 1200 words",
        "HIGH": "500 to 800 words",
        "MODERATE": "250 to 500 words"
    }.get(importance, "400 to 600 words")

    prompt = f"""
STORY TOPIC / EVENT: {headline_hint}
NEWSPAPER SECTION: {section}
CATEGORY: {category}
IMPORTANCE LEVEL: {importance} (Target depth: {word_target})
INDIA IMPACT ANALYSIS REQUIRED: {"YES" if india_impact_needed else "NO"}
{"ONGOING STORY CONTEXT: " + ongoing_story_context if ongoing_story_context else ""}

VERIFIED SOURCE MATERIAL:
{sources_text}

TASK:
Write a comprehensive, accessible newspaper article based SOLELY on the source material above. Use clear, everyday language so any reader can understand it.
Return a valid JSON object matching this schema:
{{
  "headline": "Informative, compelling newspaper headline (no clickbait)",
  "simplified_summary": "2-3 short, friendly sentences in simple plain English explaining what happened at a glance so anyone can grasp it immediately",
  "introduction": "Concise lead paragraph covering what happened, who was involved, and the core development",
  "detailed_reporting": "Comprehensive, factual body detailing the full background, events, verified quotes, and figures in easy-to-understand prose",
  "background_context": "Historical or recent context explained in simple terms so the reader understands why this occurred",
  "key_developments": "Structured breakdown or bullet points of the most essential new facts",
  "why_it_matters": "In-depth explanation of the strategic, geopolitical, economic, or societal significance in simple terms",
  "india_impact": {"Detailed analysis of direct or indirect consequences for India's economy, trade, diplomacy, or citizens" if india_impact_needed else "null"},
  "economic_industry_impact": "Impact on financial markets, relevant corporate sectors, trade, or consumer prices (if applicable, else null)",
  "what_happens_next": "Upcoming court dates, government meetings, regulatory deadlines, or expected next steps",
  "tags": ["3 to 6 relevant keywords"],
  "countries": ["List of countries directly involved"],
  "explained_terms": [
    {{
      "term": "Hard term, acronym, or shortform (e.g. Forex, Repo Rate, FTA, Bilateral, Disinvestment, Semiconductor Fab)",
      "meaning": "1-2 sentence crystal-clear explanation in simple plain words with an everyday analogy"
    }}
  ]
}}
"""
    return prompt.strip()

KNOWLEDGE_CORNER_SYSTEM = """You are an educator and senior economic/geopolitical analyst writing the 'Daily Knowledge Corner' for a national newspaper.
Your goal is to explain 3 to 5 real-world concepts, principles, or institutions that directly relate to today's news developments, helping readers expand their general knowledge, financial literacy, and economic understanding.
"""

def make_knowledge_prompt(articles_summary: str) -> str:
    return f"""
Review the day's published articles:
{articles_summary}

TASK:
Select 3 to 5 educational concepts, economic terms, legal doctrines, or international treaties/institutions mentioned or relevant to the developments above.
Explain each concept in simple, accessible, yet intellectually rigorous language.

Return JSON in this format:
[
  {{
    "term": "Term or Concept Name (e.g. Sovereign Bond Yield, Current Account Deficit, Article 356)",
    "simple_explanation": "Clear explanation in 100 to 150 words using simple analogies where helpful",
    "why_relevant_today": "Explanation of how this concept connects directly to today's news event",
    "related_headline": "Headline of the article where this concept arose"
  }}
]
"""

WATCH_NEXT_SYSTEM = """You are an investigative newspaper editor compiling the 'What to Watch Next' intelligence radar.
Extract ONLY upcoming events, deadlines, court hearings, RBI/Fed meetings, elections, or regulatory moves that are explicitly verified in the day's reporting. Do NOT invent dates or meetings.
"""

def make_watch_next_prompt(articles_summary: str) -> str:
    return f"""
From the following news reporting of today's edition:
{articles_summary}

TASK:
Identify upcoming scheduled events, announcements, hearings, economic data releases, or geopolitical talks.
Return JSON in this format:
[
  {{
    "event": "Short description of upcoming event",
    "expected_date": "Exact date, timeline, or month if mentioned (e.g. 'November 28, 2026' or 'Early next week')",
    "category": "Economy / Politics / Judiciary / Diplomacy / Sports / Technology",
    "why_important": "Why readers should keep an eye on this upcoming development"
  }}
]
"""
