import asyncio
import structlog
from typing import Callable, Any

log = structlog.get_logger()

async def run_with_retry(func: Callable[..., Any], max_retries: int = 3, backoff_base: float = 2.0, **kwargs) -> Any:
    last_exc = None
    for attempt in range(1, max_retries + 1):
        try:
            log.info("generation_execution_attempt", attempt=attempt, max_retries=max_retries)
            return await func(**kwargs)
        except Exception as e:
            last_exc = e
            log.error("generation_attempt_failed", attempt=attempt, error=str(e))
            if attempt < max_retries:
                sleep_sec = backoff_base ** attempt
                log.info("retrying_after_delay", sleep_sec=sleep_sec)
                await asyncio.sleep(sleep_sec)
    
    raise RuntimeError(f"All {max_retries} attempts failed. Last exception: {last_exc}")
