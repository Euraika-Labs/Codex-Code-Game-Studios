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
BOOTSTRAP = REPO_ROOT / "global-pack" / "bin" / "bootstrap.py"

sys.path.insert(0, str((REPO_ROOT / "global-pack" / "bin").resolve()))
from _installer_lib import resolve_codex_home  # noqa: E402


def run(
    command: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    timeout: float | None = None,
) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise AssertionError(
            f"Command timed out after {timeout}s: {' '.join(command)}\n"
            f"stdout:\n{exc.stdout or ''}\n\nstderr:\n{exc.stderr or ''}"
        ) from exc
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


def assert_equal(actual: object, expected: object, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}: expected {expected!r}, got {actual!r}")


def has_codex_auth(codex_home: Path) -> bool:
    return (codex_home / "auth.json").exists()


def test_codex_home_resolution() -> None:
    explicit = resolve_codex_home(
        env={"CODEX_HOME": "/tmp/custom-codex"},
        home_path=Path("/home/tester"),
    )
    assert_equal(explicit.strategy, "explicit-codex-home", "explicit CODEX_HOME strategy")
    assert_equal(explicit.path, Path("/tmp/custom-codex"), "explicit CODEX_HOME path")

    windows_native = resolve_codex_home(
        env={"USERPROFILE": "/windows-home/user"},
        platform="win32",
        home_path=Path("/ignored"),
    )
    assert_equal(windows_native.strategy, "windows-home", "native Windows strategy")
    assert_equal(
        windows_native.path,
        Path("/windows-home/user/.codex"),
        "native Windows home path",
    )

    wsl_shared = resolve_codex_home(
        env={"WSL_DISTRO_NAME": "Ubuntu", "USERPROFILE": "/mnt/c/Users/Alice"},
        platform="linux",
        home_path=Path("/home/alice"),
        path_exists=lambda path: path == Path("/mnt/c/Users/Alice/.codex"),
    )
    assert_equal(
        wsl_shared.strategy,
        "wsl-shared-windows-home",
        "WSL shared-home strategy",
    )
    assert_equal(
        wsl_shared.path,
        Path("/mnt/c/Users/Alice/.codex"),
        "WSL shared-home path",
    )

    wsl_local = resolve_codex_home(
        env={"WSL_DISTRO_NAME": "Ubuntu", "USERPROFILE": "/mnt/c/Users/Alice"},
        platform="linux",
        home_path=Path("/home/alice"),
        path_exists=lambda path: False,
    )
    assert_equal(wsl_local.strategy, "wsl-linux-home", "WSL fallback strategy")
    assert_equal(wsl_local.path, Path("/home/alice/.codex"), "WSL fallback path")

    linux_default = resolve_codex_home(
        env={},
        platform="linux",
        home_path=Path("/home/alice"),
        path_exists=lambda path: False,
        proc_version_path=Path("/tmp/non-wsl-proc-version"),
    )
    assert_equal(
        linux_default.strategy,
        "platform-default-home",
        "Linux default strategy",
    )
    assert_equal(
        linux_default.path,
        Path("/home/alice/.codex"),
        "Linux default home path",
    )


def main() -> int:
    test_codex_home_resolution()

    with tempfile.TemporaryDirectory(prefix="codex-global-home-") as home_dir, tempfile.TemporaryDirectory(
        prefix="codex-global-target-"
    ) as repo_dir, tempfile.TemporaryDirectory(prefix="codex-global-outside-") as outside_dir:
        codex_home = Path(home_dir) / ".codex"
        target_repo = Path(repo_dir) / "game-repo"
        target_repo.mkdir(parents=True, exist_ok=True)

        run(
            [
                sys.executable,
                str(BOOTSTRAP),
                "--codex-home",
                str(codex_home),
                "--source-repo",
                str(REPO_ROOT),
                "--global-only",
            ]
        )

        run(
            [
                sys.executable,
                str(BOOTSTRAP),
                "--codex-home",
                str(codex_home),
                "--source-repo",
                str(REPO_ROOT),
            ],
            cwd=Path(outside_dir),
        )

        assert_exists(codex_home / "skills" / "studio-help" / "SKILL.md")
        assert_exists(codex_home / "skills" / "install-studio" / "SKILL.md")
        assert_exists(codex_home / "skills" / "adopt-studio" / "SKILL.md")
        assert_exists(codex_home / "agents" / "studio-bootstrapper.toml")
        assert_exists(codex_home / "bin" / "bootstrap.py")
        assert_exists(codex_home / "bin" / "install_repo_studio.py")
        assert_exists(codex_home / "codex-game-studios-install.json")

        run(["git", "init"], cwd=target_repo)

        run(
            [
                sys.executable,
                str(codex_home / "bin" / "bootstrap.py"),
                "--codex-home",
                str(codex_home),
            ]
            ,
            cwd=target_repo,
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
                timeout=20,
            )
            global_text = global_prompt.stdout + global_prompt.stderr
            if "studio-help" not in global_text:
                raise AssertionError("Expected studio-help in global prompt context")

            if has_codex_auth(codex_home):
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
                        timeout=45,
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
            else:
                print("Skipped live global skill probe because the temporary CODEX_HOME has no auth.json.")

            repo_prompt = run(
                [codex_path, "debug", "prompt-input"],
                cwd=target_repo,
                env=env,
                timeout=20,
            )
            repo_text = repo_prompt.stdout + repo_prompt.stderr
            if "start" not in repo_text:
                raise AssertionError("Expected start in installed repo prompt context")

            if has_codex_auth(codex_home):
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
                        timeout=45,
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
            else:
                print("Skipped live repo skill probe because the temporary CODEX_HOME has no auth.json.")

        print("Hybrid global installer validation passed.")
        print(f"Codex home: {codex_home}")
        print(f"Target repo: {target_repo}")
        print(f"Outside repo: {outside_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
