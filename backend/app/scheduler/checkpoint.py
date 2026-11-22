from datetime import datetime, timedelta, timezone
import structlog
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.scheduler_state import SchedulerState

try:
    from zoneinfo import ZoneInfo
    IST = ZoneInfo("Asia/Kolkata")
except ImportError:
    IST = timezone(timedelta(hours=5, minutes=30))

log = structlog.get_logger()

async def get_or_create_state(db: AsyncSession) -> SchedulerState:
    res = await db.execute(select(SchedulerState).where(SchedulerState.id == 1))
    state = res.scalar_one_or_none()
    if not state:
        state = SchedulerState(id=1, is_running=False, retry_count=0)
        db.add(state)
        await db.commit()
        await db.refresh(state)
    return state

async def get_current_coverage_window(db: AsyncSession) -> tuple[datetime, datetime]:
    state = await get_or_create_state(db)
    now_ist = datetime.now(IST).replace(tzinfo=None)

    if state.last_successful_cutoff:
        # Add 30-min small overlap to catch late-indexed news
        start_time = state.last_successful_cutoff - timedelta(minutes=30)
    else:
        start_time = now_ist - timedelta(hours=24)

    return start_time, now_ist

async def set_generation_start(db: AsyncSession, start_time: datetime, end_time: datetime):
    state = await get_or_create_state(db)
    state.is_running = True
    state.last_generation_start = datetime.utcnow()
    state.current_coverage_start = start_time
    state.current_coverage_end = end_time
    await db.commit()

async def advance_checkpoint(db: AsyncSession, successful_cutoff: datetime):
    state = await get_or_create_state(db)
    state.last_successful_cutoff = successful_cutoff
    state.is_running = False
    state.last_status = "SUCCESS"
    state.last_generation_end = datetime.utcnow()
    state.retry_count = 0
    await db.commit()
    log.info("checkpoint_advanced_successfully", cutoff=successful_cutoff.isoformat())

async def mark_generation_failed(db: AsyncSession, error_msg: str):
    state = await get_or_create_state(db)
    state.is_running = False
    state.last_status = f"FAILED: {error_msg[:100]}"
    state.retry_count += 1
    # CRITICAL RULE: Never advance last_successful_cutoff on failure
    await db.commit()
    log.error("generation_failed_checkpoint_preserved", retry_count=state.retry_count)
