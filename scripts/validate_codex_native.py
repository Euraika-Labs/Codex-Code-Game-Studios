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

from build_workflow_matrix import WORKFLOW_CATALOG_PATH, build_matrix, load_yaml

try:
    import yaml
except Exception:  # pragma: no cover - optional dependency
    yaml = None


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"
AGENTS_DIR = REPO_ROOT / ".codex" / "agents"
GLOBAL_PACK_DIR = REPO_ROOT / "global-pack"
GLOBAL_SKILLS_DIR = GLOBAL_PACK_DIR / "skills"
GLOBAL_AGENTS_DIR = GLOBAL_PACK_DIR / "agents"
GLOBAL_BIN_DIR = GLOBAL_PACK_DIR / "bin"
GLOBAL_MANIFEST_PATH = GLOBAL_PACK_DIR / "manifest.json"
ROOT_BOOTSTRAP_SH = REPO_ROOT / "bootstrap.sh"
ROOT_BOOTSTRAP_PS1 = REPO_ROOT / "bootstrap.ps1"
CONFIG_PATH = REPO_ROOT / ".codex" / "config.toml"
HOOKS_CONFIG_PATH = REPO_ROOT / ".codex" / "hooks.json"
HOOKS_DIR = REPO_ROOT / ".codex" / "hooks"
SCENARIOS_DIR = REPO_ROOT / "fixtures" / "e2e" / "scenarios"
STATES_DIR = REPO_ROOT / "fixtures" / "e2e" / "states"
FRAMEWORK_AGENTS_PATH = REPO_ROOT / "Codex Skill Testing Framework" / "AGENTS.md"
DOC_SURFACES = (
    REPO_ROOT / "README.md",
    REPO_ROOT / "UPGRADING.md",
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "docs",
    REPO_ROOT / "Codex Skill Testing Framework",
)
SUPPORTED_HOOK_EVENTS = {
    "SessionStart",
    "PreToolUse",
    "PostToolUse",
    "UserPromptSubmit",
    "Stop",
}
STALE_RUNTIME_PATTERNS = {
    "docs/studio/skills/": "repo skills now live under .agents/skills/",
    ".claude/skills/": "Claude skill paths are not valid in this Codex-native repo",
    ".claude/agents/": "Claude agent paths are not valid in this Codex-native repo",
    "`ask the user directly in plain text`": "pseudo-tool references should be plain-text instructions instead",
    "Write/Edit tools": "refer to file edits or apply_patch, not obsolete Write/Edit tool names",
}
STALE_DOC_PATTERNS = {
    "Claude Code": "docs should describe this repo as a standalone Codex product",
    "CLAUDE.md": "shared guidance should refer to AGENTS.md",
    ".claude/": "docs should not point to deprecated Claude paths",
    "AskUserQuestion": "docs should not mention obsolete prompt helpers",
    "settings.local.json": "docs should point to Codex-native override surfaces",
    "@anthropic-ai/claude-code": "install instructions should reference @openai/codex",
    "built for Claude": "docs should not frame the repo as a derivative product",
    "port of the original": "docs should not frame the repo as a port",
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


def validate_global_pack(errors: list[str]) -> None:
    if not GLOBAL_MANIFEST_PATH.exists():
        fail(errors, f"{GLOBAL_MANIFEST_PATH}: missing")
        return

    try:
        manifest = json.loads(GLOBAL_MANIFEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(errors, f"{GLOBAL_MANIFEST_PATH}: JSON parse error: {exc}")
        return

    required_manifest_keys = {
        "global_skills",
        "global_agents",
        "bin_files",
        "repo_files",
        "repo_dirs",
        "repo_nested_guides",
        "starter_dirs",
    }
    for key in required_manifest_keys:
        if key not in manifest:
            fail(errors, f"{GLOBAL_MANIFEST_PATH}: missing key '{key}'")

    global_skill_names = manifest.get("global_skills", [])
    if not isinstance(global_skill_names, list) or not global_skill_names:
        fail(errors, f"{GLOBAL_MANIFEST_PATH}: global_skills must be a non-empty list")
        global_skill_names = []

    for skill_name in global_skill_names:
        skill_dir = GLOBAL_SKILLS_DIR / skill_name
        skill_md = skill_dir / "SKILL.md"
        openai_yaml = skill_dir / "agents" / "openai.yaml"
        if not skill_md.exists():
            fail(errors, f"{skill_md}: missing")
            continue
        if not openai_yaml.exists():
            fail(errors, f"{openai_yaml}: missing")
            continue

        fields = parse_frontmatter(skill_md)
        name = fields.get("name")
        description = fields.get("description")
        if not name or not description:
            fail(errors, f"{skill_md}: missing frontmatter name/description")

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
        if name and f"${name}" not in yaml_text:
            fail(errors, f"{openai_yaml}: default_prompt should mention ${name}")

    declared_skill_names = set(global_skill_names)
    actual_skill_names = {path.name for path in GLOBAL_SKILLS_DIR.iterdir() if path.is_dir()} if GLOBAL_SKILLS_DIR.exists() else set()
    if declared_skill_names != actual_skill_names:
        fail(
            errors,
            f"{GLOBAL_MANIFEST_PATH}: global_skills does not match the skill directories in {GLOBAL_SKILLS_DIR}",
        )

    global_agent_names = manifest.get("global_agents", [])
    if not isinstance(global_agent_names, list) or not global_agent_names:
        fail(errors, f"{GLOBAL_MANIFEST_PATH}: global_agents must be a non-empty list")
        global_agent_names = []

    for agent_name in global_agent_names:
        agent_toml = GLOBAL_AGENTS_DIR / agent_name
        if not agent_toml.exists():
            fail(errors, f"{agent_toml}: missing")
            continue

        try:
            data = tomllib.loads(agent_toml.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            fail(errors, f"{agent_toml}: TOML parse error: {exc}")
            continue

        for key in ("name", "description", "developer_instructions", "sandbox_mode"):
            if not data.get(key):
                fail(errors, f"{agent_toml}: missing {key}")

    declared_agent_names = set(global_agent_names)
    actual_agent_names = {path.name for path in GLOBAL_AGENTS_DIR.glob("*.toml")} if GLOBAL_AGENTS_DIR.exists() else set()
    if declared_agent_names != actual_agent_names:
        fail(
            errors,
            f"{GLOBAL_MANIFEST_PATH}: global_agents does not match the TOMLs in {GLOBAL_AGENTS_DIR}",
        )

    bin_files = manifest.get("bin_files", [])
    if not isinstance(bin_files, list) or not bin_files:
        fail(errors, f"{GLOBAL_MANIFEST_PATH}: bin_files must be a non-empty list")
        bin_files = []

    for bin_name in bin_files:
        bin_path = GLOBAL_BIN_DIR / bin_name
        if not bin_path.exists():
            fail(errors, f"{bin_path}: missing")

    git_path = shutil.which("git")
    if git_path:
        for tracked_path in sorted({*(GLOBAL_BIN_DIR / name for name in bin_files), ROOT_BOOTSTRAP_SH, ROOT_BOOTSTRAP_PS1}):
            result = subprocess.run(
                [git_path, "check-ignore", "-q", str(tracked_path)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                fail(errors, f"{tracked_path}: must not be ignored by git")

    if not ROOT_BOOTSTRAP_SH.exists():
        fail(errors, f"{ROOT_BOOTSTRAP_SH}: missing")
    if not ROOT_BOOTSTRAP_PS1.exists():
        fail(errors, f"{ROOT_BOOTSTRAP_PS1}: missing")

    bash_path = shutil.which("bash")
    if bash_path and ROOT_BOOTSTRAP_SH.exists():
        result = subprocess.run(
            [bash_path, "-n", str(ROOT_BOOTSTRAP_SH)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            fail(
                errors,
                f"{ROOT_BOOTSTRAP_SH}: bash -n failed: {(result.stderr or result.stdout).strip()}",
            )

    for key in ("repo_files", "repo_dirs", "repo_nested_guides", "starter_dirs"):
        values = manifest.get(key, [])
        if not isinstance(values, list):
            fail(errors, f"{GLOBAL_MANIFEST_PATH}: {key} must be a list")
            continue
        if key == "starter_dirs":
            continue
        for relative_path in values:
            target = REPO_ROOT / relative_path
            if not target.exists():
                fail(errors, f"{GLOBAL_MANIFEST_PATH}: referenced repo path is missing: {target}")


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


def validate_runtime_wording(errors: list[str]) -> None:
    runtime_files = sorted(SKILLS_DIR.glob("*/SKILL.md")) + sorted(AGENTS_DIR.glob("*.toml"))
    if FRAMEWORK_AGENTS_PATH.exists():
        runtime_files.append(FRAMEWORK_AGENTS_PATH)

    for path in runtime_files:
        text = path.read_text(encoding="utf-8")
        for needle, explanation in STALE_RUNTIME_PATTERNS.items():
            if needle in text:
                fail(errors, f"{path}: stale runtime wording '{needle}' ({explanation})")


def validate_docs_wording(errors: list[str]) -> None:
    doc_files: list[Path] = []
    for surface in DOC_SURFACES:
        if surface.is_file():
            doc_files.append(surface)
            continue
        if surface.is_dir():
            doc_files.extend(sorted(surface.rglob("*.md")))
            doc_files.extend(sorted(surface.rglob("*.yaml")))
            doc_files.extend(sorted(surface.rglob("*.yml")))

    seen: set[Path] = set()
    for path in doc_files:
        if path in seen:
            continue
        seen.add(path)
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as exc:
            fail(errors, f"{path}: could not read doc for validation: {exc}")
            continue

        for needle, explanation in STALE_DOC_PATTERNS.items():
            if needle in text:
                fail(errors, f"{path}: stale documentation wording '{needle}' ({explanation})")


def validate_scenarios(errors: list[str]) -> None:
    if not SCENARIOS_DIR.exists():
        return

    scenario_count = 0
    for scenario_path in sorted(SCENARIOS_DIR.glob("*.json")):
        scenario_count += 1
        try:
            spec = json.loads(scenario_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(errors, f"{scenario_path}: JSON parse error: {exc}")
            continue

        for key in ("name", "fixture", "turns"):
            if key not in spec:
                fail(errors, f"{scenario_path}: missing required key '{key}'")

        covers = spec.get("covers")
        if not isinstance(covers, list) or not covers:
            fail(errors, f"{scenario_path}: covers must be a non-empty list")
        else:
            for index, cover in enumerate(covers, start=1):
                if not isinstance(cover, str) or not cover.strip():
                    fail(errors, f"{scenario_path}: cover {index} must be a non-empty string")

        turns = spec.get("turns")
        if not isinstance(turns, list) or not turns:
            fail(errors, f"{scenario_path}: turns must be a non-empty list")
        else:
            for index, turn in enumerate(turns, start=1):
                if not isinstance(turn, dict):
                    fail(errors, f"{scenario_path}: turn {index} must be an object")
                    continue
                prompt = turn.get("prompt")
                if not isinstance(prompt, str) or not prompt.strip():
                    fail(errors, f"{scenario_path}: turn {index} missing prompt")
                expect_regex = turn.get("expect_regex")
                if expect_regex is not None and not isinstance(expect_regex, str):
                    fail(errors, f"{scenario_path}: turn {index} expect_regex must be a string")
                if isinstance(expect_regex, str):
                    try:
                        re.compile(expect_regex)
                    except re.error as exc:
                        fail(errors, f"{scenario_path}: turn {index} invalid expect_regex: {exc}")

        fixture_name = spec.get("fixture")
        if isinstance(fixture_name, str):
            fixture_dir = STATES_DIR / fixture_name
            if not fixture_dir.exists():
                fail(errors, f"{scenario_path}: missing fixture state {fixture_dir}")
        else:
            fail(errors, f"{scenario_path}: fixture must be a string")

        assertions = spec.get("assertions", [])
        if not isinstance(assertions, list):
            fail(errors, f"{scenario_path}: assertions must be a list")
        else:
            for index, assertion in enumerate(assertions, start=1):
                if not isinstance(assertion, dict):
                    fail(errors, f"{scenario_path}: assertion {index} must be an object")
                    continue
                assertion_type = assertion.get("type")
                if assertion_type not in {
                    "path_exists",
                    "path_not_exists",
                    "file_contains",
                    "glob_count",
                }:
                    fail(errors, f"{scenario_path}: assertion {index} uses unsupported type '{assertion_type}'")

    if scenario_count == 0:
        fail(errors, f"{SCENARIOS_DIR}: no scenario JSON files found")


def validate_workflow_matrix(errors: list[str]) -> None:
    matrix = build_matrix()
    for error in matrix.get("errors", []):
        fail(errors, error)

    summary = matrix.get("summary", {})
    workflow_catalog = load_yaml(WORKFLOW_CATALOG_PATH)
    expected_workflow_steps = sum(
        len(phase.get("steps", []))
        for phase in workflow_catalog.get("phases", {}).values()
    )
    if summary.get("skills_total") != len(list(SKILLS_DIR.glob("*/SKILL.md"))):
        fail(errors, "workflow matrix did not enumerate every repo skill")
    if summary.get("agents_total") != len(list(AGENTS_DIR.glob("*.toml"))):
        fail(errors, "workflow matrix did not enumerate every custom agent")
    if summary.get("workflow_steps_total") != expected_workflow_steps:
        fail(
            errors,
            f"expected workflow matrix to enumerate {expected_workflow_steps} workflow steps, found {summary.get('workflow_steps_total')}",
        )


def main() -> int:
    errors: list[str] = []
    validate_skills(errors)
    validate_agents(errors)
    validate_global_pack(errors)
    validate_project_config(errors)
    validate_hooks(errors)
    validate_runtime_wording(errors)
    validate_docs_wording(errors)
    validate_scenarios(errors)
    validate_workflow_matrix(errors)

    if errors:
        print("Codex-native validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Codex-native validation passed.")
    print(f"Skills checked: {len(list(SKILLS_DIR.glob('*/SKILL.md')))}")
    print(f"Agents checked: {len(list(AGENTS_DIR.glob('*.toml')))}")
    print(f"Global skills checked: {len(list(GLOBAL_SKILLS_DIR.glob('*/SKILL.md')))}")
    print(f"Global agents checked: {len(list(GLOBAL_AGENTS_DIR.glob('*.toml')))}")
    print(f"Hooks checked: {len(list(HOOKS_DIR.glob('*.sh')))}")
    print(f"Scenarios checked: {len(list(SCENARIOS_DIR.glob('*.json')))}")
    print(f"Workflow variants checked: {build_matrix()['summary']['variants_total']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
