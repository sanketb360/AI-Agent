import importlib.util
import sys
import types
from pathlib import Path


def test_evaluator_can_import_news_filter_agent(monkeypatch):
    repo_root = Path(__file__).resolve().parents[1]
    module_path = repo_root / "src" / "evaluation" / "evaluator.py"

    fake_news_filter_agent = types.ModuleType("src.agents.news_filter_agent")

    class DummyAgent:
        pass

    fake_news_filter_agent.NewsFilterAgent = DummyAgent

    src_pkg = types.ModuleType("src")
    src_pkg.__path__ = [str(repo_root / "src")]
    agents_pkg = types.ModuleType("src.agents")
    agents_pkg.__path__ = [str(repo_root / "src" / "agents")]

    monkeypatch.setitem(sys.modules, "src", src_pkg)
    monkeypatch.setitem(sys.modules, "src.agents", agents_pkg)
    monkeypatch.setitem(
        sys.modules, "src.agents.news_filter_agent", fake_news_filter_agent
    )

    spec = importlib.util.spec_from_file_location("evaluator_under_test", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    assert module.FilterEvaluator is not None
