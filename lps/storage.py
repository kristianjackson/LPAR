"""Local filesystem storage helpers for LPS."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .schema import empty_profile


DEFAULT_WORKSPACE = Path(".lps")
PROFILE_DIR = "profiles"


def init_workspace(base_dir: Path = DEFAULT_WORKSPACE) -> Path:
    """Initialize the local LPS workspace structure."""
    (base_dir / PROFILE_DIR).mkdir(parents=True, exist_ok=True)
    return base_dir


def write_profile(profile_name: str, profile: dict[str, Any], base_dir: Path = DEFAULT_WORKSPACE) -> Path:
    """Write a profile JSON document to the workspace."""
    init_workspace(base_dir)
    target = base_dir / PROFILE_DIR / f"{profile_name}.json"
    target.write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
    return target


def read_profile(path: Path) -> dict[str, Any]:
    """Read a profile JSON document from disk."""
    return json.loads(path.read_text(encoding="utf-8"))


def create_sample_profile(profile_name: str = "default", base_dir: Path = DEFAULT_WORKSPACE) -> Path:
    """Create a starter profile document."""
    return write_profile(profile_name, empty_profile(), base_dir)
