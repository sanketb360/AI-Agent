import sys
from pathlib import Path

from src.pipeline import bootstrap_repo_root


def test_bootstrap_repo_root_adds_workspace_root_to_sys_path():
    repo_root = Path(__file__).resolve().parents[1]
    sys.path = [p for p in sys.path if Path(p).resolve() != repo_root]

    bootstrap_repo_root()

    assert str(repo_root) in sys.path
