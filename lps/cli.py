"""CLI entry point for the LinkedIn Positioning System."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .analysis import analyze_profile
from .ingestion import IngestionError, parse_profile_text
from .rewrite import rewrite_profile
from .schema import validate_profile
from .storage import (
    create_sample_profile,
    init_workspace,
    read_profile,
    write_analysis_report,
    write_rewrite_artifact,
    write_profile,
)


def cmd_init(args: argparse.Namespace) -> int:
    workspace = init_workspace(Path(args.workspace))
    sample_path = create_sample_profile(profile_name=args.profile_name, base_dir=workspace)
    print(f"Initialized workspace at: {workspace}")
    print(f"Created sample profile: {sample_path}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    profile = read_profile(Path(args.path))
    errors = validate_profile(profile)

    if errors:
        print("Profile validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Profile validation passed.")
    return 0


def cmd_ingest(args: argparse.Namespace) -> int:
    try:
        source_text = _read_ingest_source(args.input)
        profile = parse_profile_text(source_text, args.format)
    except (IngestionError, OSError) as exc:
        print(f"Profile ingestion failed: {exc}")
        return 1

    errors = validate_profile(profile)
    if errors:
        print("Profile ingestion failed validation:")
        for error in errors:
            print(f"- {error}")
        return 1

    workspace = init_workspace(Path(args.workspace))
    target = write_profile(args.profile_name, profile, base_dir=workspace)
    print(f"Ingested profile saved to: {target}")
    return 0


def cmd_analyze(args: argparse.Namespace) -> int:
    profile_path = Path(args.path)

    try:
        profile = read_profile(profile_path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Profile analysis failed: {exc}")
        return 1

    errors = validate_profile(profile)
    if errors:
        print("Profile analysis failed validation:")
        for error in errors:
            print(f"- {error}")
        return 1

    report = analyze_profile(profile, args.lens, str(profile_path))
    workspace = init_workspace(Path(args.workspace))
    report_name = f"{profile_path.stem}-{args.lens}"
    target = write_analysis_report(report_name, report, base_dir=workspace)

    print(f"Analysis report saved to: {target}")
    print(f"Lens: {report['lens_label']}")
    print("Scores:")
    for score_name, score_value in report["scores"].items():
        print(f"- {score_name}: {score_value}")
    return 0


def cmd_rewrite(args: argparse.Namespace) -> int:
    profile_path = Path(args.path)

    try:
        profile = read_profile(profile_path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Profile rewrite failed: {exc}")
        return 1

    errors = validate_profile(profile)
    if errors:
        print("Profile rewrite failed validation:")
        for error in errors:
            print(f"- {error}")
        return 1

    artifact = rewrite_profile(profile, args.lens, str(profile_path))
    workspace = init_workspace(Path(args.workspace))
    artifact_name = f"{profile_path.stem}-{args.lens}"
    target = write_rewrite_artifact(artifact_name, artifact, base_dir=workspace)

    print(f"Rewrite artifact saved to: {target}")
    print(f"Lens: {artifact['lens_label']}")
    print("Variants:")
    for variant in artifact["variants"]:
        print(f"- {variant['label']}")
    return 0


def _read_ingest_source(input_path: str | None) -> str:
    if input_path:
        return Path(input_path).read_text(encoding="utf-8")

    if getattr(sys.stdin, "isatty", lambda: False)():
        raise IngestionError("No input provided. Pass --input or pipe content on stdin.")

    source_text = sys.stdin.read()
    if not source_text.strip():
        raise IngestionError("No input provided. Pass --input or pipe content on stdin.")
    return source_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="lps", description="LinkedIn Positioning System CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_cmd = subparsers.add_parser("init", help="Initialize local workspace")
    init_cmd.add_argument("--workspace", default=".lps", help="Workspace directory path")
    init_cmd.add_argument("--profile-name", default="default", help="Sample profile filename stem")
    init_cmd.set_defaults(func=cmd_init)

    validate_cmd = subparsers.add_parser("validate", help="Validate a profile JSON document")
    validate_cmd.add_argument("path", help="Path to profile JSON file")
    validate_cmd.set_defaults(func=cmd_validate)

    analyze_cmd = subparsers.add_parser("analyze", help="Analyze a profile JSON document")
    analyze_cmd.add_argument("path", help="Path to profile JSON file")
    analyze_cmd.add_argument(
        "--lens",
        choices=("ai", "transformation", "consulting"),
        required=True,
        help="Positioning lens to analyze against",
    )
    analyze_cmd.add_argument("--workspace", default=".lps", help="Workspace directory path")
    analyze_cmd.set_defaults(func=cmd_analyze)

    rewrite_cmd = subparsers.add_parser("rewrite", help="Rewrite a profile JSON document")
    rewrite_cmd.add_argument("path", help="Path to profile JSON file")
    rewrite_cmd.add_argument(
        "--lens",
        choices=("ai", "transformation", "consulting"),
        required=True,
        help="Positioning lens to rewrite for",
    )
    rewrite_cmd.add_argument("--workspace", default=".lps", help="Workspace directory path")
    rewrite_cmd.set_defaults(func=cmd_rewrite)

    ingest_cmd = subparsers.add_parser("ingest", help="Ingest profile content into schema v1")
    ingest_cmd.add_argument(
        "--format",
        choices=("markdown", "paste"),
        required=True,
        help="Ingestion format for the input content",
    )
    ingest_cmd.add_argument(
        "--input",
        help="Optional path to the input file; otherwise reads from stdin",
    )
    ingest_cmd.add_argument("--workspace", default=".lps", help="Workspace directory path")
    ingest_cmd.add_argument("--profile-name", default="default", help="Output profile filename stem")
    ingest_cmd.set_defaults(func=cmd_ingest)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
