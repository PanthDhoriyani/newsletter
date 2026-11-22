import pytest
from app.utils.deduplication import fuzzy_headline_similarity, group_duplicate_articles, extract_keywords

def test_fuzzy_similarity_identical():
    assert fuzzy_headline_similarity("Sensex surges 800 points", "Sensex surges 800 points") == 1.0

def test_fuzzy_similarity_different():
    score = fuzzy_headline_similarity("Sensex surges 800 points", "NASA rover finds water on Mars")
    assert score < 0.3

def test_fuzzy_similarity_minor_variation():
    score = fuzzy_headline_similarity("Nifty hits 25,000 for the first time", "Nifty crosses 25,000 mark for the first time")
    assert score > 0.70

def test_group_duplicate_articles():
    articles = [
        {"headline": "RBI cuts repo rate by 25 bps", "source_name": "Source A"},
        {"headline": "RBI cuts key repo rate by 25 bps", "source_name": "Source B"},
        {"headline": "ISRO launches lunar orbiter satellite", "source_name": "Source C"}
    ]
    groups = group_duplicate_articles(articles, threshold=0.75)
    assert len(groups) == 2

def test_extract_keywords():
    text = "The Reserve Bank of India has announced monetary policy adjustments for banking liquidity."
    keywords = extract_keywords(text)
    assert "reserve" in keywords or "monetary" in keywords or "policy" in keywords
