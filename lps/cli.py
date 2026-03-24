"""CLI entry point for the LinkedIn Positioning System."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .ingestion import IngestionError, parse_profile_text
from .schema import validate_profile
from .storage import create_sample_profile, init_workspace, read_profile, write_profile


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
