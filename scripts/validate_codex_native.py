#!/usr/bin/env python3
"""Validate Codex-native repo contracts for skills, agents, and project config."""

from __future__ import annotations

import json
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib

try:
    import yaml
except Exception:  # pragma: no cover - optional dependency
    yaml = None


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"
AGENTS_DIR = REPO_ROOT / ".codex" / "agents"
CONFIG_PATH = REPO_ROOT / ".codex" / "config.toml"
HOOKS_CONFIG_PATH = REPO_ROOT / ".codex" / "hooks.json"
HOOKS_DIR = REPO_ROOT / ".codex" / "hooks"
SUPPORTED_HOOK_EVENTS = {
    "SessionStart",
    "PreToolUse",
    "PostToolUse",
    "UserPromptSubmit",
    "Stop",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}

    if yaml is not None:
        data = yaml.safe_load(match.group(1))
        if isinstance(data, dict):
            return {
                str(key): "" if value is None else str(value)
                for key, value in data.items()
            }
        return {}

    fields: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def validate_skills(errors: list[str]) -> None:
    skill_count = 0
    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        skill_count += 1
        fields = parse_frontmatter(skill_md)
        name = fields.get("name")
        description = fields.get("description")
        if not name or not description:
            fail(errors, f"{skill_md}: missing frontmatter name/description")
            continue

        openai_yaml = skill_md.parent / "agents" / "openai.yaml"
        if not openai_yaml.exists():
            fail(errors, f"{openai_yaml}: missing")
            continue

        yaml_text = openai_yaml.read_text(encoding="utf-8")
        required_patterns = {
            "display_name": r"(?m)^\s*display_name:\s+",
            "short_description": r"(?m)^\s*short_description:\s+",
            "default_prompt": r"(?m)^\s*default_prompt:\s+",
            "allow_implicit_invocation": r"(?m)^\s*allow_implicit_invocation:\s+(true|false)\s*$",
        }
        for field_name, pattern in required_patterns.items():
            if not re.search(pattern, yaml_text):
                fail(errors, f"{openai_yaml}: missing {field_name}")

        if f"${name}" not in yaml_text:
            fail(errors, f"{openai_yaml}: default_prompt should mention ${name}")

    if skill_count == 0:
        fail(errors, f"{SKILLS_DIR}: no skills found")


