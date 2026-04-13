#!/usr/bin/env python3
"""Universal bootstrap for the global pack and repo-local studio layer."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _installer_lib import (  # noqa: E402
    CodexHomeSelection,
    InstallerError,
    default_codex_home,
    detect_git_root,
    install_global_pack,
    install_repo_studio,
    resolve_codex_home,
    resolve_source_repo,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Install the Codex Code Game Studios global pack and, when run "
            "inside a git repo, bootstrap the full studio into that repo."
        )
    )
    parser.add_argument(
        "--codex-home",
        default=None,
        help="Override the target Codex home. Defaults to smart platform-aware detection.",
    )
    parser.add_argument(
        "--source-repo",
        default=None,
        help="Path to the Codex-Code-Game-Studios source repo.",
    )
    parser.add_argument(
        "--target",
        default=None,
        help="Target repository root to bootstrap. Defaults to the current git root when available.",
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
    parser.add_argument(
        "--global-only",
        action="store_true",
        help="Install only the global pack and skip repo bootstrap.",
    )
    parser.add_argument(
        "--repo-only",
        action="store_true",
        help="Skip global-pack installation and bootstrap only the target repo.",
    )
    return parser


def choose_codex_home(args: argparse.Namespace) -> CodexHomeSelection:
    if args.codex_home:
        return CodexHomeSelection(
            Path(args.codex_home).expanduser().resolve(),
            "explicit-argument",
        )
    return resolve_codex_home()


def print_actions(stage: str, actions: list[str]) -> None:
    for action in actions:
        print(f"[{stage}] {action}")


def print_conflicts(stage: str, conflicts: list[str]) -> None:
    if not conflicts:
        return
    print("")
    print(f"{stage} conflicts detected:")
    for conflict in conflicts:
        print(f"- {conflict}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.global_only and args.repo_only:
        parser.error("--global-only and --repo-only cannot be used together")

    codex_home_selection = choose_codex_home(args)
    codex_home = codex_home_selection.path if not args.repo_only else (
        Path(args.codex_home).expanduser().resolve()
        if args.codex_home
        else default_codex_home()
    )

    try:
        source_repo = resolve_source_repo(
            Path(__file__),
            source_repo=args.source_repo,
            codex_home=codex_home,
        )
    except InstallerError as exc:
        parser.error(str(exc))
        return 2

    target_repo: Path | None = None
    if args.target:
        target_repo = Path(args.target).expanduser().resolve()
    elif not args.global_only:
        target_repo = detect_git_root(Path.cwd())

    if args.repo_only and target_repo is None:
        parser.error(
            "No git repository detected. Run inside a git repo or pass --target."
        )

    global_actions: list[str] = []
    global_conflicts: list[str] = []
    repo_actions: list[str] = []
    repo_conflicts: list[str] = []

    try:
        if not args.repo_only:
            global_actions, global_conflicts = install_global_pack(
                source_repo,
                codex_home,
                dry_run=args.dry_run,
                force=args.force,
            )
            print_actions("global", global_actions)

        if not args.global_only and target_repo is not None:
            repo_actions, repo_conflicts = install_repo_studio(
                source_repo,
                target_repo,
                dry_run=args.dry_run,
                force=args.force,
            )
            print_actions("repo", repo_actions)
    except InstallerError as exc:
        parser.error(str(exc))
        return 2

    print_conflicts("Global install", global_conflicts)
    print_conflicts("Repository bootstrap", repo_conflicts)
    if global_conflicts or repo_conflicts:
        print("")
        print("Re-run with --force if you want to overwrite those files.")
        return 1

    print("")
    print(f"Source repo: {source_repo}")
    if not args.repo_only:
        print(
            f"Codex home: {codex_home} ({codex_home_selection.strategy})"
        )
    if target_repo is not None and not args.global_only:
        print(f"Repo target: {target_repo}")
        next_step = "Next: open Codex there and start with $start or $help."
    elif args.global_only or target_repo is None:
        next_step = (
            "Next: run this bootstrap inside a git repository to install the full studio there."
        )
    else:
        next_step = "Next: run Codex in the target repo."

    if args.dry_run:
        print("Dry run complete.")
    else:
        if args.repo_only:
            print("Repository bootstrap complete.")
        elif target_repo is None or args.global_only:
            print("Global bootstrap complete.")
        else:
            print("Global bootstrap and repository bootstrap complete.")
    print(next_step)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
