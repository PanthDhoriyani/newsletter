from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, or_
from app.database import get_db
from app.models.article import Article, ArticleImportance
from app.models.reading_progress import ReadingProgress, ReadStatus
from app.models.saved_article import SavedArticle
from app.schemas.article import ArticleRead, ArticleListItem

router = APIRouter(prefix="/articles", tags=["articles"])

@router.get("/{article_id}", response_model=ArticleRead)
async def get_article_by_id(article_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Article).where(Article.id == article_id)
    res = await db.execute(stmt)
    article = res.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.get("/search", response_model=List[ArticleListItem])
async def search_articles(
    q: Optional[str] = Query(None),
    section: Optional[str] = Query(None),
    importance: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    limit: int = Query(30, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Article)
    
    if q:
        search_filter = f"%{q.strip()}%"
        stmt = stmt.where(
            or_(
                Article.headline.ilike(search_filter),
                Article.content.ilike(search_filter),
                Article.introduction.ilike(search_filter)
            )
        )
    if section:
        stmt = stmt.where(Article.section == section.upper())
    if importance:
        stmt = stmt.where(Article.importance == ArticleImportance(importance.upper()))
    if category:
        stmt = stmt.where(Article.category.ilike(f"%{category}%"))

    stmt = stmt.order_by(desc(Article.published_at)).limit(limit)
    res = await db.execute(stmt)
    articles = res.scalars().all()
    return articles

@router.get("/unread", response_model=List[ArticleListItem])
async def get_unread_articles(
    limit: int = Query(30, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    # Articles not marked READ in ReadingProgress
    stmt = (
        select(Article)
        .outerjoin(ReadingProgress, Article.id == ReadingProgress.article_id)
        .where(or_(ReadingProgress.status == None, ReadingProgress.status == ReadStatus.UNREAD))
        .order_by(
            # CRITICAL first, then HIGH, then MODERATE
            Article.importance,
            desc(Article.published_at)
        )
        .limit(limit)
    )
    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/saved", response_model=List[ArticleRead])
async def get_saved_articles(db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Article)
        .join(SavedArticle, Article.id == SavedArticle.article_id)
        .order_by(desc(SavedArticle.saved_at))
    )
    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/critical", response_model=List[ArticleListItem])
async def get_critical_unread_articles(db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Article)
        .where(Article.importance == ArticleImportance.CRITICAL)
        .order_by(desc(Article.published_at))
        .limit(20)
    )
    res = await db.execute(stmt)
    return res.scalars().all()