def validate_agents(errors: list[str]) -> None:
    agent_count = 0
    for agent_toml in sorted(AGENTS_DIR.glob("*.toml")):
        agent_count += 1
        try:
            data = tomllib.loads(agent_toml.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            fail(errors, f"{agent_toml}: TOML parse error: {exc}")
            continue

        for key in ("name", "description", "developer_instructions", "sandbox_mode"):
            if not data.get(key):
                fail(errors, f"{agent_toml}: missing {key}")

        nicknames = data.get("nickname_candidates")
        if not isinstance(nicknames, list) or len(nicknames) < 3:
            fail(
                errors,
                f"{agent_toml}: nickname_candidates must contain at least 3 names",
            )

    if agent_count == 0:
        fail(errors, f"{AGENTS_DIR}: no agent TOMLs found")


def validate_project_config(errors: list[str]) -> None:
    try:
        config = tomllib.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        fail(errors, f"{CONFIG_PATH}: TOML parse error: {exc}")
        return

    agents_cfg = config.get("agents", {})
    if agents_cfg.get("max_threads") != 6:
        fail(errors, f"{CONFIG_PATH}: expected [agents].max_threads = 6")
    if agents_cfg.get("max_depth") != 1:
        fail(errors, f"{CONFIG_PATH}: expected [agents].max_depth = 1")

    features_cfg = config.get("features", {})
    if HOOKS_CONFIG_PATH.exists() and features_cfg.get("codex_hooks") is not True:
        fail(errors, f"{CONFIG_PATH}: expected [features].codex_hooks = true")


def validate_hooks(errors: list[str]) -> None:
    if not HOOKS_CONFIG_PATH.exists():
        return

    try:
        hooks_config = json.loads(HOOKS_CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(errors, f"{HOOKS_CONFIG_PATH}: JSON parse error: {exc}")
        return

    hook_events = hooks_config.get("hooks")
    if not isinstance(hook_events, dict):
        fail(errors, f"{HOOKS_CONFIG_PATH}: expected top-level 'hooks' object")
        return

    for event_name, matcher_groups in hook_events.items():
        if event_name not in SUPPORTED_HOOK_EVENTS:
            fail(errors, f"{HOOKS_CONFIG_PATH}: unsupported hook event '{event_name}'")
            continue

        if not isinstance(matcher_groups, list) or not matcher_groups:
            fail(errors, f"{HOOKS_CONFIG_PATH}: event '{event_name}' must have a non-empty matcher group list")
            continue

        for group_index, matcher_group in enumerate(matcher_groups, start=1):
            if not isinstance(matcher_group, dict):
                fail(
                    errors,
                    f"{HOOKS_CONFIG_PATH}: {event_name} group {group_index} must be an object",
                )
                continue

            matcher = matcher_group.get("matcher")
            if matcher is not None and not isinstance(matcher, str):
                fail(
                    errors,
                    f"{HOOKS_CONFIG_PATH}: {event_name} group {group_index} matcher must be a string",
                )
                matcher = None

            if matcher:
                try:
                    compiled = re.compile(matcher)
                except re.error as exc:
                    fail(
                        errors,
                        f"{HOOKS_CONFIG_PATH}: {event_name} group {group_index} has invalid regex '{matcher}': {exc}",
                    )
                    compiled = None

                if compiled and event_name in {"PreToolUse", "PostToolUse"} and compiled.search("Bash") is None:
                    fail(
                        errors,
                        f"{HOOKS_CONFIG_PATH}: {event_name} group {group_index} matcher '{matcher}' is a runtime no-op because current Codex only emits Bash for this event",
                    )

                if compiled and event_name == "SessionStart":
                    matches_source = compiled.search("startup") is not None or compiled.search("resume") is not None
                    if not matches_source:
                        fail(
                            errors,
                            f"{HOOKS_CONFIG_PATH}: SessionStart group {group_index} matcher '{matcher}' does not match startup or resume",
                        )

            if event_name in {"Stop", "UserPromptSubmit"} and matcher not in (None, "", "*"):
                fail(
                    errors,
                    f"{HOOKS_CONFIG_PATH}: {event_name} group {group_index} matcher is ignored by current Codex and should be omitted",
                )

            handlers = matcher_group.get("hooks")
            if not isinstance(handlers, list) or not handlers:
                fail(
                    errors,
                    f"{HOOKS_CONFIG_PATH}: {event_name} group {group_index} must contain at least one hook handler",
                )
                continue

            for handler_index, handler in enumerate(handlers, start=1):
                if not isinstance(handler, dict):
                    fail(
                        errors,
                        f"{HOOKS_CONFIG_PATH}: {event_name} group {group_index} handler {handler_index} must be an object",
                    )
                    continue

                handler_type = handler.get("type")
                if handler_type != "command":
                    fail(
                        errors,
                        f"{HOOKS_CONFIG_PATH}: {event_name} group {group_index} handler {handler_index} uses unsupported hook type '{handler_type}'",
                    )
                    continue

                if "timeout_sec" in handler:
                    fail(
                        errors,
                        f"{HOOKS_CONFIG_PATH}: {event_name} group {group_index} handler {handler_index} uses unsupported key 'timeout_sec'; use 'timeout' or 'timeoutSec'",
                    )

                command = handler.get("command")
                if not isinstance(command, str) or not command.strip():
                    fail(
                        errors,
                        f"{HOOKS_CONFIG_PATH}: {event_name} group {group_index} handler {handler_index} missing command",
                    )
                    continue

                if ".codex/hooks/" in command and "git rev-parse --show-toplevel" not in command:
                    fail(
                        errors,
                        f"{HOOKS_CONFIG_PATH}: {event_name} group {group_index} handler {handler_index} should resolve repo-local hooks from the git root",
                    )

                match = re.search(r"\.codex/hooks/([A-Za-z0-9._-]+\.sh)", command)
                if match:
                    hook_script = HOOKS_DIR / match.group(1)
                    if not hook_script.exists():
                        fail(
                            errors,
                            f"{HOOKS_CONFIG_PATH}: {event_name} group {group_index} handler {handler_index} references missing script {hook_script}",
                        )

    bash_path = shutil.which("bash")
    if bash_path:
        for hook_script in sorted(HOOKS_DIR.glob("*.sh")):
            result = subprocess.run(
                [bash_path, "-n", str(hook_script)],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                fail(
                    errors,
                    f"{hook_script}: bash -n failed: {(result.stderr or result.stdout).strip()}",
                )


def main() -> int:
    errors: list[str] = []
    validate_skills(errors)
    validate_agents(errors)
    validate_project_config(errors)
    validate_hooks(errors)

    if errors:
        print("Codex-native validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Codex-native validation passed.")
    print(f"Skills checked: {len(list(SKILLS_DIR.glob('*/SKILL.md')))}")
    print(f"Agents checked: {len(list(AGENTS_DIR.glob('*.toml')))}")
    print(f"Hooks checked: {len(list(HOOKS_DIR.glob('*.sh')))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
