"""Orchestrate multiple news fetchers."""

import asyncio
from typing import List

from src import storage
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.fetchers.rss_fetcher import RSSFetcher
from src.models.article import Article
from src.storage.markdown_storage import MarkdownStorage
from src.fetchers.github_trending_fetcher import GitHubTrendingFetcher
from src.transformers.article_transformer import ArticleTransformer
from typing import List
from src.fetchers.base_fetcher import BaseFetcher
from src.transformers.article_transformer import ArticleTransformer
from src.storage.base_storage import ArticleStorage
# src/orchestrator.py

from typing import List
from src.fetchers.base_fetcher import BaseFetcher
from src.transformers.article_transformer import ArticleTransformer
from src.storage.base_storage import ArticleStorage




class FetchOrchestrator:
    """
    Orchestrates multiple fetchers.
    
    Follows Dependency Inversion Principle:
    - Depends on abstractions (BaseFetcher, ArticleStorage)
    - Dependencies injected via constructor
    """
    
    def __init__(
        self,
        fetchers: List[BaseFetcher],
        storage: ArticleStorage,
        transformer: ArticleTransformer
    ):
        """
        Initialize with injected dependencies.
        
        Args:
            fetchers: List of fetcher instances
            storage: Storage implementation
            transformer: Transformer instance
        """
        self.fetchers = fetchers
        self.storage = storage
        self.transformer = transformer
    
    async def fetch_all(self) -> List[Article]:
        """Fetch from all sources."""
        all_articles = []
        
        for fetcher in self.fetchers:
            articles = await fetcher.fetch_and_save()
            all_articles.extend(articles)
        
        return all_articles


# Test it
async def main():
    """Test orchestrator."""
    orchestrator = FetchOrchestrator()
    articles = await orchestrator.fetch_all()

    print(f"\n📊 Sample articles:")
    for article in articles[:5]:
        print(f"  [{article.source}] {article.title[:60]}...")


if __name__ == "__main__":
    asyncio.run(main())
