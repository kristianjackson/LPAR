import json
from pathlib import Path

from lps.cli import main
from lps.rewrite import rewrite_profile
from lps.storage import write_profile
from lps.versioning import create_version_record, render_version_diff


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


def test_create_version_record_selects_requested_variant() -> None:
    artifact = rewrite_profile(_source_profile(), "ai", "rewrite.json")
    record = create_version_record(artifact, "ai-core", "rewrite.json")

    assert record["variant_id"] == "ai-core"
    assert record["profile"]["headline"]


def test_render_version_diff_contains_changed_sections() -> None:
    artifact = rewrite_profile(_source_profile(), "ai", "rewrite.json")
    version_a = create_version_record(artifact, "ai-core", "rewrite.json")
    version_b = create_version_record(artifact, "ai-operator", "rewrite.json")

    diff = render_version_diff(version_a, version_b)

    assert "--- " in diff
    assert "+++ " in diff
    assert "# Headline" in diff


def test_cli_versions_save_and_list(tmp_path: Path, capsys) -> None:
    workspace = tmp_path / "workspace"
    profile_path = write_profile("version-target", _source_profile(), base_dir=workspace)

    assert main(["rewrite", str(profile_path), "--lens", "ai", "--workspace", str(workspace)]) == 0
    rewrite_path = workspace / "rewrites" / "version-target-ai.json"

    save_exit = main(
        [
            "versions",
            "save",
            str(rewrite_path),
            "--variant-id",
            "ai-core",
            "--workspace",
            str(workspace),
        ]
    )

    assert save_exit == 0
    version_files = list((workspace / "versions").glob("*.json"))
    assert len(version_files) == 1

    list_exit = main(["versions", "list", "--workspace", str(workspace)])

    assert list_exit == 0
    output = capsys.readouterr().out
    assert "ai-core" in output


def test_cli_diff_outputs_saved_version_diff(tmp_path: Path, capsys) -> None:
    workspace = tmp_path / "workspace"
    profile_path = write_profile("version-target", _source_profile(), base_dir=workspace)

    assert main(["rewrite", str(profile_path), "--lens", "ai", "--workspace", str(workspace)]) == 0
    rewrite_path = workspace / "rewrites" / "version-target-ai.json"

    assert (
        main(
            [
                "versions",
                "save",
                str(rewrite_path),
                "--variant-id",
                "ai-core",
                "--workspace",
                str(workspace),
            ]
        )
        == 0
    )
    assert (
        main(
            [
                "versions",
                "save",
                str(rewrite_path),
                "--variant-id",
                "ai-operator",
                "--workspace",
                str(workspace),
            ]
        )
        == 0
    )

    version_ids = [
        json.loads(path.read_text(encoding="utf-8"))["version_id"]
        for path in (workspace / "versions").glob("*.json")
    ]
    version_ids.sort()

    diff_exit = main(["diff", version_ids[0], version_ids[1], "--workspace", str(workspace)])

    assert diff_exit == 0
    output = capsys.readouterr().out
    assert "--- " in output
    assert "+++ " in output
