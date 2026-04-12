#!/usr/bin/env python3
"""Run live Codex smoke tests across repo skills and custom agents."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"
AGENTS_DIR = REPO_ROOT / ".codex" / "agents"
DEFAULT_RESULTS_DIR = Path(tempfile.gettempdir()) / "codex-e2e-results"

SKILL_OK = "SKILL_OK"
AGENT_OK = "AGENT_OK"
KNOWN_RUNTIME_WARNINGS = (
    "codex_rollout::list",
    "codex_core::shell_snapshot",
    "codex_core::file_watcher",
    "stream disconnected - retrying sampling request",
    "codex_analytics::client",
)


@dataclass
class ProbeResult:
    kind: str
    name: str
    ok: bool
    final_message: str
    duration_sec: float
    issues: list[str]
    failed_commands: list[str]
    stderr_lines: list[str]
    json_path: str
    message_path: str


def parse_frontmatter_name(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8")
    match = re.search(r"^name:\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip().strip("\"'") if match else skill_md.parent.name


def list_skills() -> list[str]:
    return [parse_frontmatter_name(skill_md) for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md"))]


def list_agents() -> list[str]:
    agent_names: list[str] = []
    for agent_toml in sorted(AGENTS_DIR.glob("*.toml")):
        text = agent_toml.read_text(encoding="utf-8")
        match = re.search(r'^name\s*=\s*"([^"]+)"', text, re.MULTILINE)
        agent_names.append(match.group(1) if match else agent_toml.stem)
    return agent_names


def skill_prompt(name: str) -> str:
    return (
        f"Use the `${name}` skill for this repository. "
        "Follow the skill faithfully until the first point where it would require "
        "user input or any file creation/modification. A normal first question to "
        "the user, clarification request, or approval gate counts as success, not "
        "failure. Read only the minimum files needed. Do not modify anything. If "
        "you hit a missing path, stale tool instruction, or contradictory repo "
        "guidance, return exactly "
        '`SKILL_FAIL: <brief reason>`. Otherwise return exactly `SKILL_OK`.'
    )


def agent_prompt(name: str) -> str:
    return (
        f"Use the `{name}` subagent exactly once for this repository. "
        'Pass it this exact task: "Reply with exactly READY and nothing else. '
        'Do not write files." If the subagent completes successfully, return '
        "exactly `AGENT_OK`. If subagent invocation or completion fails, return "
        'exactly `AGENT_FAIL: <brief reason>`. Do not write files.'
    )


def run_codex_exec(
    *,
    prompt: str,
    json_path: Path,
    message_path: Path,
    model: str | None,
    reasoning_effort: str | None,
    timeout: int,
) -> tuple[int, str]:
    command = [
        "codex",
        "exec",
        "-C",
        str(REPO_ROOT),
        "--enable",
        "codex_hooks",
        "--skip-git-repo-check",
        "--ephemeral",
        "--color",
        "never",
        "--json",
        "-s",
        "read-only",
        "-o",
        str(message_path),
    ]
    if model:
        command.extend(["-m", model])
    if reasoning_effort:
        command.extend(["-c", f'model_reasoning_effort="{reasoning_effort}"'])
    command.append(prompt)

    with json_path.open("w", encoding="utf-8") as stdout_handle:
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            stdout=stdout_handle,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )
    return completed.returncode, completed.stderr


def is_expected_skill_boundary(final_message: str) -> bool:
    lower = final_message.lower()
    boundary_signals = (
        "asks the user",
        "ask the user",
        "user input",
        "approval",
        "clarification",
        "wait for the user",
        "what would you like",
        "which would you like",
        "which feature",
        "which sprint",
        "[a]",
    )
    hard_failure_signals = (
        "missing",
        "stale",
        "contradict",
        "unsupported",
        "broken",
        "not found",
        "invalid",
        "pseudo-tool",
    )
    if any(signal in lower for signal in boundary_signals) and not any(
        signal in lower for signal in hard_failure_signals
    ):
        return True

    project_prereq_signals = ("run `$", "requires `$", "try `$", "use `$")
    project_path_signals = (
        "design/",
        "production/",
        "docs/",
        "prototypes/",
        "src/",
        "assets/",
    )
    runtime_path_signals = (
        ".agents/",
        ".codex/",
        ".claude/",
        "docs/studio/skills/",
    )
    return (
        any(signal in lower for signal in project_prereq_signals)
        and any(signal in lower for signal in project_path_signals)
        and not any(signal in lower for signal in runtime_path_signals)
        and not any(signal in lower for signal in hard_failure_signals if signal != "not found")
    )


def is_expected_project_artifact_gap(final_message: str) -> bool:
    lower = final_message.lower()
    project_path_signals = (
        "design/",
        "production/",
        "docs/",
        "prototypes/",
        "src/",
        "assets/",
    )
    runtime_path_signals = (
        ".agents/",
        ".codex/",
        ".claude/",
        "docs/studio/skills/",
    )
    hard_failure_signals = (
        "stale",
        "contradict",
        "unsupported",
        "broken",
        "invalid",
        "pseudo-tool",
    )
    project_artifact_signals = (
        "game concept",
        "systems index",
        "gdd",
        "backlog",
        "story",
        "adr",
        "architecture registry",
        "control manifest",
        "asset spec",
        "art bible",
        "test setup",
        "engine reference",
        "technical preferences",
    )
    return (
        any(
            signal in lower
            for signal in (
                "missing",
                "not found",
                "no ",
                "does not exist",
                "do not exist",
                "not configured",
            )
        )
        and (
            any(signal in lower for signal in project_path_signals)
            or any(signal in lower for signal in project_artifact_signals)
            or "$setup-engine" in lower
        )
        and not any(signal in lower for signal in runtime_path_signals)
        and not any(signal in lower for signal in hard_failure_signals)
    )


def parse_events(json_path: Path) -> tuple[list[str], list[str], bool]:
    failed_commands: list[str] = []
    issues: list[str] = []
    saw_spawn_agent = False

    for raw_line in json_path.read_text(encoding="utf-8").splitlines():
        raw_line = raw_line.strip()
        if not raw_line:
            continue
        try:
            event = json.loads(raw_line)
        except json.JSONDecodeError:
            issues.append(f"non-JSON event line: {raw_line[:120]}")
            continue

        item = event.get("item")
        if isinstance(item, dict):
            item_type = item.get("type")
            if item_type == "command_execution":
                exit_code = item.get("exit_code")
                status = item.get("status")
                command = str(item.get("command", "<unknown command>"))
                benign_probe_miss = (
                    exit_code in {1, 2, 123}
                    and any(
                        probe in command
                        for probe in (
                            "rg --files",
                            "rg ",
                            " rg ",
                            "grep ",
                            " grep ",
                            "[ -f ",
                            "[ -e ",
                            "test -f ",
                            "test -e ",
                            "find ",
                            "xargs ",
                            " ls ",
                        )
                    )
                )
                if not benign_probe_miss and (
                    status == "failed" or (isinstance(exit_code, int) and exit_code != 0)
                ):
                    failed_commands.append(f"{command} (exit={exit_code})")
            elif item_type == "collab_tool_call":
                if item.get("tool") == "spawn_agent":
                    saw_spawn_agent = True
                if item.get("status") == "failed":
                    issues.append(f"collab tool failed: {item.get('tool')}")

    return failed_commands, issues, saw_spawn_agent


def is_benign_project_gap_command(command_record: str) -> bool:
    command = command_record.lower()
    project_path_signals = (
        "design/",
        "production/",
        "docs/",
        "prototypes/",
        "src/",
        "assets/",
    )
    probe_signals = (
        "sed -n ",
        "cat ",
        "rg --files",
        "find ",
        "[ -f ",
        "[ -e ",
        "test -f ",
        "test -e ",
        "ls ",
    )
    return any(path in command for path in project_path_signals) and any(
        probe in command for probe in probe_signals
    )


def filter_stderr(stderr_text: str) -> list[str]:
    lines = [line.strip() for line in stderr_text.splitlines() if line.strip()]
    filtered: list[str] = []
    for line in lines:
        if line == "Reading additional input from stdin...":
            continue
        if line.startswith("<") or line.startswith("</"):
            continue
        if "window._cf_" in line:
            continue
        if any(marker in line for marker in KNOWN_RUNTIME_WARNINGS):
            continue
        filtered.append(line)
    return filtered


def run_probe(
    *,
    kind: str,
    name: str,
    model: str | None,
    reasoning_effort: str | None,
    timeout: int,
    results_dir: Path,
) -> ProbeResult:
    slug = name.replace("/", "-")
    json_path = results_dir / f"{kind}-{slug}.jsonl"
    message_path = results_dir / f"{kind}-{slug}.txt"
    prompt = skill_prompt(name) if kind == "skill" else agent_prompt(name)

    started_at = time.monotonic()
    issues: list[str] = []
    failed_commands: list[str] = []
    stderr_lines: list[str] = []
    final_message = ""
    saw_spawn_agent = False

    try:
        exit_code, stderr_text = run_codex_exec(
            prompt=prompt,
            json_path=json_path,
            message_path=message_path,
            model=model,
            reasoning_effort=reasoning_effort,
            timeout=timeout,
        )
        stderr_lines = filter_stderr(stderr_text)
        if exit_code != 0:
            issues.append(f"codex exec exited with code {exit_code}")
        if message_path.exists():
            final_message = message_path.read_text(encoding="utf-8").strip()
        if json_path.exists():
            failed_commands, parse_issues, saw_spawn_agent = parse_events(json_path)
            issues.extend(parse_issues)
        else:
            issues.append("missing JSON event log")
    except subprocess.TimeoutExpired:
        issues.append(f"timed out after {timeout}s")

    if kind == "skill":
        expected_boundary = is_expected_skill_boundary(final_message)
        expected_gap = is_expected_project_artifact_gap(final_message)
        blocking_failed_commands = failed_commands
        if (expected_gap or final_message == SKILL_OK) and failed_commands and all(
            is_benign_project_gap_command(command) for command in failed_commands
        ):
            blocking_failed_commands = []
        ok = (
            (
                final_message == SKILL_OK
                or expected_boundary
                or expected_gap
            )
            and not blocking_failed_commands
            and not issues
        )
        failed_commands = blocking_failed_commands
    else:
        if not saw_spawn_agent:
            issues.append("did not spawn a subagent")
        ok = final_message == AGENT_OK and saw_spawn_agent and not failed_commands and not issues

    return ProbeResult(
        kind=kind,
        name=name,
        ok=ok,
        final_message=final_message,
        duration_sec=round(time.monotonic() - started_at, 2),
        issues=issues,
        failed_commands=failed_commands,
        stderr_lines=stderr_lines,
        json_path=str(json_path),
        message_path=str(message_path),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("skills", "agents", "all"),
        default="all",
        help="Which live probe set to run.",
    )
    parser.add_argument(
        "--names",
        nargs="*",
        default=None,
        help="Optional explicit skill/agent names to run instead of the discovered full set.",
    )
    parser.add_argument("--model", default=None, help="Optional model override for skill probes.")
    parser.add_argument(
        "--reasoning-effort",
        default="low",
        help="Optional reasoning-effort override for the top-level Codex exec run.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=180,
        help="Per-probe timeout in seconds.",
    )
    parser.add_argument(
        "--results-dir",
        default=None,
        help="Directory for JSONL/message artifacts. Defaults to a timestamped temp directory.",
    )
    return parser.parse_args()


def build_results_dir(requested: str | None) -> Path:
    if requested:
        output_dir = Path(requested)
    else:
        stamp = time.strftime("%Y%m%d-%H%M%S")
        output_dir = DEFAULT_RESULTS_DIR / stamp
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def main() -> int:
    args = parse_args()
    results_dir = build_results_dir(args.results_dir)

    if args.mode == "skills":
        queue = [("skill", name) for name in (args.names or list_skills())]
    elif args.mode == "agents":
        queue = [("agent", name) for name in (args.names or list_agents())]
    else:
        skill_names = args.names or list_skills()
        queue = [("skill", name) for name in skill_names]
        if args.names is None:
            queue.extend(("agent", name) for name in list_agents())

    results: list[ProbeResult] = []
    total = len(queue)
    for index, (kind, name) in enumerate(queue, start=1):
        result = run_probe(
            kind=kind,
            name=name,
            model=args.model if kind == "skill" else None,
            reasoning_effort=args.reasoning_effort,
            timeout=args.timeout,
            results_dir=results_dir,
        )
        results.append(result)
        status = "PASS" if result.ok else "FAIL"
        print(
            f"[{index:03d}/{total:03d}] {kind}:{name} -> {status} "
            f"({result.duration_sec:.2f}s)"
        )
        if not result.ok:
            if result.final_message:
                print(f"  final: {result.final_message}")
            for issue in result.issues[:3]:
                print(f"  issue: {issue}")
            for command in result.failed_commands[:2]:
                print(f"  command: {command}")

    summary = {
        "repo_root": str(REPO_ROOT),
        "results_dir": str(results_dir),
        "mode": args.mode,
        "total": len(results),
        "passed": sum(1 for result in results if result.ok),
        "failed": sum(1 for result in results if not result.ok),
        "results": [asdict(result) for result in results],
    }
    summary_path = results_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print()
    print(f"Summary written to {summary_path}")
    print(
        f"Passed: {summary['passed']} / {summary['total']} | "
        f"Failed: {summary['failed']} / {summary['total']}"
    )

    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
