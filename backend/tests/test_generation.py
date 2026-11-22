import pytest
from app.models.article import ArticleImportance
from app.models.newsletter import NewsletterStatus
from app.utils.india_impact import score_india_relevance, has_india_impact
from app.utils.market_impact import detect_market_impact
from app.llm.quota_manager import QuotaManager

def test_article_importance_values():
    assert ArticleImportance.CRITICAL.value == "CRITICAL"
    assert ArticleImportance.HIGH.value == "HIGH"
    assert ArticleImportance.MODERATE.value == "MODERATE"

def test_newsletter_status_values():
    assert NewsletterStatus.PUBLISHED.value == "PUBLISHED"
    assert NewsletterStatus.FAILED.value == "FAILED"

def test_india_impact_scoring():
    article_in = {"headline": "RBI and Finance Ministry review Rupee exchange rate stability", "country": "IN"}
    article_out = {"headline": "Local elections conclude in Brazilian province", "country": "BR"}
    
    assert score_india_relevance(article_in) > score_india_relevance(article_out)
    assert has_india_impact(article_in) is True

def test_market_impact_detection():
    article = {"headline": "Nifty surges while crude oil prices drop sharply"}
    impact = detect_market_impact(article)
    assert impact["has_market_impact"] is True
    assert len(impact["affected_markets"]) >= 2

def test_quota_manager_limits():
    qm = QuotaManager()
    assert qm.can_use_gemini() is True
    qm._gemini_count = 1000
    assert qm.can_use_gemini(limit=950) is False
