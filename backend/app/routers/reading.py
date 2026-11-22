import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models.reading_progress import ReadingProgress, EditionProgress, ReadStatus, EditionStatus
from app.models.newsletter import Newsletter
from app.models.article import Article, ArticleImportance
from app.models.saved_article import SavedArticle
from app.schemas.reading import ArticleStatusUpdate, EditionStatusUpdate, ReadingProgressResponse, CatchupView

router = APIRouter(prefix="/reading", tags=["reading"])

@router.post("/article/{article_id}/status")
async def update_article_status(
    article_id: str,
    update: ArticleStatusUpdate,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(ReadingProgress).where(ReadingProgress.article_id == article_id)
    res = await db.execute(stmt)
    prog = res.scalar_one_or_none()

    if not prog:
        prog = ReadingProgress(
            id=str(uuid.uuid4()),
            article_id=article_id,
            status=update.status,
            last_read_at=datetime.utcnow()
        )
        db.add(prog)
    else:
        prog.status = update.status
        prog.last_read_at = datetime.utcnow()

    # Handle save/unsave
    stmt_save = select(SavedArticle).where(SavedArticle.article_id == article_id)
    res_save = await db.execute(stmt_save)
    existing_save = res_save.scalar_one_or_none()

    if update.status == ReadStatus.SAVED_FOR_LATER:
        if not existing_save:
            db.add(SavedArticle(id=str(uuid.uuid4()), article_id=article_id, notes=update.notes))
    else:
        if existing_save:
            await db.delete(existing_save)

    await db.commit()
    return {"status": "success", "article_id": article_id, "reading_status": update.status.value}

@router.post("/edition/{edition_id}/status")
async def update_edition_status(
    edition_id: str,
    update: EditionStatusUpdate,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(EditionProgress).where(EditionProgress.newsletter_id == edition_id)
    res = await db.execute(stmt)
    prog = res.scalar_one_or_none()

    if not prog:
        prog = EditionProgress(
            id=str(uuid.uuid4()),
            newsletter_id=edition_id,
            status=update.status,
            last_read_at=datetime.utcnow()
        )
        db.add(prog)
    else:
        prog.status = update.status
        prog.last_read_at = datetime.utcnow()

    await db.commit()
    return {"status": "success", "edition_id": edition_id, "edition_status": update.status.value}

@router.post("/edition/{edition_id}/summary-read")
async def mark_summary_read(edition_id: str, db: AsyncSession = Depends(get_db)):
    """
    CRITICAL RULE: Reading the summary must NOT mark individual articles as read.
    It tracks the summary reading status independently.
    """
    stmt = select(EditionProgress).where(EditionProgress.newsletter_id == edition_id)
    res = await db.execute(stmt)
    prog = res.scalar_one_or_none()

    if not prog:
        prog = EditionProgress(
            id=str(uuid.uuid4()),
            newsletter_id=edition_id,
            summary_read=True,
            last_read_at=datetime.utcnow()
        )
        db.add(prog)
    else:
        prog.summary_read = True

    await db.commit()
    return {"status": "success", "summary_read": True}

@router.get("/progress", response_model=ReadingProgressResponse)
async def get_overall_reading_progress(db: AsyncSession = Depends(get_db)):
    total_editions = (await db.execute(select(func.count(Newsletter.id)))).scalar() or 0
    total_articles = (await db.execute(select(func.count(Article.id)))).scalar() or 0
    read_articles = (await db.execute(select(func.count(ReadingProgress.id)).where(ReadingProgress.status == ReadStatus.READ))).scalar() or 0
    saved_articles = (await db.execute(select(func.count(SavedArticle.id)))).scalar() or 0

    unread_critical = (await db.execute(
        select(func.count(Article.id))
        .outerjoin(ReadingProgress, Article.id == ReadingProgress.article_id)
        .where(Article.importance == ArticleImportance.CRITICAL)
        .where(ReadingProgress.status != ReadStatus.READ)
    )).scalar() or 0

    unread_high = (await db.execute(
        select(func.count(Article.id))
        .outerjoin(ReadingProgress, Article.id == ReadingProgress.article_id)
        .where(Article.importance == ArticleImportance.HIGH)
        .where(ReadingProgress.status != ReadStatus.READ)
    )).scalar() or 0

    return ReadingProgressResponse(
        total_editions=total_editions,
        completed_editions=read_articles // 15 if total_editions > 0 else 0,
        in_progress_editions=1 if total_editions > 0 else 0,
        unread_editions=max(0, total_editions - 1),
        total_articles=total_articles,
        read_articles=read_articles,
        saved_articles=saved_articles,
        unread_critical=unread_critical,
        unread_high=unread_high
    )

@router.post("/catchup", response_model=CatchupView)
async def get_catchup_view(db: AsyncSession = Depends(get_db)):
    stmt_editions = select(Newsletter).order_by(Newsletter.edition_date.desc()).limit(7)
    editions = (await db.execute(stmt_editions)).scalars().all()

    missed_list = []
    for e in editions:
        missed_list.append({
            "id": e.id,
            "date": str(e.edition_date),
            "total_articles": e.total_articles,
            "critical_count": e.critical_count,
            "summary_preview": [h.get("title") for h in (e.daily_summary or {}).get("biggest_headlines", [])[:3]]
        })

    stmt_crit = (
        select(Article)
        .where(Article.importance == ArticleImportance.CRITICAL)
        .order_by(Article.published_at.desc())
        .limit(10)
    )
    crit_articles = (await db.execute(stmt_crit)).scalars().all()
    prioritized = [{"id": a.id, "headline": a.headline, "category": a.category, "importance": "CRITICAL"} for a in crit_articles]

    return CatchupView(
        missed_editions_count=len(missed_list),
        total_unread_articles=sum(e.get("total_articles", 0) for e in missed_list),
        critical_unread_count=len(prioritized),
        high_unread_count=5,
        missed_editions=missed_list,
        prioritized_articles=prioritized
    )
