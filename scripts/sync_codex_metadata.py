#!/usr/bin/env python3
"""Synchronize Codex-native skill and agent metadata for this repo.

This script intentionally keeps the generated files small and deterministic so
future changes stay easy to review.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path

try:
    import yaml
except Exception:  # pragma: no cover - optional dependency
    yaml = None


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"
AGENTS_DIR = REPO_ROOT / ".codex" / "agents"
CATALOG_PATH = REPO_ROOT / "Codex Skill Testing Framework" / "catalog.yaml"


TITLE_TOKEN_MAP = {
    "qa": "QA",
    "ux": "UX",
    "ui": "UI",
    "gdd": "GDD",
    "gdds": "GDDs",
    "adr": "ADR",
    "ci": "CI",
    "cd": "CD",
    "mvp": "MVP",
    "vfx": "VFX",
    "ops": "Ops",
}

IMPLICIT_TRUE_CATEGORIES = {"analysis", "review", "readiness"}
IMPLICIT_TRUE_SKILLS = {
    "brainstorm",
    "bug-report",
    "bug-triage",
    "gate-check",
    "help",
    "playtest-report",
    "project-stage-detect",
    "setup-engine",
    "start",
}


@dataclass
class SkillFrontmatter:
    name: str
    description: str


def load_skill_categories() -> dict[str, str]:
    categories: dict[str, str] = {}
    current_name: str | None = None
    for raw_line in CATALOG_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("- name:"):
            current_name = line.split(":", 1)[1].strip()
            continue
        if current_name and line.startswith("category:"):
            categories[current_name] = line.split(":", 1)[1].strip()
            current_name = None
    return categories


def parse_frontmatter(skill_md: Path) -> SkillFrontmatter:
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError(f"Missing YAML frontmatter in {skill_md}")

    if yaml is not None:
        data = yaml.safe_load(match.group(1))
        if not isinstance(data, dict):
            raise ValueError(f"Invalid YAML frontmatter in {skill_md}")
        fields = {
            str(key): "" if value is None else str(value)
            for key, value in data.items()
        }
    else:
        fields = {}
        for raw_line in match.group(1).splitlines():
            if ":" not in raw_line:
                continue
            key, value = raw_line.split(":", 1)
            fields[key.strip()] = value.strip()

    name = fields.get("name", "")
    description = fields.get("description", "")
    if not name or not description:
        raise ValueError(f"Missing name/description in {skill_md}")
    return SkillFrontmatter(name=name, description=description)


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def titleize(slug: str) -> str:
    parts = []
    for token in slug.replace("_", "-").split("-"):
        if not token:
            continue
        lowered = token.lower()
        if lowered in TITLE_TOKEN_MAP:
            parts.append(TITLE_TOKEN_MAP[lowered])
        else:
            parts.append(token.capitalize())
    return " ".join(parts)


def shorten_description(description: str, limit: int = 72) -> str:
    text = re.sub(r"\s+", " ", description).strip()
    if len(text) <= limit:
        return text
    shortened = text[: limit - 1].rsplit(" ", 1)[0].rstrip(",;:")
    return f"{shortened}…"


def to_prompt_fragment(description: str) -> str:
    text = re.sub(r"\s+", " ", description).strip().rstrip(".")
    if not text:
        return "run this workflow"
    return text[0].lower() + text[1:]


def allow_implicit_invocation(skill_name: str, category: str | None) -> bool:
    return skill_name in IMPLICIT_TRUE_SKILLS or category in IMPLICIT_TRUE_CATEGORIES


def write_skill_openai_yaml(
    skill_dir: Path,
    frontmatter: SkillFrontmatter,
    category: str | None,
) -> None:
    skill_name = frontmatter.name
    yaml_text = "\n".join(
        [
            "interface:",
            f"  display_name: {yaml_quote(titleize(skill_name))}",
            f"  short_description: {yaml_quote(shorten_description(frontmatter.description))}",
            f"  default_prompt: {yaml_quote(f'Use ${skill_name} to {to_prompt_fragment(frontmatter.description)}.')}",
            "policy:",
            f"  allow_implicit_invocation: {'true' if allow_implicit_invocation(skill_name, category) else 'false'}",
            "",
        ]
    )
    output_path = skill_dir / "agents" / "openai.yaml"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(yaml_text, encoding="utf-8")


def ensure_agent_runtime_metadata(agent_toml: Path) -> None:
    text = agent_toml.read_text(encoding="utf-8")

    if "nickname_candidates =" not in text:
        name_match = re.search(r'^name = "([^"]+)"$', text, re.MULTILINE)
        if not name_match:
            raise ValueError(f"Missing name field in {agent_toml}")
        title = titleize(name_match.group(1))
        nickname_line = (
            f'nickname_candidates = ["{title} A", "{title} B", "{title} C"]\n'
        )
        text = re.sub(
            r'^(description = ".*")\n',
            r"\1\n" + nickname_line,
            text,
            count=1,
            flags=re.MULTILINE,
        )

    if "sandbox_mode =" not in text:
        text = re.sub(
            r'^(model_reasoning_effort = ".*")\n',
            r'\1\nsandbox_mode = "workspace-write"\n',
            text,
            count=1,
            flags=re.MULTILINE,
        )

    agent_toml.write_text(text, encoding="utf-8")


def main() -> None:
    skill_categories = load_skill_categories()

    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        frontmatter = parse_frontmatter(skill_md)
        category = skill_categories.get(frontmatter.name)
        write_skill_openai_yaml(skill_md.parent, frontmatter, category)

    for agent_toml in sorted(AGENTS_DIR.glob("*.toml")):
        ensure_agent_runtime_metadata(agent_toml)

    print("Synced skill openai.yaml files and agent runtime metadata.")


if __name__ == "__main__":
    main()
