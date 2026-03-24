import io
import sys
from pathlib import Path

import pytest

from lps.cli import main
from lps.ingestion import IngestionError, parse_markdown_profile, parse_paste_profile
from lps.storage import read_profile


FIXTURES = Path(__file__).parent / "fixtures"


def _fixture_text(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_parse_markdown_profile_reads_core_sections() -> None:
    profile = parse_markdown_profile(_fixture_text("sample_profile.md"))

    assert profile["headline"] == "AI Transformation Leader"
    assert profile["about"] == (
        "I build AI products.\n\n"
        "I lead operating change across strategy, delivery, and adoption."
    )
    assert profile["experience"] == [
        {
            "title": "Director, AI",
            "company": "ExampleCorp",
            "description": "Led AI strategy and execution across product and delivery teams.",
        },
        {
            "title": "Principal Consultant",
            "company": "AdvisoryCo",
            "description": "Delivered transformation programs for enterprise clients.",
        },
    ]


def test_parse_paste_profile_reads_labeled_sections() -> None:
    profile = parse_paste_profile(_fixture_text("sample_profile_paste.txt"))

    assert profile["headline"] == "AI Transformation Leader"
    assert len(profile["experience"]) == 2
    assert profile["experience"][0]["company"] == "ExampleCorp"


def test_parse_markdown_profile_rejects_missing_required_section() -> None:
    with pytest.raises(IngestionError, match="missing the '# Experience' section"):
        parse_markdown_profile("# Headline\nExample\n\n# About\nExample")


def test_parse_paste_profile_rejects_invalid_experience_line() -> None:
    with pytest.raises(IngestionError, match="Paste experience lines must use"):
        parse_paste_profile(
            "Headline: Example\nAbout:\nExample\n\nExperience:\nDirector | ExampleCorp | Missing dash"
        )


def test_cli_ingest_markdown_writes_profile_json(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"

    exit_code = main(
        [
            "ingest",
            "--format",
            "markdown",
            "--input",
            str(FIXTURES / "sample_profile.md"),
            "--workspace",
            str(workspace),
            "--profile-name",
            "markdown-profile",
        ]
    )

    assert exit_code == 0
    profile = read_profile(workspace / "profiles" / "markdown-profile.json")
    assert profile["headline"] == "AI Transformation Leader"


def test_cli_ingest_paste_writes_profile_json(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"

    exit_code = main(
        [
            "ingest",
            "--format",
            "paste",
            "--input",
            str(FIXTURES / "sample_profile_paste.txt"),
            "--workspace",
            str(workspace),
            "--profile-name",
            "paste-profile",
        ]
    )

    assert exit_code == 0
    profile = read_profile(workspace / "profiles" / "paste-profile.json")
    assert profile["experience"][1]["title"] == "Principal Consultant"


def test_cli_ingest_reads_from_stdin(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    class FakeStdin(io.StringIO):
        def isatty(self) -> bool:
            return False

    workspace = tmp_path / "workspace"
    monkeypatch.setattr(sys, "stdin", FakeStdin(_fixture_text("sample_profile_paste.txt")))

    exit_code = main(
        [
            "ingest",
            "--format",
            "paste",
            "--workspace",
            str(workspace),
            "--profile-name",
            "stdin-profile",
        ]
    )

    assert exit_code == 0
    profile = read_profile(workspace / "profiles" / "stdin-profile.json")
    assert profile["headline"] == "AI Transformation Leader"
