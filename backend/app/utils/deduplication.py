import re
from typing import List, Dict, Any

try:
    from rapidfuzz import fuzz
    def fuzzy_headline_similarity(h1: str, h2: str) -> float:
        if not h1 or not h2:
            return 0.0
        return fuzz.ratio(h1.lower().strip(), h2.lower().strip()) / 100.0
except ImportError:
    from difflib import SequenceMatcher
    def fuzzy_headline_similarity(h1: str, h2: str) -> float:
        if not h1 or not h2:
            return 0.0
        return SequenceMatcher(None, h1.lower().strip(), h2.lower().strip()).ratio()

def group_duplicate_articles(articles: List[Dict[str, Any]], threshold: float = 0.80) -> List[List[Dict[str, Any]]]:
    groups: List[List[Dict[str, Any]]] = []
    used_indices = set()

    for i, a in enumerate(articles):
        if i in used_indices:
            continue
        group = [a]
        h1 = a.get("headline", "")
        for j, b in enumerate(articles[i+1:], i+1):
            if j not in used_indices:
                h2 = b.get("headline", "")
                if fuzzy_headline_similarity(h1, h2) >= threshold:
                    group.append(b)
                    used_indices.add(j)
        used_indices.add(i)
        groups.append(group)

    return groups

STOPWORDS = {
    "the", "a", "an", "in", "of", "to", "for", "is", "are", "was", "were",
    "and", "or", "but", "with", "on", "at", "by", "from", "as", "that", "this",
    "it", "not", "be", "has", "have", "had", "will", "would", "can", "could",
    "says", "said", "after", "over", "into", "about", "more", "its", "news"
}

def extract_keywords(text: str) -> List[str]:
    if not text:
        return []
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    freq = {}
    for w in words:
        if w not in STOPWORDS:
            freq[w] = freq.get(w, 0) + 1
    sorted_words = sorted(freq.keys(), key=lambda x: freq[x], reverse=True)
    return sorted_words[:12]
