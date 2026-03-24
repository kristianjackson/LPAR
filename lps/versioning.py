"""Versioning and diff helpers for LPS."""

from __future__ import annotations

from datetime import datetime, timezone
import difflib
import json
from pathlib import Path
from typing import Any

from .storage import VERSION_DIR


def create_version_record(
    rewrite_artifact: dict[str, Any],
    variant_id: str,
    source_rewrite: str,
) -> dict[str, Any]:
    """Create a saved version record from a rewrite artifact variant."""
    variant = _find_variant(rewrite_artifact["variants"], variant_id)
    version_id = _build_version_id(rewrite_artifact["lens"], variant_id)
    timestamp = datetime.now(timezone.utc).isoformat()

    return {
        "artifact_version": 1,
        "version_id": version_id,
        "saved_at": timestamp,
        "source_rewrite": source_rewrite,
        "source_profile": rewrite_artifact["source_profile"],
        "lens": rewrite_artifact["lens"],
        "lens_label": rewrite_artifact["lens_label"],
        "variant_id": variant["id"],
        "variant_label": variant["label"],
        "profile": variant["profile"],
    }


def list_version_records(base_dir: Path) -> list[dict[str, Any]]:
    """Return saved version records sorted by newest first."""
    version_dir = base_dir / VERSION_DIR
    if not version_dir.exists():
        return []

    records: list[dict[str, Any]] = []
    for path in version_dir.glob("*.json"):
        records.append(json.loads(path.read_text(encoding="utf-8")))

    return sorted(records, key=lambda record: record["saved_at"], reverse=True)


def read_version_record(base_dir: Path, version_id: str) -> dict[str, Any]:
    """Read a saved version record from the workspace."""
    target = base_dir / VERSION_DIR / f"{version_id}.json"
    return json.loads(target.read_text(encoding="utf-8"))


def render_version_diff(version_a: dict[str, Any], version_b: dict[str, Any]) -> str:
    """Render a unified diff between two saved version profiles."""
    profile_a = _render_profile(version_a["profile"])
    profile_b = _render_profile(version_b["profile"])

    diff_lines = list(
        difflib.unified_diff(
            profile_a,
            profile_b,
            fromfile=version_a["version_id"],
            tofile=version_b["version_id"],
            lineterm="",
        )
    )

    return "\n".join(diff_lines)


def _find_variant(variants: list[dict[str, Any]], variant_id: str) -> dict[str, Any]:
    for variant in variants:
        if variant["id"] == variant_id:
            return variant
    raise ValueError(f"Variant not found in rewrite artifact: {variant_id}")


def _build_version_id(lens: str, variant_id: str) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    return f"{timestamp}-{lens}-{variant_id}"


def _render_profile(profile: dict[str, Any]) -> list[str]:
    lines = [
        "# Headline",
        profile["headline"],
        "",
        "# About",
        profile["about"],
        "",
        "# Experience",
    ]

    for item in profile["experience"]:
        lines.extend(
            [
                f"## {item['title']} | {item['company']}",
                item["description"],
                "",
            ]
        )

    return lines
