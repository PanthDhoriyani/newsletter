from typing import List, Dict, Any

VERIFICATION_SYSTEM = """You are a senior news fact-checker and source intelligence analyst.
Your objective is to verify claims across multiple independent reporting outlets, identify contradictions, and flag any unverified rumors.
"""

def make_verification_prompt(claims: List[str], sources: List[Dict[str, Any]]) -> str:
    sources_summary = "\n".join([
        f"- {s.get('source_name')} ({s.get('source_type')}): {s.get('snippet', '')} | {s.get('headline', '')}"
        for s in sources
    ])
    claims_list = "\n".join([f"{i+1}. {c}" for i, c in enumerate(claims)])

    return f"""
CLAIMS TO VERIFY:
{claims_list}

AVAILABLE REPORTING SOURCES:
{sources_summary}

TASK:
Cross-reference each claim against the sources. Return valid JSON only:
{{
  "verified": true | false,
  "confidence_score": 0.0 to 1.0,
  "independent_source_count": integer,
  "status": "VERIFIED" | "SINGLE_SOURCE" | "CONTRADICTED" | "UNVERIFIED",
  "contradictions_found": ["List any conflicting figures or facts between sources, or leave empty if none"],
  "notes": "Short summary of verification findings"
}}
"""
