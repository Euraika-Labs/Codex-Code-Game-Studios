#!/usr/bin/env python3
"""Validate Codex-native repo contracts for skills, agents, and project config."""

from __future__ import annotations

import re
from pathlib import Path
import sys
import tomllib


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"
AGENTS_DIR = REPO_ROOT / ".codex" / "agents"
CONFIG_PATH = REPO_ROOT / ".codex" / "config.toml"


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
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


def main() -> int:
    errors: list[str] = []
    validate_skills(errors)
    validate_agents(errors)
    validate_project_config(errors)

    if errors:
        print("Codex-native validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Codex-native validation passed.")
    print(f"Skills checked: {len(list(SKILLS_DIR.glob('*/SKILL.md')))}")
    print(f"Agents checked: {len(list(AGENTS_DIR.glob('*.toml')))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
