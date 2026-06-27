"""Orchestrate multiple news fetchers."""

import asyncio
from typing import List, Optional

from src.fetchers.base_fetcher import BaseFetcher
from src.fetchers.github_trending_fetcher import GitHubTrendingFetcher
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.models.article import Article
from src.storage.base_storage import ArticleStorage
from src.storage.markdown_storage import MarkdownStorage
from src.transformers.article_transformer import ArticleTransformer


class FetchOrchestrator:
    """
    Orchestrates multiple fetchers.

    Follows Dependency Inversion Principle:
    - Depends on abstractions (BaseFetcher, ArticleStorage)
    - Dependencies injected via constructor
    """

    def __init__(
        self,
        fetchers: Optional[List[BaseFetcher]] = None,
        storage: Optional[ArticleStorage] = None,
        transformer: Optional[ArticleTransformer] = None,
    ):
        """Initialize with injected dependencies or sensible defaults."""
        self.transformer = transformer or ArticleTransformer()
        self.storage = storage or MarkdownStorage("data/articles")
        self.fetchers = fetchers or [
            HackerNewsFetcher(self.transformer, self.storage),
            GitHubTrendingFetcher(self.transformer, self.storage),
        ]

    async def fetch_all(self) -> List[Article]:
        """Fetch from all configured sources."""
        all_articles: List[Article] = []

        for fetcher in self.fetchers:
            articles = await fetcher.fetch_and_save()
            all_articles.extend(articles)

        return all_articles


async def main():
    """Test orchestrator."""
    orchestrator = FetchOrchestrator()
    articles = await orchestrator.fetch_all()

    print("\n📊 Sample articles:")
    for article in articles[:5]:
        print(f"  [{article.source}] {article.title[:60]}...")


if __name__ == "__main__":
    asyncio.run(main())
