"""CLI entry point for the LinkedIn Positioning System."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .schema import validate_profile
from .storage import create_sample_profile, init_workspace, read_profile


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

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
