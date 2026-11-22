import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.database import get_db
from app.models.breaking_news import BreakingNews
from app.schemas.breaking_news import BreakingNewsCreate, BreakingNewsRead

router = APIRouter(prefix="/breaking", tags=["breaking"])

@router.get("/", response_model=List[BreakingNewsRead])
async def get_breaking_news(db: AsyncSession = Depends(get_db)):
    stmt = (
        select(BreakingNews)
        .where(BreakingNews.is_active == True)
        .order_by(desc(BreakingNews.published_at))
        .limit(5)
    )
    res = await db.execute(stmt)
    return res.scalars().all()

@router.post("/", response_model=BreakingNewsRead)
async def publish_breaking_news(
    payload: BreakingNewsCreate,
    db: AsyncSession = Depends(get_db)
):
    # Rule: Breaking news must verify sources and cannot replace regular paper
    is_verified = len(payload.sources) >= 2
    
    bn = BreakingNews(
        id=str(uuid.uuid4()),
        headline=payload.headline,
        summary=payload.summary,
        content=payload.content,
        importance=payload.importance,
        sources=payload.sources,
        is_verified=is_verified,
        published_at=datetime.utcnow(),
        is_active=True
    )
    db.add(bn)
    await db.commit()
    await db.refresh(bn)
    return bn
