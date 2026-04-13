#!/usr/bin/env python3
"""End-to-end validation for the hybrid global installer."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALL_GLOBAL = REPO_ROOT / "global-pack" / "bin" / "install_global_pack.py"


def run(
    command: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"Command failed ({result.returncode}): {' '.join(command)}\n"
            f"stdout:\n{result.stdout}\n\nstderr:\n{result.stderr}"
        )
    return result


def assert_exists(path: Path) -> None:
    if not path.exists():
        raise AssertionError(f"Expected path to exist: {path}")


def is_runtime_auth_issue(text: str) -> bool:
    needles = (
        "401 Unauthorized",
        "Missing bearer",
        "authentication required",
        "failed to connect to websocket",
        "stream disconnected - retrying",
    )
    return any(needle in text for needle in needles)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="codex-global-home-") as home_dir, tempfile.TemporaryDirectory(
        prefix="codex-global-target-"
    ) as repo_dir:
        codex_home = Path(home_dir) / ".codex"
        target_repo = Path(repo_dir) / "game-repo"
        target_repo.mkdir(parents=True, exist_ok=True)

        run(
            [
                sys.executable,
                str(INSTALL_GLOBAL),
                "--codex-home",
                str(codex_home),
                "--source-repo",
                str(REPO_ROOT),
            ]
        )

        assert_exists(codex_home / "skills" / "studio-help" / "SKILL.md")
        assert_exists(codex_home / "skills" / "install-studio" / "SKILL.md")
        assert_exists(codex_home / "skills" / "adopt-studio" / "SKILL.md")
        assert_exists(codex_home / "agents" / "studio-bootstrapper.toml")
        assert_exists(codex_home / "bin" / "install_repo_studio.py")
        assert_exists(codex_home / "codex-game-studios-install.json")

        run(["git", "init"], cwd=target_repo)

        run(
            [
                sys.executable,
                str(codex_home / "bin" / "install_repo_studio.py"),
                "--codex-home",
                str(codex_home),
                "--target",
                str(target_repo),
            ]
        )

        expected_repo_paths = [
            target_repo / "AGENTS.md",
            target_repo / ".agents" / "skills" / "start" / "SKILL.md",
            target_repo / ".codex" / "agents" / "producer.toml",
            target_repo / "docs" / "studio" / "workflow-catalog.yaml",
            target_repo / "docs" / "WORKFLOW-GUIDE.md",
            target_repo / "design" / "AGENTS.md",
            target_repo / "src" / "AGENTS.md",
            target_repo / "tests" / "AGENTS.md",
            target_repo / "production" / "releases" / "steam",
        ]
        for path in expected_repo_paths:
            assert_exists(path)

        codex_path = shutil.which("codex")
        if codex_path:
            env = os.environ.copy()
            env["CODEX_HOME"] = str(codex_home)

            global_prompt = run(
                [codex_path, "debug", "prompt-input"],
                cwd=Path(repo_dir),
                env=env,
            )
            global_text = global_prompt.stdout + global_prompt.stderr
            if "studio-help" not in global_text:
                raise AssertionError("Expected studio-help in global prompt context")

            try:
                global_exec = run(
                    [
                        codex_path,
                        "exec",
                        "--skip-git-repo-check",
                        "-s",
                        "read-only",
                        "Use $adopt-studio to audit whether this directory is ready for Codex Code Game Studios. Reply with exactly one line: STATUS: NOT_INSTALLED or STATUS: READY. Do not write files.",
                    ],
                    cwd=Path(repo_dir),
                    env=env,
                )
                global_exec_text = global_exec.stdout + global_exec.stderr
                if "STATUS:" not in global_exec_text:
                    raise AssertionError(
                        "Expected STATUS output from $adopt-studio runtime probe"
                    )
            except AssertionError as exc:
                if not is_runtime_auth_issue(str(exc)):
                    raise
                print("Skipped live global skill probe because Codex auth was unavailable in the temporary CODEX_HOME.")

            repo_prompt = run(
                [codex_path, "debug", "prompt-input"],
                cwd=target_repo,
                env=env,
            )
            repo_text = repo_prompt.stdout + repo_prompt.stderr
            if "start" not in repo_text:
                raise AssertionError("Expected start in installed repo prompt context")

            try:
                repo_exec = run(
                    [
                        codex_path,
                        "exec",
                        "-s",
                        "read-only",
                        "Use $help to inspect this repo and reply with exactly one line starting with STATUS:. Do not write files.",
                    ],
                    cwd=target_repo,
                    env=env,
                )
                repo_exec_text = repo_exec.stdout + repo_exec.stderr
                if "STATUS:" not in repo_exec_text:
                    raise AssertionError(
                        "Expected STATUS output from repo-local $help runtime probe"
                    )
            except AssertionError as exc:
                if not is_runtime_auth_issue(str(exc)):
                    raise
                print("Skipped live repo skill probe because Codex auth was unavailable in the temporary CODEX_HOME.")

        print("Hybrid global installer validation passed.")
        print(f"Codex home: {codex_home}")
        print(f"Target repo: {target_repo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
