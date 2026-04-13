#!/usr/bin/env python3
"""Install the full studio layer into a target repository."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _installer_lib import (  # noqa: E402
    InstallerError,
    default_codex_home,
    install_repo_studio,
    resolve_source_repo,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install the full Codex Code Game Studios repo layer into a target repository."
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Target repository root to bootstrap.",
    )
    parser.add_argument(
        "--codex-home",
        default=None,
        help="Codex home used to resolve the stored source repo metadata.",
    )
    parser.add_argument(
        "--source-repo",
        default=None,
        help="Path to the Codex-Code-Game-Studios source repo.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview actions without copying files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite conflicting files in the target repository.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    codex_home = (
        Path(args.codex_home).expanduser().resolve()
        if args.codex_home
        else default_codex_home()
    )
    target_root = Path(args.target).expanduser().resolve()

    try:
        repo_root = resolve_source_repo(
            Path(__file__),
            source_repo=args.source_repo,
            codex_home=codex_home,
        )
        actions, conflicts = install_repo_studio(
            repo_root,
            target_root,
            dry_run=args.dry_run,
            force=args.force,
        )
    except InstallerError as exc:
        parser.error(str(exc))
        return 2

    for action in actions:
        print(action)

    if conflicts:
        print("")
        print("Conflicts detected:")
        for conflict in conflicts:
            print(f"- {conflict}")
        print("")
        print("Re-run with --force if you want to overwrite those files.")
        return 1

    if args.dry_run:
        print("")
        print("Dry run complete.")
    else:
        print("")
        print(f"Studio layer installed into {target_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
