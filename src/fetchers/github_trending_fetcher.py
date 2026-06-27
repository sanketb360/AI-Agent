"""Fetch from GitHub Trending."""

import ssl
from datetime import datetime
from typing import List, Optional

import aiohttp
import certifi
from bs4 import BeautifulSoup

from src.fetchers.base_fetcher import BaseFetcher
from src.models.article import Article
from src.storage.base_storage import ArticleStorage
from src.transformers.article_transformer import ArticleTransformer


class GitHubTrendingFetcher(BaseFetcher):
    """
    Fetch trending repositories from GitHub.

    NEW fetcher - demonstrates Open/Closed Principle.
    Added WITHOUT modifying any existing code!
    """

    def __init__(
        self,
        transformer: Optional[ArticleTransformer] = None,
        storage: Optional[ArticleStorage] = None,
    ):
        super().__init__(transformer=transformer, storage=storage)

    async def fetch_articles(self) -> List[Article]:
        """Scrape GitHub trending page."""
        url = "https://github.com/trending"
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        connector = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url) as response:
                html = await response.text()

        soup = BeautifulSoup(html, "html.parser")
        repos = soup.select("article.Box-row")

        articles = []
        for repo in repos[:20]:  # Top 20
            # Extract repo info
            title_elem = repo.select_one("h2 a")
            if not title_elem:
                continue

            title = title_elem.text.strip().replace("\n", "").replace(" ", "")
            href = title_elem["href"]
            url = f"https://github.com{href}"

            description_elem = repo.select_one("p")
            description = description_elem.text.strip() if description_elem else ""

            stars_elem = repo.select_one("span.d-inline-block.float-sm-right")
            stars = stars_elem.text.strip() if stars_elem else "0"

            article = Article(
                title=title,
                url=url,
                published_at=datetime.now(),
                source="github_trending",
                summary=f"{description} (⭐ {stars})",
                score=0,
            )
            articles.append(article)

        return articles

    def get_source_name(self) -> str:
        """Return source name."""
        return "github_trending"
