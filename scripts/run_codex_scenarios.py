#!/usr/bin/env python3
"""Run fixture-based Codex E2E scenarios in throwaway repo copies."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES_ROOT = REPO_ROOT / "fixtures" / "e2e"
SCENARIOS_DIR = FIXTURES_ROOT / "scenarios"
STATES_DIR = FIXTURES_ROOT / "states"
DEFAULT_RESULTS_DIR = Path(tempfile.gettempdir()) / "codex-scenario-results"


@dataclass
class TurnResult:
    index: int
    prompt: str
    exit_code: int
    duration_sec: float
    final_message: str
    session_id: str
    json_path: str
    message_path: str
    stderr_lines: list[str]
    issues: list[str]


@dataclass
class ScenarioResult:
    name: str
    fixture: str
    ok: bool
    workdir: str
    turns: list[TurnResult]
    assertion_errors: list[str]
    notes: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scenario",
        nargs="*",
        default=None,
        help="Optional scenario names to run. Defaults to every JSON file in fixtures/e2e/scenarios.",
    )
    parser.add_argument(
        "--results-dir",
        default=None,
        help="Directory for scenario logs and summaries.",
    )
    parser.add_argument(
        "--model",
        default="gpt-5.4-mini",
        help="Model to use for scenario runs.",
    )
    parser.add_argument(
        "--reasoning-effort",
        default="low",
        help="Reasoning effort to pass to Codex.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=240,
        help="Per-turn timeout in seconds.",
    )
    parser.add_argument(
        "--keep-workdirs",
        action="store_true",
        help="Do not delete throwaway working directories after the run.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List scenario names and exit.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_results_dir(requested: str | None) -> Path:
    if requested:
        output_dir = Path(requested)
    else:
        stamp = time.strftime("%Y%m%d-%H%M%S")
        output_dir = DEFAULT_RESULTS_DIR / stamp
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def scenario_paths(selected: list[str] | None) -> list[Path]:
    available = {path.stem: path for path in sorted(SCENARIOS_DIR.glob("*.json"))}
    if selected is None:
        return list(available.values())

    missing = [name for name in selected if name not in available]
    if missing:
        raise SystemExit(f"Unknown scenario(s): {', '.join(missing)}")
    return [available[name] for name in selected]


def ignore_copy(directory: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    current = Path(directory)
    for name in names:
        candidate = current / name
        if name in {".git", "__pycache__"} or name.endswith(".pyc"):
            ignored.add(name)
            continue
        try:
            relative = candidate.relative_to(REPO_ROOT)
        except ValueError:
            relative = None
        if relative == Path(".git/index.lock"):
            ignored.add(name)
    return ignored


def create_throwaway_copy(destination: Path) -> None:
    shutil.copytree(REPO_ROOT, destination, symlinks=False, ignore=ignore_copy)
    initialize_git_repo(destination)


def initialize_git_repo(workdir: Path) -> None:
    git_path = shutil.which("git")
    if not git_path:
        return

    commands = [
        [git_path, "init", "-b", "main"],
        [git_path, "config", "user.name", "Codex Scenario Runner"],
        [git_path, "config", "user.email", "codex-scenarios@example.invalid"],
        [git_path, "add", "-A"],
        [git_path, "commit", "-m", "Scenario fixture snapshot"],
    ]
    for command in commands:
        subprocess.run(
            command,
            cwd=workdir,
            capture_output=True,
            text=True,
            check=True,
        )


def apply_overlay(workdir: Path, fixture_name: str) -> None:
    overlay_dir = STATES_DIR / fixture_name / "overlay"
    if not overlay_dir.exists():
        return

    for source in sorted(overlay_dir.rglob("*")):
        if source.is_dir():
            continue
        relative = source.relative_to(overlay_dir)
        target = workdir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def parse_thread_id(json_path: Path) -> str:
    for raw_line in json_path.read_text(encoding="utf-8").splitlines():
        raw_line = raw_line.strip()
        if not raw_line:
            continue
        try:
            event = json.loads(raw_line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "thread.started" and event.get("thread_id"):
            return str(event["thread_id"])
    return ""


def filter_stderr(stderr_text: str) -> list[str]:
    ignored_markers = (
        "codex_rollout::list",
        "codex_core::shell_snapshot",
        "codex_core::file_watcher",
        "codex_analytics::client",
        "stream disconnected - retrying sampling request",
    )
    lines = [line.strip() for line in stderr_text.splitlines() if line.strip()]
    kept: list[str] = []
    for line in lines:
        if line == "Reading additional input from stdin...":
            continue
        if line.startswith("<") or line.startswith("</"):
            continue
        if "window._cf_" in line:
            continue
        if any(marker in line for marker in ignored_markers):
            continue
        kept.append(line)
    return kept


def run_turn(
    *,
    workdir: Path,
    scenario_dir: Path,
    turn_index: int,
    prompt: str,
    session_id: str | None,
    model: str,
    reasoning_effort: str,
    timeout: int,
) -> TurnResult:
    json_path = scenario_dir / f"turn-{turn_index:02d}.jsonl"
    message_path = scenario_dir / f"turn-{turn_index:02d}.txt"

    if session_id:
        command = [
            "codex",
            "exec",
            "resume",
            "--json",
            "--enable",
            "codex_hooks",
            "--skip-git-repo-check",
            "--full-auto",
            "-m",
            model,
            "-c",
            f'model_reasoning_effort="{reasoning_effort}"',
            "-o",
            str(message_path),
            session_id,
            prompt,
        ]
    else:
        command = [
            "codex",
            "exec",
            "--json",
            "--enable",
            "codex_hooks",
            "--skip-git-repo-check",
            "-s",
            "workspace-write",
            "--color",
            "never",
            "-m",
            model,
            "-c",
            f'model_reasoning_effort="{reasoning_effort}"',
            "-o",
            str(message_path),
            prompt,
        ]

    started = time.monotonic()
    issues: list[str] = []
    stderr_lines: list[str] = []

    try:
        with json_path.open("w", encoding="utf-8") as stdout_handle:
            completed = subprocess.run(
                command,
                cwd=workdir,
                stdout=stdout_handle,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout,
            )
        exit_code = completed.returncode
        stderr_lines = filter_stderr(completed.stderr)
    except subprocess.TimeoutExpired:
        exit_code = 124
        issues.append(f"timed out after {timeout}s")
        stderr_lines = []

    if exit_code != 0:
        issues.append(f"codex exited with code {exit_code}")

    final_message = message_path.read_text(encoding="utf-8").strip() if message_path.exists() else ""
    next_session_id = session_id or parse_thread_id(json_path)
    if not next_session_id:
        issues.append("missing session/thread id in turn output")

    return TurnResult(
        index=turn_index,
        prompt=prompt,
        exit_code=exit_code,
        duration_sec=round(time.monotonic() - started, 2),
        final_message=final_message,
        session_id=next_session_id,
        json_path=str(json_path),
        message_path=str(message_path),
        stderr_lines=stderr_lines,
        issues=issues,
    )


def assert_path_exists(workdir: Path, path: str) -> str | None:
    target = workdir / path
    if not target.exists():
        return f"expected path to exist: {path}"
    return None


def assert_path_not_exists(workdir: Path, path: str) -> str | None:
    target = workdir / path
    if target.exists():
        return f"expected path to be absent: {path}"
    return None


def assert_file_contains(workdir: Path, path: str, *, contains: str | None, regex: str | None) -> str | None:
    target = workdir / path
    if not target.exists():
        return f"expected file for content assertion: {path}"
    text = target.read_text(encoding="utf-8")
    if contains is not None and contains not in text:
        return f"{path}: missing expected text: {contains}"
    if regex is not None and re.search(regex, text, re.MULTILINE) is None:
        return f"{path}: missing expected regex: {regex}"
    return None


def assert_glob_count(workdir: Path, pattern: str, *, minimum: int | None, exact: int | None) -> str | None:
    count = len(list(workdir.glob(pattern)))
    if minimum is not None and count < minimum:
        return f"{pattern}: expected at least {minimum} matches, found {count}"
    if exact is not None and count != exact:
        return f"{pattern}: expected exactly {exact} matches, found {count}"
    return None


def run_assertions(workdir: Path, assertions: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for assertion in assertions:
        assertion_type = assertion["type"]
        if assertion_type == "path_exists":
            error = assert_path_exists(workdir, assertion["path"])
        elif assertion_type == "path_not_exists":
            error = assert_path_not_exists(workdir, assertion["path"])
        elif assertion_type == "file_contains":
            error = assert_file_contains(
                workdir,
                assertion["path"],
                contains=assertion.get("contains"),
                regex=assertion.get("regex"),
            )
        elif assertion_type == "glob_count":
            error = assert_glob_count(
                workdir,
                assertion["pattern"],
                minimum=assertion.get("min"),
                exact=assertion.get("exact"),
            )
        else:
            error = f"unsupported assertion type: {assertion_type}"
        if error:
            errors.append(error)
    return errors


def run_scenario(
    scenario_path: Path,
    *,
    results_dir: Path,
    model: str,
    reasoning_effort: str,
    timeout: int,
    keep_workdirs: bool,
) -> ScenarioResult:
    spec = load_json(scenario_path)
    scenario_name = spec["name"]
    fixture_name = spec["fixture"]
    scenario_dir = results_dir / scenario_name
    scenario_dir.mkdir(parents=True, exist_ok=True)

    temp_root = Path(tempfile.mkdtemp(prefix=f"codex-scenario-{scenario_name}-"))
    workdir = temp_root / "repo"
    notes: list[str] = []

    try:
        create_throwaway_copy(workdir)
        apply_overlay(workdir, fixture_name)
        notes.append(f"fixture={fixture_name}")

        turns: list[TurnResult] = []
        session_id: str | None = None
        for index, turn_spec in enumerate(spec["turns"], start=1):
            if index > 1:
                expected = spec["turns"][index - 2].get("expect_regex")
                if expected and re.search(expected, turns[-1].final_message, re.MULTILINE | re.DOTALL) is None:
                    turns[-1].issues.append(f"expected previous turn to match regex: {expected}")
                    break

            turn = run_turn(
                workdir=workdir,
                scenario_dir=scenario_dir,
                turn_index=index,
                prompt=turn_spec["prompt"],
                session_id=session_id,
                model=model,
                reasoning_effort=reasoning_effort,
                timeout=timeout,
            )
            turns.append(turn)
            session_id = turn.session_id

            if turn_spec.get("expect_regex") and re.search(
                turn_spec["expect_regex"], turn.final_message, re.MULTILINE | re.DOTALL
            ) is None:
                turn.issues.append(f"final message did not match regex: {turn_spec['expect_regex']}")
                break

            if turn.issues:
                break

        assertion_errors: list[str] = []
        if not any(turn.issues for turn in turns):
            assertion_errors = run_assertions(workdir, spec.get("assertions", []))

        result = ScenarioResult(
            name=scenario_name,
            fixture=fixture_name,
            ok=not any(turn.issues for turn in turns) and not assertion_errors,
            workdir=str(workdir),
            turns=turns,
            assertion_errors=assertion_errors,
            notes=notes,
        )
        (scenario_dir / "result.json").write_text(
            json.dumps(asdict(result), indent=2),
            encoding="utf-8",
        )
        return result
    finally:
        if not keep_workdirs and temp_root.exists():
            shutil.rmtree(temp_root)


def main() -> int:
    args = parse_args()
    paths = scenario_paths(args.scenario)
    if args.list:
        for path in paths:
            print(path.stem)
        return 0

    results_dir = build_results_dir(args.results_dir)
    results: list[ScenarioResult] = []

    for path in paths:
        result = run_scenario(
            path,
            results_dir=results_dir,
            model=args.model,
            reasoning_effort=args.reasoning_effort,
            timeout=args.timeout,
            keep_workdirs=args.keep_workdirs,
        )
        results.append(result)
        status = "PASS" if result.ok else "FAIL"
        print(f"{result.name}: {status}")
        if not result.ok:
            for turn in result.turns:
                for issue in turn.issues:
                    print(f"  turn {turn.index}: {issue}")
            for error in result.assertion_errors:
                print(f"  assert: {error}")

    summary = {
        "repo_root": str(REPO_ROOT),
        "results_dir": str(results_dir),
        "total": len(results),
        "passed": sum(1 for result in results if result.ok),
        "failed": sum(1 for result in results if not result.ok),
        "results": [asdict(result) for result in results],
    }
    summary_path = results_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print()
    print(f"Summary written to {summary_path}")
    print(f"Passed: {summary['passed']} / {summary['total']} | Failed: {summary['failed']} / {summary['total']}")
    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
