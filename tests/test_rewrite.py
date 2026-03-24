import json
from pathlib import Path

from lps.cli import main
from lps.rewrite import rewrite_profile
from lps.storage import write_profile


def _source_profile() -> dict[str, object]:
    return {
        "headline": "AI Transformation Leader",
        "about": "I lead AI products, delivery programs, and operating change across enterprise teams.",
        "experience": [
            {
                "title": "Director, AI",
                "company": "ExampleCorp",
                "description": (
                    "Led AI strategy and execution across product and delivery teams, reducing support load by 30%."
                ),
            },
            {
                "title": "Principal Consultant",
                "company": "AdvisoryCo",
                "description": "Delivered transformation programs for enterprise clients.",
            },
        ],
    }


def test_rewrite_profile_generates_two_variants() -> None:
    artifact = rewrite_profile(_source_profile(), "ai", "profile.json")

    assert len(artifact["variants"]) == 2
    assert artifact["variants"][0]["profile"]["headline"]
    assert len(artifact["variants"][0]["profile"]["experience"]) == 2
    assert len(artifact["factuality_checklist"]) >= 3


def test_rewrite_profile_preserves_titles_and_companies() -> None:
    artifact = rewrite_profile(_source_profile(), "consulting", "profile.json")
    first_variant = artifact["variants"][0]["profile"]

    assert first_variant["experience"][0]["title"] == "Director, AI"
    assert first_variant["experience"][0]["company"] == "ExampleCorp"


def test_cli_rewrite_writes_artifact_json(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    profile_path = write_profile("rewrite-target", _source_profile(), base_dir=workspace)

    exit_code = main(
        [
            "rewrite",
            str(profile_path),
            "--lens",
            "transformation",
            "--workspace",
            str(workspace),
        ]
    )

    assert exit_code == 0
    artifact = json.loads((workspace / "rewrites" / "rewrite-target-transformation.json").read_text())
    assert artifact["lens"] == "transformation"
    assert len(artifact["variants"]) == 2


def test_cli_rewrite_rejects_invalid_profile(tmp_path: Path) -> None:
    invalid_profile = tmp_path / "invalid.json"
    invalid_profile.write_text('{"headline": "Example"}\n', encoding="utf-8")

    exit_code = main(["rewrite", str(invalid_profile), "--lens", "ai", "--workspace", str(tmp_path)])

    assert exit_code == 1
