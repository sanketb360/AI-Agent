"""Base fetcher interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.models.article import Article
from src.storage.base_storage import ArticleStorage
from src.transformers.article_transformer import ArticleTransformer


class BaseFetcher(ABC):
    def __init__(
        self,
        transformer: Optional[ArticleTransformer] = None,
        storage: Optional[ArticleStorage] = None,
    ):
        self.transformer = transformer
        self.storage = storage

    async def fetch_and_save(self) -> List[Article]:
        """
        Template method - defines algorithm skeleton.

        Steps:
        1. Fetch (varies by subclass)
        2. Save (same for all)

        Subclasses customize step 1 via fetch_articles().
        """
        articles = await self.fetch_articles()

        if articles and self.storage is not None:
            filename = f"{self.get_source_name()}_articles.md"
            self.storage.save(articles, filename)

        return articles

    @abstractmethod
    async def fetch_articles(self) -> List[Article]:
        """
        Fetch articles from source.

        Must be implemented by subclasses.
        This is the ONLY method that varies by source.

        Returns:
            List of Article objects
        """
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        """
        Get the name of this source.

        Returns:
            Source name (e.g., 'hackernews', 'rss', 'github')
        """
        pass
