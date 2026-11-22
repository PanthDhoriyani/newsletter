from typing import Dict, Any
from app.agents.supervisor import run_newspaper_pipeline
from app.agents.weekly_agent import generate_weekly_review

async def run_generation(coverage_window: Dict[str, str]) -> str:
    result = await run_newspaper_pipeline(coverage_window)
    if not result.get("edition_id"):
        raise RuntimeError("Generation failed to produce an edition ID.")
    return result["edition_id"]

__all__ = ["run_generation", "generate_weekly_review"]
