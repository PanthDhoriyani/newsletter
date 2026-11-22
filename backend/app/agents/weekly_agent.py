import uuid
import structlog
from datetime import date, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.newsletter import Newsletter, NewsletterStatus
from app.models.weekly_review import WeeklyReview
from app.llm.gemini_client import gemini_client

log = structlog.get_logger()

async def generate_weekly_review(week_start: date, week_end: date, db: AsyncSession) -> str:
    stmt = (
        select(Newsletter)
        .where(Newsletter.edition_date >= week_start, Newsletter.edition_date <= week_end)
        .where(Newsletter.status == NewsletterStatus.PUBLISHED)
    )
    res = await db.execute(stmt)
    editions = res.scalars().all()

    if not editions:
        log.warning("no_published_editions_found_for_week", week_start=str(week_start))
        # Create empty placeholder
        review = WeeklyReview(
            id=str(uuid.uuid4()),
            week_start=week_start,
            week_end=week_end,
            content={"message": "No published editions available for this week range."},
            weekly_summary={"summary": "No editions recorded."},
            published_at=datetime.utcnow(),
            status="PUBLISHED",
            is_immutable=True,
            total_editions=0
        )
        db.add(review)
        await db.commit()
        return review.id

    # Synthesize weekly overview
    editions_text = "\n".join([f"Date: {e.edition_date}, Articles: {e.total_articles}" for e in editions])
    system_prompt = "You are the Chief Editor compiling the Sunday Weekly Review edition."
    user_prompt = f"Synthesize this week's news into an in-depth weekly review:\n{editions_text}\nReturn JSON with keys: 'top_stories', 'india_weekly', 'global_weekly', 'markets_weekly', 'weekly_summary'."

    data = await gemini_client.generate_json(system_prompt, user_prompt)
    review_id = str(uuid.uuid4())

    review = WeeklyReview(
        id=review_id,
        week_start=week_start,
        week_end=week_end,
        content=data,
        weekly_summary=data.get("weekly_summary", {}),
        published_at=datetime.utcnow(),
        status="PUBLISHED",
        is_immutable=True,
        total_editions=len(editions)
    )
    db.add(review)
    await db.commit()
    log.info("weekly_review_generated", review_id=review_id)
    return review_id
