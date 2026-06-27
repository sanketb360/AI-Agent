"""Fetch top stories from HackerNews."""

import asyncio
import ssl
from datetime import datetime
from typing import List, Optional

import aiohttp
import certifi

from src.fetchers.base_fetcher import BaseFetcher
from src.models.article import Article
from src.storage.markdown_storage import MarkdownStorage
from src.transformers.article_transformer import ArticleTransformer
from src.utils.rate_limiter import RateLimiter


class HackerNewsFetcher(BaseFetcher):
    """Fetch top stories from HackerNews."""

    BASE_URL = "https://hacker-news.firebaseio.com/v0"

    def __init__(
        self,
        transformer: Optional[ArticleTransformer] = None,
        storage: Optional[MarkdownStorage] = None,
    ):
        transformer = transformer or ArticleTransformer()
        storage = storage or MarkdownStorage()
        super().__init__(transformer, storage)
        self.rate_limiter = RateLimiter(max_concurrent=10)

    async def fetch_articles(self) -> List[Article]:
        """Fetch HackerNews items and transform them into Article objects."""
        story_ids = await self._fetch_top_story_ids()
        raw_items = await self._fetch_stories(story_ids[:30])
        return self.transformer.transform_hackernews(raw_items)

    async def fetch(self, limit: int = 30) -> List[Article]:
        """Fetch a limited number of articles."""
        articles = await self.fetch_articles()
        return articles[:limit]

    async def fetch_and_save(self, limit: int = 30) -> List[Article]:
        """Fetch articles and save them to markdown storage."""
        articles = await self.fetch(limit)
        if articles:
            self.storage.save(articles, "hackernews_articles.md")
        return articles

    def get_source_name(self) -> str:
        """Return source name."""
        return "hackernews"

    async def _fetch_top_story_ids(self) -> List[int]:
        """Fetch the list of top story IDs from HackerNews."""
        url = f"{self.BASE_URL}/topstories.json"
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl_context)
        ) as session:
            async with session.get(url) as response:
                return await response.json()

    async def _fetch_stories(self, story_ids: List[int]) -> List[dict]:
        """Fetch multiple story items concurrently."""
        tasks = [self._fetch_story(story_id) for story_id in story_ids]
        stories = await asyncio.gather(*tasks)
        return [story for story in stories if story is not None]

    async def _fetch_story(self, story_id: int) -> Optional[dict]:
        """Fetch a single HackerNews story item by ID."""
        url = f"{self.BASE_URL}/item/{story_id}.json"
        try:
            async with self.rate_limiter:
                ssl_context = ssl.create_default_context(cafile=certifi.where())
                async with aiohttp.ClientSession(
                    connector=aiohttp.TCPConnector(ssl=ssl_context)
                ) as session:
                    async with session.get(url) as response:
                        data = await response.json()
                        if not data or not data.get("url"):
                            return None
                        return data
        except Exception as exc:
            print(f"⚠️  Failed to fetch story {story_id}: {exc}")
            return None


# Quick local smoke test
async def test_fetch():
    """Quick test of the HackerNews fetcher."""
    fetcher = HackerNewsFetcher()
    articles = await fetcher.fetch(limit=5)

    print(f"\n📊 Results:")
    for article in articles:
        print(f"  - {article.title[:50]}...")
    return articles


if __name__ == "__main__":
    asyncio.run(test_fetch())
