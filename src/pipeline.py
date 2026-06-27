"""Complete pipeline: Fetch -> Filter."""

import asyncio
import sys
from pathlib import Path


def bootstrap_repo_root() -> None:
    """Ensure the repository root is importable when running this script directly."""
    repo_root = Path(__file__).resolve().parent.parent
    repo_root_str = str(repo_root)
    if repo_root_str not in sys.path:
        sys.path.insert(0, repo_root_str)


bootstrap_repo_root()

from src.orchestrator import FetchOrchestrator


async def run_pipeline():
    """
    Run complete pipeline.

    1. Fetch articles (Milestone 1)
    2. Filter with AI agent (Milestone 3)
    """
    repo_root = Path(__file__).resolve().parent.parent

    print("=" * 60)
    print("  Complete Pipeline: Fetch + Filter")
    print("=" * 60)

    # Step 1: Fetch articles
    print("\n📰 Step 1: Fetching articles...")
    orchestrator = FetchOrchestrator()
    articles = await orchestrator.fetch_all()

    fetch_output = repo_root / "data/articles/all_articles.md"
    print(f"✅ Fetched {len(articles)} articles")
    print(f"   Saved to: {fetch_output}")

    # Step 2: Filter with AI
    print("\n🤖 Step 2: Filtering with AI...")
    from src.agents.news_filter_agent import NewsFilterAgent

    agent = NewsFilterAgent()
    filter_output = repo_root / "data/context/filtered_articles.md"

    await agent.execute(input_path=str(fetch_output), output_path=str(filter_output))

    print("✅ Filtering complete")
    print(f"   Filtered articles: {filter_output}")

    print("\n" + "=" * 60)
    print("🎉 Pipeline complete!")
    print(f"   1. Fetched: {fetch_output}")
    print(f"   2. Filtered: {filter_output}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_pipeline())
