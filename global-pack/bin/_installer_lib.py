#!/usr/bin/env python3
"""Shared helpers for the hybrid global installer."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
from typing import Callable


METADATA_FILENAME = "codex-game-studios-install.json"


class InstallerError(RuntimeError):
    """Raised when installer inputs or state are invalid."""


@dataclass(frozen=True)
class CodexHomeSelection:
    """Selected Codex home plus the strategy used to choose it."""

    path: Path
    strategy: str


def is_windows_platform(platform: str | None = None) -> bool:
    platform_value = platform or sys.platform
    return platform_value.startswith("win")


def is_wsl_environment(
    env: dict[str, str] | None = None,
    proc_version_path: Path | None = None,
) -> bool:
    env_map = os.environ if env is None else env
    if env_map.get("WSL_DISTRO_NAME") or env_map.get("WSL_INTEROP"):
        return True

    version_path = proc_version_path or Path("/proc/version")
    try:
        version_text = version_path.read_text(encoding="utf-8").lower()
    except OSError:
        return False
    return "microsoft" in version_text or "wsl" in version_text


def windows_codex_home_from_env(env: dict[str, str] | None = None) -> Path | None:
    env_map = os.environ if env is None else env
    user_profile = env_map.get("USERPROFILE")
    if user_profile:
        return Path(user_profile).expanduser() / ".codex"

    home_drive = env_map.get("HOMEDRIVE")
    home_path = env_map.get("HOMEPATH")
    if home_drive and home_path:
        return Path(f"{home_drive}{home_path}") / ".codex"
    return None


def resolve_codex_home(
    *,
    env: dict[str, str] | None = None,
    platform: str | None = None,
    proc_version_path: Path | None = None,
    path_exists: Callable[[Path], bool] | None = None,
    home_path: Path | None = None,
) -> CodexHomeSelection:
    env_map = os.environ if env is None else env
    exists = path_exists or (lambda path: path.exists())
    user_home = (home_path or Path.home()).expanduser().resolve()

    env_value = env_map.get("CODEX_HOME")
    if env_value:
        return CodexHomeSelection(
            Path(env_value).expanduser().resolve(),
            "explicit-codex-home",
        )

    if is_windows_platform(platform):
        windows_home = windows_codex_home_from_env(env_map)
        if windows_home is not None:
            return CodexHomeSelection(
                windows_home.expanduser().resolve(),
                "windows-home",
            )
        return CodexHomeSelection((user_home / ".codex").resolve(), "windows-fallback")

    if is_wsl_environment(env_map, proc_version_path=proc_version_path):
        shared_home = windows_codex_home_from_env(env_map)
        if shared_home is not None and exists(shared_home):
            return CodexHomeSelection(
                shared_home.expanduser().resolve(),
                "wsl-shared-windows-home",
            )
        return CodexHomeSelection((user_home / ".codex").resolve(), "wsl-linux-home")

    return CodexHomeSelection((user_home / ".codex").resolve(), "platform-default-home")


def default_codex_home() -> Path:
    return resolve_codex_home().path


def metadata_path(codex_home: Path) -> Path:
    return codex_home / METADATA_FILENAME


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_manifest(repo_root: Path) -> dict:
    manifest_path = repo_root / "global-pack" / "manifest.json"
    if not manifest_path.exists():
        raise InstallerError(f"Missing manifest: {manifest_path}")
    return load_json(manifest_path)


def detect_git_root(start_path: Path | None = None) -> Path | None:
    cwd = (start_path or Path.cwd()).resolve()
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    stdout = result.stdout.strip()
    if not stdout:
        return None
    return Path(stdout).resolve()


def resolve_source_repo(
    script_path: Path,
    source_repo: str | None = None,
    codex_home: Path | None = None,
) -> Path:
    if source_repo:
        repo_root = Path(source_repo).expanduser().resolve()
        if not (repo_root / "global-pack" / "manifest.json").exists():
            raise InstallerError(
                f"{repo_root} is not a Codex Code Game Studios source repo"
            )
        return repo_root

    repo_candidate = script_path.resolve().parents[2]
    if (repo_candidate / "global-pack" / "manifest.json").exists():
        return repo_candidate

    home = (codex_home or default_codex_home()).resolve()
    install_metadata = metadata_path(home)
    if install_metadata.exists():
        payload = load_json(install_metadata)
        repo_root = Path(payload["source_repo"]).expanduser().resolve()
        if (repo_root / "global-pack" / "manifest.json").exists():
            return repo_root

    raise InstallerError(
        "Unable to resolve the source studio repo. Re-run the installer from the "
        "Codex-Code-Game-Studios clone or pass --source-repo explicitly."
    )


def ensure_directory(path: Path, actions: list[str], dry_run: bool) -> None:
    if path.exists():
        return
    actions.append(f"mkdir {path}")
    if not dry_run:
        path.mkdir(parents=True, exist_ok=True)


def files_identical(source: Path, target: Path) -> bool:
    if not target.exists() or source.stat().st_size != target.stat().st_size:
        return False
    return source.read_bytes() == target.read_bytes()


def copy_file(
    source: Path,
    target: Path,
    *,
    dry_run: bool,
    force: bool,
    actions: list[str],
    conflicts: list[str],
) -> None:
    if target.exists():
        if files_identical(source, target):
            actions.append(f"skip-identical {target}")
            return
        if not force:
            conflicts.append(str(target))
            return

    actions.append(f"copy {source} -> {target}")
    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def copy_tree(
    source_dir: Path,
    target_dir: Path,
    *,
    dry_run: bool,
    force: bool,
    actions: list[str],
    conflicts: list[str],
) -> None:
    for source_path in sorted(source_dir.rglob("*")):
        if source_path.is_dir():
            continue
        relative_path = source_path.relative_to(source_dir)
        copy_file(
            source_path,
            target_dir / relative_path,
            dry_run=dry_run,
            force=force,
            actions=actions,
            conflicts=conflicts,
        )


def write_metadata(
    repo_root: Path,
    codex_home: Path,
    *,
    dry_run: bool,
    actions: list[str],
) -> None:
    payload = {
        "pack_name": "Codex Code Game Studios",
        "source_repo": str(repo_root),
    }
    target = metadata_path(codex_home)
    actions.append(f"write {target}")
    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def install_global_pack(
    repo_root: Path,
    codex_home: Path,
    *,
    dry_run: bool,
    force: bool,
) -> tuple[list[str], list[str]]:
    manifest = load_manifest(repo_root)
    actions: list[str] = []
    conflicts: list[str] = []

    ensure_directory(codex_home, actions, dry_run)
    ensure_directory(codex_home / "skills", actions, dry_run)
    ensure_directory(codex_home / "agents", actions, dry_run)
    ensure_directory(codex_home / "bin", actions, dry_run)

    for skill_name in manifest["global_skills"]:
        copy_tree(
            repo_root / "global-pack" / "skills" / skill_name,
            codex_home / "skills" / skill_name,
            dry_run=dry_run,
            force=force,
            actions=actions,
            conflicts=conflicts,
        )

    for agent_name in manifest["global_agents"]:
        copy_file(
            repo_root / "global-pack" / "agents" / agent_name,
            codex_home / "agents" / agent_name,
            dry_run=dry_run,
            force=force,
            actions=actions,
            conflicts=conflicts,
        )

    for bin_name in manifest["bin_files"]:
        copy_file(
            repo_root / "global-pack" / "bin" / bin_name,
            codex_home / "bin" / bin_name,
            dry_run=dry_run,
            force=force,
            actions=actions,
            conflicts=conflicts,
        )

    if not conflicts:
        write_metadata(repo_root, codex_home, dry_run=dry_run, actions=actions)

    return actions, conflicts


def install_repo_studio(
    repo_root: Path,
    target_root: Path,
    *,
    dry_run: bool,
    force: bool,
) -> tuple[list[str], list[str]]:
    manifest = load_manifest(repo_root)
    actions: list[str] = []
    conflicts: list[str] = []

    ensure_directory(target_root, actions, dry_run)

    for starter_dir in manifest["starter_dirs"]:
        ensure_directory(target_root / starter_dir, actions, dry_run)

    for relative_path in manifest["repo_files"]:
        copy_file(
            repo_root / relative_path,
            target_root / relative_path,
            dry_run=dry_run,
            force=force,
            actions=actions,
            conflicts=conflicts,
        )

    for relative_path in manifest["repo_nested_guides"]:
        copy_file(
            repo_root / relative_path,
            target_root / relative_path,
            dry_run=dry_run,
            force=force,
            actions=actions,
            conflicts=conflicts,
        )

    for relative_dir in manifest["repo_dirs"]:
        copy_tree(
            repo_root / relative_dir,
            target_root / relative_dir,
            dry_run=dry_run,
            force=force,
            actions=actions,
            conflicts=conflicts,
        )

    return actions, conflicts
