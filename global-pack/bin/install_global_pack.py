#!/usr/bin/env python3
"""Install the curated global pack into a Codex home directory."""

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
    install_global_pack,
    resolve_source_repo,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install Codex Code Game Studios global skills and agents."
    )
    parser.add_argument(
        "--codex-home",
        default=None,
        help="Override the target Codex home. Defaults to $CODEX_HOME or ~/.codex.",
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
        help="Overwrite conflicting installed files.",
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

    try:
        repo_root = resolve_source_repo(
            Path(__file__),
            source_repo=args.source_repo,
            codex_home=codex_home,
        )
        actions, conflicts = install_global_pack(
            repo_root,
            codex_home,
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
        print(f"Global pack installed into {codex_home}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
