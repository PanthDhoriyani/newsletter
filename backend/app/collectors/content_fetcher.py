import httpx
import structlog
from bs4 import BeautifulSoup
from typing import Dict

log = structlog.get_logger()

class ContentFetcher:
    def __init__(self):
        self._cache: Dict[str, str] = {}
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    async def fetch_article_text(self, url: str) -> str:
        if not url:
            return ""
        if url in self._cache:
            return self._cache[url]

        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True, headers=self.headers) as client:
                res = await client.get(url)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, "html.parser")
                    
                    # Remove clutter
                    for tag in soup(["script", "style", "nav", "footer", "aside", "header", "form"]):
                        tag.decompose()

                    # Find main article text
                    article_elem = soup.find("article") or soup.find("main") or soup.find(class_=lambda c: c and ("article" in c or "story" in c))
                    if article_elem:
                        paragraphs = article_elem.find_all("p")
                    else:
                        paragraphs = soup.find_all("p")

                    text_chunks = [p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 35]
                    full_text = " ".join(text_chunks)[:3500]  # First 3500 chars

                    self._cache[url] = full_text
                    return full_text
        except Exception:
            pass

        return ""

content_fetcher = ContentFetcher()
