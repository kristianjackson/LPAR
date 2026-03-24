"""Local filesystem storage helpers for LPS."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .schema import empty_profile


DEFAULT_WORKSPACE = Path(".lps")
PROFILE_DIR = "profiles"
ANALYSIS_DIR = "analysis"
REWRITE_DIR = "rewrites"


def init_workspace(base_dir: Path = DEFAULT_WORKSPACE) -> Path:
    """Initialize the local LPS workspace structure."""
    (base_dir / PROFILE_DIR).mkdir(parents=True, exist_ok=True)
    (base_dir / ANALYSIS_DIR).mkdir(parents=True, exist_ok=True)
    (base_dir / REWRITE_DIR).mkdir(parents=True, exist_ok=True)
    return base_dir


def write_profile(profile_name: str, profile: dict[str, Any], base_dir: Path = DEFAULT_WORKSPACE) -> Path:
    """Write a profile JSON document to the workspace."""
    init_workspace(base_dir)
    target = base_dir / PROFILE_DIR / f"{profile_name}.json"
    target.write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
    return target


def write_analysis_report(
    report_name: str,
    report: dict[str, Any],
    base_dir: Path = DEFAULT_WORKSPACE,
) -> Path:
    """Write an analysis report JSON document to the workspace."""
    init_workspace(base_dir)
    target = base_dir / ANALYSIS_DIR / f"{report_name}.json"
    target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return target


def write_rewrite_artifact(
    artifact_name: str,
    artifact: dict[str, Any],
    base_dir: Path = DEFAULT_WORKSPACE,
) -> Path:
    """Write a rewrite artifact JSON document to the workspace."""
    init_workspace(base_dir)
    target = base_dir / REWRITE_DIR / f"{artifact_name}.json"
    target.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    return target


def read_profile(path: Path) -> dict[str, Any]:
    """Read a profile JSON document from disk."""
    return json.loads(path.read_text(encoding="utf-8"))


def create_sample_profile(profile_name: str = "default", base_dir: Path = DEFAULT_WORKSPACE) -> Path:
    """Create a starter profile document."""
    return write_profile(profile_name, empty_profile(), base_dir)
