from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.database import get_db
from app.models.newsletter import Newsletter, NewsletterStatus
from app.models.article import Article
from app.schemas.newsletter import NewsletterListItem, NewsletterRead, EditionOverview
from app.schemas.article import ArticleRead
from app.scheduler.daily_scheduler import run_daily_generation_job

router = APIRouter(prefix="/editions", tags=["editions"])

@router.get("/", response_model=List[NewsletterListItem])
async def list_editions(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    stmt = (
        select(Newsletter)
        .order_by(desc(Newsletter.edition_date))
        .offset(offset)
        .limit(limit)
    )
    res = await db.execute(stmt)
    editions = res.scalars().all()
    
    output = []
    for e in editions:
        output.append(NewsletterListItem(
            id=e.id,
            edition_date=e.edition_date,
            published_at=e.published_at,
            status=e.status,
            total_articles=e.total_articles,
            critical_count=e.critical_count,
            high_count=e.high_count,
            moderate_count=e.moderate_count,
            edition_status="COMPLETED" if e.status == NewsletterStatus.PUBLISHED else "UNREAD",
            articles_read=0
        ))
    return output

@router.get("/today", response_model=NewsletterRead)
async def get_today_edition(db: AsyncSession = Depends(get_db)):
    today_date = date.today()
    stmt = select(Newsletter).where(Newsletter.edition_date == today_date)
    res = await db.execute(stmt)
    edition = res.scalar_one_or_none()
    
    if not edition:
        # Fallback to the latest published edition
        stmt_latest = (
            select(Newsletter)
            .where(Newsletter.status == NewsletterStatus.PUBLISHED)
            .order_by(desc(Newsletter.edition_date))
            .limit(1)
        )
        res_latest = await db.execute(stmt_latest)
        edition = res_latest.scalar_one_or_none()

    if not edition:
        raise HTTPException(status_code=404, detail="No newspaper edition published yet.")

    return edition

@router.get("/missed", response_model=List[NewsletterListItem])
async def get_missed_editions(db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Newsletter)
        .order_by(desc(Newsletter.edition_date))
        .limit(10)
    )
    res = await db.execute(stmt)
    editions = res.scalars().all()
    return editions

@router.get("/{edition_id}", response_model=NewsletterRead)
async def get_edition_by_id(edition_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Newsletter).where(Newsletter.id == edition_id)
    res = await db.execute(stmt)
    edition = res.scalar_one_or_none()
    if not edition:
        raise HTTPException(status_code=404, detail="Edition not found")
    return edition

@router.get("/{edition_id}/summary")
async def get_edition_summary(edition_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Newsletter).where(Newsletter.id == edition_id)
    res = await db.execute(stmt)
    edition = res.scalar_one_or_none()
    if not edition:
        raise HTTPException(status_code=404, detail="Edition not found")
    return edition.daily_summary or {}

@router.get("/{edition_id}/overview", response_model=EditionOverview)
async def get_edition_overview(edition_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Newsletter).where(Newsletter.id == edition_id)
    res = await db.execute(stmt)
    edition = res.scalar_one_or_none()
    if not edition:
        raise HTTPException(status_code=404, detail="Edition not found")

    headlines = []
    if edition.daily_summary and "biggest_headlines" in edition.daily_summary:
        headlines = [h.get("title", "") for h in edition.daily_summary["biggest_headlines"][:4]]

    return EditionOverview(
        id=edition.id,
        edition_date=edition.edition_date,
        published_at=edition.published_at,
        total_articles=edition.total_articles,
        critical_count=edition.critical_count,
        high_count=edition.high_count,
        moderate_count=edition.moderate_count,
        status=edition.status.value,
        summary_preview=headlines,
        reading_percentage=0.0
    )

@router.get("/status")
async def get_generation_status(db: AsyncSession = Depends(get_db)):
    """Returns the live status of the generation pipeline."""
    from app.models.scheduler_state import SchedulerState
    stmt = select(SchedulerState).where(SchedulerState.id == 1)
    res = await db.execute(stmt)
    state = res.scalar_one_or_none()
    if not state:
        return {"is_generating": False, "last_status": "IDLE"}
    return {
        "is_generating": state.is_running,
        "last_status": state.last_status or "IDLE",
        "last_generation_start": state.last_generation_start.isoformat() if state.last_generation_start else None,
        "last_generation_end": state.last_generation_end.isoformat() if state.last_generation_end else None,
        "last_successful_cutoff": state.last_successful_cutoff.isoformat() if state.last_successful_cutoff else None,
        "retry_count": state.retry_count
    }

@router.post("/generate")
async def trigger_manual_generation(background_tasks: BackgroundTasks):
    """Allows triggering immediate generation out of schedule."""
    background_tasks.add_task(run_daily_generation_job)
    return {"message": "Newspaper generation initiated in background", "status": "PENDING"}
