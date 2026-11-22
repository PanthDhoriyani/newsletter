from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, extract
from app.database import get_db
from app.models.newsletter import Newsletter
from app.models.ongoing_story import OngoingStory
from app.schemas.newsletter import NewsletterListItem

router = APIRouter(prefix="/archive", tags=["archive"])

@router.get("/calendar")
async def get_archive_calendar(
    year: int = Query(2026),
    month: int = Query(11),
    db: AsyncSession = Depends(get_db)
):
    stmt = (
        select(Newsletter)
        .where(extract('year', Newsletter.edition_date) == year)
        .where(extract('month', Newsletter.edition_date) == month)
        .order_by(Newsletter.edition_date.asc())
    )
    res = await db.execute(stmt)
    editions = res.scalars().all()

    calendar_data = []
    for e in editions:
        calendar_data.append({
            "id": e.id,
            "date": str(e.edition_date),
            "status": e.status.value,
            "total_articles": e.total_articles,
            "critical_count": e.critical_count,
            "edition_status": "COMPLETED" if e.status.value == "PUBLISHED" else "UNREAD"
        })
    return calendar_data

@router.get("/editions", response_model=List[NewsletterListItem])
async def get_all_archived_editions(
    limit: int = Query(30, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Newsletter).order_by(desc(Newsletter.edition_date)).offset(offset).limit(limit)
    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/ongoing-stories")
async def get_ongoing_stories(db: AsyncSession = Depends(get_db)):
    stmt = select(OngoingStory).order_by(desc(OngoingStory.last_updated)).limit(20)
    res = await db.execute(stmt)
    return res.scalars().all()
