import pytest
import uuid
from datetime import datetime, date
from app.models.newsletter import Newsletter, NewsletterStatus
from app.models.article import Article, ArticleImportance

@pytest.mark.asyncio
async def test_reading_summary_independent_from_articles(client, db_session):
    # Setup test edition
    ed_id = str(uuid.uuid4())
    art_id = str(uuid.uuid4())

    edition = Newsletter(
        id=ed_id,
        edition_date=date(2026, 11, 23),
        coverage_start=datetime.utcnow(),
        coverage_end=datetime.utcnow(),
        status=NewsletterStatus.PUBLISHED,
        total_articles=1
    )
    article = Article(
        id=art_id,
        newsletter_id=ed_id,
        headline="Test Article Headline",
        section="INDIA",
        category="Economy",
        importance=ArticleImportance.HIGH,
        content="Test content body",
        published_at=datetime.utcnow()
    )
    db_session.add(edition)
    db_session.add(article)
    await db_session.commit()

    # Mark summary as read
    res = await client.post(f"/api/reading/edition/{ed_id}/summary-read")
    assert res.status_code == 200
    assert res.json()["summary_read"] is True

    # Critical requirement: Article read status must remain UNREAD!
    res_art = await client.get("/api/articles/unread")
    assert res_art.status_code == 200
    unread_ids = [a["id"] for a in res_art.json()]
    assert art_id in unread_ids
