from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.database import get_db
from app.models.newsletter import Newsletter, NewsletterStatus
from app.models.article import Article, ArticleImportance
from app.models.breaking_news import BreakingNews
from app.models.reading_progress import ReadingProgress, ReadStatus
from app.models.saved_article import SavedArticle

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/")
async def get_dashboard_data(db: AsyncSession = Depends(get_db)):
    # 1. Latest Published Edition
    stmt_edition = (
        select(Newsletter)
        .where(Newsletter.status == NewsletterStatus.PUBLISHED)
        .order_by(desc(Newsletter.edition_date))
        .limit(1)
    )
    edition = (await db.execute(stmt_edition)).scalar_one_or_none()
    
    edition_info = None
    if edition:
        edition_info = {
            "id": edition.id,
            "edition_date": str(edition.edition_date),
            "total_articles": edition.total_articles,
            "critical_count": edition.critical_count,
            "high_count": edition.high_count,
            "moderate_count": edition.moderate_count,
            "summary_preview": (edition.daily_summary or {}).get("biggest_headlines", [])[:3]
        }

    # 2. Breaking News
    stmt_breaking = (
        select(BreakingNews)
        .where(BreakingNews.is_active == True)
        .order_by(desc(BreakingNews.published_at))
        .limit(3)
    )
    breaking_items = (await db.execute(stmt_breaking)).scalars().all()

    # 3. Top Critical & High Unread Articles
    stmt_articles = (
        select(Article)
        .where(Article.importance.in_([ArticleImportance.CRITICAL, ArticleImportance.HIGH]))
        .order_by(desc(Article.published_at))
        .limit(6)
    )
    top_articles = (await db.execute(stmt_articles)).scalars().all()

    # 4. Saved Articles Count
    stmt_saved = select(Article).join(SavedArticle).limit(5)
    saved_items = (await db.execute(stmt_saved)).scalars().all()

    # 5. Generation Status
    from app.models.scheduler_state import SchedulerState
    stmt_sched = select(SchedulerState).where(SchedulerState.id == 1)
    sched_state = (await db.execute(stmt_sched)).scalar_one_or_none()

    return {
        "today_edition": edition_info,
        "is_generating": sched_state.is_running if sched_state else False,
        "generation_status": sched_state.last_status if sched_state else "IDLE",
        "breaking_news": [
            {
                "id": b.id,
                "headline": b.headline,
                "summary": b.summary,
                "importance": b.importance,
                "published_at": b.published_at.isoformat()
            } for b in breaking_items
        ],
        "top_stories": [
            {
                "id": a.id,
                "headline": a.headline,
                "section": a.section,
                "category": a.category,
                "importance": a.importance.value,
                "introduction": a.introduction,
                "published_at": a.published_at.isoformat()
            } for a in top_articles
        ],
        "reading_progress": {
            "total_editions": 1 if edition else 0,
            "read_articles": 0,
            "saved_count": len(saved_items)
        }
    }
