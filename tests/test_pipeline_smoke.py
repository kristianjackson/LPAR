import json
from pathlib import Path

from lps.cli import main


FIXTURES = Path(__file__).parent / "fixtures"


def test_full_cli_pipeline_smoke(tmp_path: Path, capsys) -> None:
    workspace = tmp_path / "workspace"
    source_markdown = FIXTURES / "sample_profile.md"

    assert main(["init", "--workspace", str(workspace), "--profile-name", "starter"]) == 0

    assert (
        main(
            [
                "ingest",
                "--format",
                "markdown",
                "--input",
                str(source_markdown),
                "--workspace",
                str(workspace),
                "--profile-name",
                "pipeline",
            ]
        )
        == 0
    )

    profile_path = workspace / "profiles" / "pipeline.json"
    assert main(["validate", str(profile_path)]) == 0
    assert main(["analyze", str(profile_path), "--lens", "ai", "--workspace", str(workspace)]) == 0
    assert main(["rewrite", str(profile_path), "--lens", "ai", "--workspace", str(workspace)]) == 0

    rewrite_path = workspace / "rewrites" / "pipeline-ai.json"
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

    version_ids = sorted(
        json.loads(path.read_text(encoding="utf-8"))["version_id"]
        for path in (workspace / "versions").glob("*.json")
    )
    assert len(version_ids) == 2

    assert main(["versions", "list", "--workspace", str(workspace)]) == 0
    assert main(["versions", "show", version_ids[0], "--workspace", str(workspace)]) == 0
    assert main(["diff", version_ids[0], version_ids[1], "--workspace", str(workspace)]) == 0

    diff_output = capsys.readouterr().out
    assert "--- " in diff_output
    assert "+++ " in diff_output

    assert main(["content", version_ids[0], "--workspace", str(workspace)]) == 0

    content_artifact = json.loads(
        (workspace / "content" / f"{version_ids[0]}.json").read_text(encoding="utf-8")
    )
    assert len(content_artifact["ideas"]) == 10
    assert len(content_artifact["post_drafts"]) == 3
    assert len(content_artifact["outreach_drafts"]) == 3
