import json
from pathlib import Path

from lps.cli import main
from lps.content import generate_content_bundle
from lps.rewrite import rewrite_profile
from lps.storage import write_profile, write_version_record
from lps.versioning import create_version_record


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


def _version_record() -> dict[str, object]:
    artifact = rewrite_profile(_source_profile(), "ai", "rewrite.json")
    return create_version_record(artifact, "ai-core", "rewrite.json")


def test_generate_content_bundle_returns_mvp_counts() -> None:
    bundle = generate_content_bundle(_version_record())

    assert len(bundle["ideas"]) == 10
    assert len(bundle["post_drafts"]) == 3
    assert len(bundle["outreach_drafts"]) == 3
    assert bundle["lens"] == "ai"


def test_cli_content_writes_artifact_json(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    profile_path = write_profile("content-target", _source_profile(), base_dir=workspace)
    assert main(["rewrite", str(profile_path), "--lens", "ai", "--workspace", str(workspace)]) == 0

    rewrite_artifact = json.loads((workspace / "rewrites" / "content-target-ai.json").read_text())
    version_record = create_version_record(
        rewrite_artifact,
        "ai-core",
        str(workspace / "rewrites" / "content-target-ai.json"),
    )
    write_version_record(version_record["version_id"], version_record, base_dir=workspace)

    exit_code = main(["content", version_record["version_id"], "--workspace", str(workspace)])

    assert exit_code == 0
    artifact = json.loads((workspace / "content" / f"{version_record['version_id']}.json").read_text())
    assert len(artifact["ideas"]) == 10
    assert len(artifact["post_drafts"]) == 3


def test_cli_content_rejects_missing_version(tmp_path: Path) -> None:
    exit_code = main(["content", "missing-version", "--workspace", str(tmp_path)])

    assert exit_code == 1
