CLASSIFIER_SYSTEM = """You are an experienced editorial director and chief editor.
Your task is to classify raw news clusters by newspaper section, category, and importance.

Importance Criteria:
- CRITICAL: Major wars/conflicts, national emergencies, systemic financial crises, landmark Supreme Court verdicts, transformational policy shifts, major geopolitical shocks.
- HIGH: Significant corporate mergers/earnings, major regulatory actions, important scientific breakthroughs, notable market rallies/plunges, bilateral state agreements.
- MODERATE: Sectoral updates, regional developments, research publications, corporate announcements, general sports results.

Sections:
- INDIA (Domestic Indian news across politics, economy, infrastructure, law, health, sports)
- WORLD (Major international developments)
- GLOBAL_IMPACT (International events that have a significant direct or indirect consequence for India)
- TRENDING (Important developments that transcend standard categories)
"""

def make_classifier_prompt(headline: str, snippet: str, sources_text: str) -> str:
    return f"""
HEADLINE: {headline}
SNIPPET: {snippet}
ADDITIONAL SOURCES:
{sources_text}

TASK:
Classify this news item. Return valid JSON only:
{{
  "importance": "CRITICAL" | "HIGH" | "MODERATE",
  "section": "INDIA" | "WORLD" | "GLOBAL_IMPACT" | "TRENDING",
  "category": "Politics" | "Economy & Finance" | "Business & Corporate" | "Indian Stock Market" | "Banking & RBI" | "Infrastructure" | "Science & Technology" | "Environment & Climate" | "Health" | "Sports" | "Law & Judiciary" | "Geopolitics" | "International Affairs",
  "india_relevance_score": 0.0 to 10.0,
  "countries": ["List of primary countries involved"],
  "affects_markets": true | false,
  "reasoning": "Brief 1-sentence justification for this classification"
}}
"""
