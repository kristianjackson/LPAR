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
    write_version_record,
    write_profile,
)
from .versioning import create_version_record, list_version_records, read_version_record, render_version_diff


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


def cmd_versions_save(args: argparse.Namespace) -> int:
    rewrite_path = Path(args.path)

    try:
        rewrite_artifact = json.loads(rewrite_path.read_text(encoding="utf-8"))
        record = create_version_record(rewrite_artifact, args.variant_id, str(rewrite_path))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Version save failed: {exc}")
        return 1

    workspace = init_workspace(Path(args.workspace))
    target = write_version_record(record["version_id"], record, base_dir=workspace)
    print(f"Saved version: {record['version_id']}")
    print(f"Version record saved to: {target}")
    return 0


def cmd_versions_list(args: argparse.Namespace) -> int:
    records = list_version_records(Path(args.workspace))
    if not records:
        print("No saved versions found.")
        return 0

    for record in records:
        print(
            f"{record['version_id']} | {record['lens']} | {record['variant_id']} | {record['saved_at']}"
        )
    return 0


def cmd_versions_show(args: argparse.Namespace) -> int:
    try:
        record = read_version_record(Path(args.workspace), args.version_id)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Version show failed: {exc}")
        return 1

    print(json.dumps(record, indent=2))
    return 0


def cmd_diff(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace)

    try:
        version_a = read_version_record(workspace, args.version_a)
        version_b = read_version_record(workspace, args.version_b)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Diff failed: {exc}")
        return 1

    print(render_version_diff(version_a, version_b))
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

    versions_cmd = subparsers.add_parser("versions", help="Manage saved profile versions")
    versions_subparsers = versions_cmd.add_subparsers(dest="versions_command", required=True)

    versions_save_cmd = versions_subparsers.add_parser("save", help="Save a rewrite variant as a version")
    versions_save_cmd.add_argument("path", help="Path to rewrite artifact JSON file")
    versions_save_cmd.add_argument("--variant-id", required=True, help="Variant identifier to save")
    versions_save_cmd.add_argument("--workspace", default=".lps", help="Workspace directory path")
    versions_save_cmd.set_defaults(func=cmd_versions_save)

    versions_list_cmd = versions_subparsers.add_parser("list", help="List saved versions")
    versions_list_cmd.add_argument("--workspace", default=".lps", help="Workspace directory path")
    versions_list_cmd.set_defaults(func=cmd_versions_list)

    versions_show_cmd = versions_subparsers.add_parser("show", help="Show a saved version record")
    versions_show_cmd.add_argument("version_id", help="Saved version identifier")
    versions_show_cmd.add_argument("--workspace", default=".lps", help="Workspace directory path")
    versions_show_cmd.set_defaults(func=cmd_versions_show)

    diff_cmd = subparsers.add_parser("diff", help="Diff two saved versions")
    diff_cmd.add_argument("version_a", help="First saved version identifier")
    diff_cmd.add_argument("version_b", help="Second saved version identifier")
    diff_cmd.add_argument("--workspace", default=".lps", help="Workspace directory path")
    diff_cmd.set_defaults(func=cmd_diff)

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
