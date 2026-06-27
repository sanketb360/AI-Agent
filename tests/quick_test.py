# Quick test
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.storage.markdown_storage import MarkdownStorage
from src.models.article import Article
from datetime import datetime

storage = MarkdownStorage("data/test_articles")
test_article = Article(
    title="Test Article",
    url="http://test.com",
    published_at=datetime.now(),
    source="test",
    summary="Test summary"
)
path = storage.save([test_article], "test.md")
assert path.exists()
print(f"✅ Saved to {path}")