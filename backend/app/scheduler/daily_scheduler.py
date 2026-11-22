import structlog
from datetime import datetime, date, timedelta, timezone
from app.config import settings

try:
    from zoneinfo import ZoneInfo
    IST = ZoneInfo("Asia/Kolkata")
except ImportError:
    IST = timezone(timedelta(hours=5, minutes=30))

from app.database import AsyncSessionLocal
from app.scheduler.checkpoint import (
    get_or_create_state,
    get_current_coverage_window,
    set_generation_start,
    advance_checkpoint,
    mark_generation_failed
)
from app.scheduler.retry import run_with_retry
from app.agents.workflow import run_generation, generate_weekly_review

log = structlog.get_logger()

# Try APScheduler if installed, else fallback to standard asyncio timer
has_apscheduler = False
try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.cron import CronTrigger
    scheduler = AsyncIOScheduler(timezone=IST)
    has_apscheduler = True
except ImportError:
    scheduler = None

async def run_daily_generation_job():
    log.info("daily_newspaper_job_triggered")
    async with AsyncSessionLocal() as db:
        state = await get_or_create_state(db)
        if state.is_running:
            log.warning("generation_already_running_skipping_duplicate_trigger")
            return

        start_time, end_time = await get_current_coverage_window(db)
        await set_generation_start(db, start_time, end_time)

        try:
            coverage_window = {
                "start": start_time.isoformat(),
                "end": end_time.isoformat()
            }
            edition_id = await run_with_retry(
                run_generation,
                max_retries=settings.max_generation_retries,
                coverage_window=coverage_window
            )
            await advance_checkpoint(db, end_time)
            log.info("daily_generation_job_succeeded", edition_id=edition_id)
        except Exception as e:
            await mark_generation_failed(db, str(e))
            log.critical("daily_generation_job_failed_permanently", error=str(e))

async def run_weekly_review_job():
    today = date.today()
    week_start = today - timedelta(days=7)
    week_end = today - timedelta(days=1)
    async with AsyncSessionLocal() as db:
        await generate_weekly_review(week_start, week_end, db)

def start_scheduler():
    if not has_apscheduler or scheduler is None:
        log.info("apscheduler_not_installed_manual_and_api_triggers_active")
        return

    hour, minute = 8, 0
    if settings.newspaper_generation_time:
        try:
            parts = settings.newspaper_generation_time.split(":")
            hour, minute = int(parts[0]), int(parts[1])
        except Exception:
            pass

    scheduler.add_job(
        run_daily_generation_job,
        CronTrigger(hour=hour, minute=minute, timezone=IST),
        id="daily_newspaper_generation",
        replace_existing=True,
        misfire_grace_time=3600,
        coalesce=True
    )

    scheduler.add_job(
        run_weekly_review_job,
        CronTrigger(day_of_week="sun", hour=9, minute=0, timezone=IST),
        id="weekly_newspaper_review",
        replace_existing=True,
        misfire_grace_time=7200
    )

    scheduler.start()
    log.info("apscheduler_started_successfully", time=f"{hour:02d}:{minute:02d} IST")

def stop_scheduler():
    if has_apscheduler and scheduler and scheduler.running:
        scheduler.shutdown(wait=False)
        log.info("scheduler_shutdown_completed")
