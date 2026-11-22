from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.database import get_db
from app.models.weekly_review import WeeklyReview

router = APIRouter(prefix="/weekly", tags=["weekly"])

@router.get("/")
async def list_weekly_reviews(db: AsyncSession = Depends(get_db)):
    stmt = select(WeeklyReview).order_by(desc(WeeklyReview.week_start)).limit(10)
    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/latest")
async def get_latest_weekly_review(db: AsyncSession = Depends(get_db)):
    stmt = select(WeeklyReview).order_by(desc(WeeklyReview.week_start)).limit(1)
    res = await db.execute(stmt)
    review = res.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="No weekly review published yet")
    return review

@router.get("/{review_id}")
async def get_weekly_review_by_id(review_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(WeeklyReview).where(WeeklyReview.id == review_id)
    res = await db.execute(stmt)
    review = res.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="Weekly review not found")
    return review
