import json
from pathlib import Path

from lps.analysis import analyze_profile
from lps.cli import main
from lps.storage import write_profile


def _strong_profile() -> dict[str, object]:
    return {
        "headline": "AI Transformation Leader | Enterprise Product and Delivery Executive",
        "about": (
            "I lead AI product strategy, model delivery, and adoption across enterprise teams. "
            "I build operating models, scale platforms, and drive measurable efficiency gains."
        ),
        "experience": [
            {
                "title": "Director, AI",
                "company": "ExampleCorp",
                "description": (
                    "Led AI roadmap and platform delivery for 4 product lines, reducing support load "
                    "by 30% and growing adoption to 12 teams."
                ),
            },
            {
                "title": "Principal Consultant",
                "company": "AdvisoryCo",
                "description": (
                    "Advised enterprise clients on AI operating models, automation programs, and "
                    "executive change plans."
                ),
            },
        ],
    }


def _weak_profile() -> dict[str, object]:
    return {
        "headline": "Leader",
        "about": "Experienced professional.",
        "experience": [
            {
                "title": "Manager",
                "company": "ExampleCorp",
                "description": "Worked on projects.",
            }
        ],
    }


def test_analyze_profile_returns_scores_and_ranked_findings() -> None:
    report = analyze_profile(_strong_profile(), "ai", "profile.json")

    assert report["scores"]["clarity"] >= 60
    assert report["scores"]["authority"] >= 50
    assert report["scores"]["lens_fit"] >= 60
    assert len(report["weaknesses"]) >= 3
    assert len(report["improvements"]) >= 3
    assert report["lens"] == "ai"


def test_analyze_profile_flags_weak_profile_for_selected_lens() -> None:
    report = analyze_profile(_weak_profile(), "consulting", "profile.json")

    assert report["scores"]["clarity"] < 60
    assert report["scores"]["authority"] < 50
    assert report["lens_gaps"]
    assert "consulting" in " ".join(report["lens_gaps"]).lower()


def test_cli_analyze_writes_report_json(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    profile_path = write_profile("analysis-target", _strong_profile(), base_dir=workspace)

    exit_code = main(
        [
            "analyze",
            str(profile_path),
            "--lens",
            "transformation",
            "--workspace",
            str(workspace),
        ]
    )

    assert exit_code == 0
    report = json.loads((workspace / "analysis" / "analysis-target-transformation.json").read_text())
    assert report["lens"] == "transformation"
    assert report["scores"]["clarity"] >= 60


def test_cli_analyze_rejects_invalid_profile(tmp_path: Path) -> None:
    invalid_profile = tmp_path / "invalid.json"
    invalid_profile.write_text('{"headline": "Example"}\n', encoding="utf-8")

    exit_code = main(["analyze", str(invalid_profile), "--lens", "ai", "--workspace", str(tmp_path)])

    assert exit_code == 1
