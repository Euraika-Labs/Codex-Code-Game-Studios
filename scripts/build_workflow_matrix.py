#!/usr/bin/env python3
"""Build a machine-readable coverage matrix for repo-defined Codex workflows."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import tomllib
from typing import Any

try:
    import yaml
except Exception as exc:  # pragma: no cover - hard dependency for this script
    raise SystemExit(f"PyYAML is required to build the workflow matrix: {exc}") from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"
AGENTS_DIR = REPO_ROOT / ".codex" / "agents"
WORKFLOW_CATALOG_PATH = REPO_ROOT / "docs" / "studio" / "workflow-catalog.yaml"
TEST_CATALOG_PATH = REPO_ROOT / "Codex Skill Testing Framework" / "catalog.yaml"
SCENARIOS_DIR = REPO_ROOT / "fixtures" / "e2e" / "scenarios"
DEFAULT_JSON_OUTPUT = REPO_ROOT / "docs" / "studio" / "workflow-coverage-matrix.json"
DEFAULT_MARKDOWN_OUTPUT = REPO_ROOT / "docs" / "studio" / "workflow-coverage-matrix.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--probe-summary",
        default=None,
        help="Optional summary.json emitted by scripts/run_codex_e2e.py.",
    )
    parser.add_argument(
        "--scenario-summary",
        default=None,
        help="Optional summary.json emitted by scripts/run_codex_scenarios.py.",
    )
    parser.add_argument(
        "--refresh-live",
        action="store_true",
        help="Run live skill/agent probes and fixture scenarios before building the matrix.",
    )
    parser.add_argument(
        "--json-out",
        default=str(DEFAULT_JSON_OUTPUT),
        help="Path for the generated JSON matrix.",
    )
    parser.add_argument(
        "--markdown-out",
        default=str(DEFAULT_MARKDOWN_OUTPUT),
        help="Path for the generated Markdown summary.",
    )
    parser.add_argument(
        "--reasoning-effort",
        default="low",
        help="Reasoning effort for live runs triggered via --refresh-live.",
    )
    parser.add_argument(
        "--probe-timeout",
        type=int,
        default=180,
        help="Per-probe timeout passed to scripts/run_codex_e2e.py when --refresh-live is used.",
    )
    parser.add_argument(
        "--scenario-timeout",
        type=int,
        default=240,
        help="Per-turn timeout passed to scripts/run_codex_scenarios.py when --refresh-live is used.",
    )
    parser.add_argument(
        "--scenario-model",
        default="gpt-5.4-mini",
        help="Model passed to scripts/run_codex_scenarios.py when --refresh-live is used.",
    )
    return parser.parse_args()


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        return {}
    return {str(key): "" if value is None else str(value) for key, value in data.items()}


def normalize_command(command: str) -> str:
    return command[1:] if command.startswith("$") else command


def skill_metadata(skill_dir: Path) -> dict[str, Any]:
    skill_md = skill_dir / "SKILL.md"
    fields = parse_frontmatter(skill_md)
    openai_yaml_path = skill_dir / "agents" / "openai.yaml"
    openai_yaml = load_yaml(openai_yaml_path) if openai_yaml_path.exists() else {}
    if not isinstance(openai_yaml, dict):
        openai_yaml = {}

    skill_text = skill_md.read_text(encoding="utf-8")
    interface = openai_yaml.get("interface", {}) if isinstance(openai_yaml.get("interface"), dict) else {}
    policy = openai_yaml.get("policy", {}) if isinstance(openai_yaml.get("policy"), dict) else {}

    lower_text = skill_text.lower()
    asks_write_approval = bool(
        re.search(r"May I (write|create|modify|update|save)", skill_text)
    ) or (
        ("approval" in lower_text or "ask before" in lower_text)
        and any(
            phrase in lower_text
            for phrase in (
                "write",
                "create file",
                "create files",
                "modify",
                "overwrite",
                "save",
            )
        )
    )

    return {
        "name": fields.get("name") or skill_dir.name,
        "description": fields.get("description", ""),
        "path": str(skill_md.relative_to(REPO_ROOT)),
        "openai_yaml_path": str(openai_yaml_path.relative_to(REPO_ROOT)) if openai_yaml_path.exists() else "",
        "implicit_allowed": bool(policy.get("allow_implicit_invocation", True)),
        "default_prompt": interface.get("default_prompt", ""),
        "display_name": interface.get("display_name", fields.get("name") or skill_dir.name),
        "short_description": interface.get("short_description", fields.get("description", "")),
        "write_approval": asks_write_approval,
    }


def load_skills() -> dict[str, dict[str, Any]]:
    return {
        skill_dir.name: skill_metadata(skill_dir)
        for skill_dir in sorted(SKILLS_DIR.iterdir())
        if (skill_dir / "SKILL.md").exists()
    }


def load_agents() -> dict[str, dict[str, Any]]:
    agents: dict[str, dict[str, Any]] = {}
    for agent_toml in sorted(AGENTS_DIR.glob("*.toml")):
        data = tomllib.loads(agent_toml.read_text(encoding="utf-8"))
        name = str(data.get("name") or agent_toml.stem)
        agents[name] = {
            "name": name,
            "path": str(agent_toml.relative_to(REPO_ROOT)),
            "description": str(data.get("description", "")),
            "sandbox_mode": str(data.get("sandbox_mode", "")),
            "model": str(data.get("model", "")),
            "reasoning_effort": str(data.get("model_reasoning_effort", "")),
        }
    return agents


def load_workflow_steps() -> list[dict[str, Any]]:
    catalog = load_yaml(WORKFLOW_CATALOG_PATH)
    steps: list[dict[str, Any]] = []
    for phase_name, phase in catalog["phases"].items():
        for step in phase.get("steps", []):
            if step.get("command"):
                commands = [normalize_command(step["command"])]
            else:
                commands = sorted(set(re.findall(r"\$([a-z0-9-]+)", step.get("description", "")))) or [None]
            for command in commands:
                steps.append(
                    {
                        "phase": phase_name,
                        "phase_label": phase.get("label", phase_name),
                        "step_id": step["id"],
                        "step_name": step.get("name", step["id"]),
                        "command": command,
                        "required": bool(step.get("required", False)),
                        "repeatable": bool(step.get("repeatable", False)),
                        "description": step.get("description", ""),
                        "artifact": step.get("artifact", {}),
                    }
                )
    return steps


def load_test_catalog() -> dict[str, dict[str, Any]]:
    catalog = load_yaml(TEST_CATALOG_PATH)
    entries: dict[str, dict[str, Any]] = {}
    for entry in catalog.get("skills", []):
        name = str(entry["name"])
        entries[name] = {
            "spec": str(entry.get("spec", "")),
            "category": str(entry.get("category", "")),
            "priority": str(entry.get("priority", "")),
        }
    return entries


def load_scenarios() -> tuple[dict[str, list[str]], list[str]]:
    coverage_map: dict[str, list[str]] = defaultdict(list)
    errors: list[str] = []
    for path in sorted(SCENARIOS_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        scenario_name = data.get("name", path.stem)
        covers = data.get("covers")
        if not isinstance(covers, list) or not covers:
            errors.append(f"{path.relative_to(REPO_ROOT)}: missing non-empty covers list")
            continue
        for variant_id in covers:
            coverage_map[str(variant_id)].append(str(scenario_name))
    return coverage_map, errors


def load_probe_summary(path: Path | None) -> dict[tuple[str, str], bool]:
    if path is None or not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    statuses: dict[tuple[str, str], bool] = {}
    for result in data.get("results", []):
        kind = str(result.get("kind", ""))
        name = str(result.get("name", ""))
        if kind and name:
            statuses[(kind, name)] = bool(result.get("ok", False))
    return statuses


def load_scenario_summary(path: Path | None) -> dict[str, bool]:
    if path is None or not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        str(result.get("name", "")): bool(result.get("ok", False))
        for result in data.get("results", [])
        if result.get("name")
    }


def live_status_for_scenarios(names: list[str], scenario_results: dict[str, bool]) -> str:
    if not names:
        return "missing"
    if not scenario_results:
        return "defined"
    statuses = [scenario_results.get(name) for name in names]
    if any(status is False for status in statuses):
        return "fail"
    if all(status is True for status in statuses):
        return "pass"
    return "defined"


def evidence_status(*, expected: list[str], present: dict[str, bool], key: tuple[str, str] | None = None) -> str:
    if key is None:
        return "n/a"
    if not present:
        return "untracked"
    return "pass" if present.get(key, False) else "fail"


def obligation_status(row: dict[str, Any]) -> str:
    static_ok = row["coverage"]["static"] == "present"
    spec_ok = row["coverage"]["spec"] == "present"
    probe_ok = row["coverage"]["live_probe"] == "pass"
    scenario_ok = row["coverage"]["scenario"] == "pass"

    kind = row["obligation_kind"]
    surface = row["surface_kind"]
    if surface == "custom-agent":
        if probe_ok:
            return "complete"
        return "partial" if row["coverage"]["live_probe"] in {"untracked", "defined"} else "missing"

    if kind == "base-flow":
        if static_ok and spec_ok and (probe_ok or scenario_ok):
            return "complete"
        if static_ok and spec_ok:
            return "partial"
        return "missing"

    if kind in {"repeatable-iteration", "write-approval"}:
        if static_ok and spec_ok and scenario_ok:
            return "complete"
        if static_ok and spec_ok:
            return "partial"
        return "missing"

    if kind == "manual-artifact-gate":
        if scenario_ok:
            return "complete"
        if row["coverage"]["scenario"] == "defined":
            return "partial"
        return "missing"

    return "partial"


def workflow_priority(required: bool, obligation_kind: str) -> str:
    if obligation_kind == "manual-artifact-gate":
        return "high" if required else "medium"
    if required and obligation_kind == "base-flow":
        return "critical"
    if required:
        return "high"
    if obligation_kind == "base-flow":
        return "medium"
    return "low"


def support_priority(obligation_kind: str) -> str:
    return "medium" if obligation_kind == "base-flow" else "low"


def agent_priority() -> str:
    return "medium"


def build_matrix(
    *,
    probe_summary_path: Path | None = None,
    scenario_summary_path: Path | None = None,
) -> dict[str, Any]:
    skills = load_skills()
    agents = load_agents()
    workflow_steps = load_workflow_steps()
    test_catalog = load_test_catalog()
    scenario_map, scenario_errors = load_scenarios()
    probe_results = load_probe_summary(probe_summary_path)
    scenario_results = load_scenario_summary(scenario_summary_path)

    workflow_commands = {step["command"] for step in workflow_steps if step["command"]}
    variants: list[dict[str, Any]] = []
    variant_ids: set[str] = set()

    def add_variant(row: dict[str, Any]) -> None:
        variant_id = row["variant_id"]
        if variant_id in variant_ids:
            raise ValueError(f"duplicate workflow variant id: {variant_id}")
        row["status"] = obligation_status(row)
        variants.append(row)
        variant_ids.add(variant_id)

    for step in workflow_steps:
        if step["command"] is None:
            coverage_ids = scenario_map.get(
                f"workflow.{step['phase']}.{step['step_id']}.manual-artifact-gate",
                [],
            )
            add_variant(
                {
                    "variant_id": f"workflow.{step['phase']}.{step['step_id']}.manual-artifact-gate",
                    "surface_kind": "workflow-step",
                    "obligation_kind": "manual-artifact-gate",
                    "priority": workflow_priority(step["required"], "manual-artifact-gate"),
                    "phase": step["phase"],
                    "step_id": step["step_id"],
                    "step_name": step["step_name"],
                    "target": "(manual)",
                    "required": step["required"],
                    "repeatable": step["repeatable"],
                    "description": step["description"],
                    "artifact": step["artifact"],
                    "skill_path": None,
                    "implicit_allowed": False,
                    "write_approval": False,
                    "coverage": {
                        "static": "n/a",
                        "spec": "n/a",
                        "live_probe": "n/a",
                        "scenario": live_status_for_scenarios(coverage_ids, scenario_results),
                        "scenario_ids": coverage_ids,
                    },
                }
            )
            continue

        skill = skills[step["command"]]
        coverage_ids = scenario_map.get(
            f"workflow.{step['phase']}.{step['step_id']}.{step['command']}.base-flow",
            [],
        )
        add_variant(
            {
                "variant_id": f"workflow.{step['phase']}.{step['step_id']}.{step['command']}.base-flow",
                "surface_kind": "workflow-step",
                "obligation_kind": "base-flow",
                "priority": workflow_priority(step["required"], "base-flow"),
                "phase": step["phase"],
                "step_id": step["step_id"],
                "step_name": step["step_name"],
                "target": step["command"],
                "required": step["required"],
                "repeatable": step["repeatable"],
                "description": step["description"],
                "artifact": step["artifact"],
                "skill_path": skill["path"],
                "implicit_allowed": skill["implicit_allowed"],
                "write_approval": skill["write_approval"],
                "coverage": {
                    "static": "present",
                    "spec": "present" if step["command"] in test_catalog else "missing",
                    "live_probe": evidence_status(
                        expected=["skill"],
                        present=probe_results,
                        key=("skill", step["command"]),
                    ),
                    "scenario": live_status_for_scenarios(coverage_ids, scenario_results),
                    "scenario_ids": coverage_ids,
                },
            }
        )

        if step["repeatable"]:
            repeat_id = f"workflow.{step['phase']}.{step['step_id']}.{step['command']}.repeatable-iteration"
            coverage_ids = scenario_map.get(repeat_id, [])
            add_variant(
                {
                    "variant_id": repeat_id,
                    "surface_kind": "workflow-step",
                    "obligation_kind": "repeatable-iteration",
                    "priority": workflow_priority(step["required"], "repeatable-iteration"),
                    "phase": step["phase"],
                    "step_id": step["step_id"],
                    "step_name": step["step_name"],
                    "target": step["command"],
                    "required": step["required"],
                    "repeatable": True,
                    "description": step["description"],
                    "artifact": step["artifact"],
                    "skill_path": skill["path"],
                    "implicit_allowed": skill["implicit_allowed"],
                    "write_approval": skill["write_approval"],
                    "coverage": {
                        "static": "present",
                        "spec": "present" if step["command"] in test_catalog else "missing",
                        "live_probe": evidence_status(
                            expected=["skill"],
                            present=probe_results,
                            key=("skill", step["command"]),
                        ),
                        "scenario": live_status_for_scenarios(coverage_ids, scenario_results),
                        "scenario_ids": coverage_ids,
                    },
                }
            )

        if skill["write_approval"]:
            approval_id = f"workflow.{step['phase']}.{step['step_id']}.{step['command']}.write-approval"
            coverage_ids = scenario_map.get(approval_id, [])
            add_variant(
                {
                    "variant_id": approval_id,
                    "surface_kind": "workflow-step",
                    "obligation_kind": "write-approval",
                    "priority": workflow_priority(step["required"], "write-approval"),
                    "phase": step["phase"],
                    "step_id": step["step_id"],
                    "step_name": step["step_name"],
                    "target": step["command"],
                    "required": step["required"],
                    "repeatable": step["repeatable"],
                    "description": step["description"],
                    "artifact": step["artifact"],
                    "skill_path": skill["path"],
                    "implicit_allowed": skill["implicit_allowed"],
                    "write_approval": True,
                    "coverage": {
                        "static": "present",
                        "spec": "present" if step["command"] in test_catalog else "missing",
                        "live_probe": evidence_status(
                            expected=["skill"],
                            present=probe_results,
                            key=("skill", step["command"]),
                        ),
                        "scenario": live_status_for_scenarios(coverage_ids, scenario_results),
                        "scenario_ids": coverage_ids,
                    },
                }
            )

    support_skill_names = sorted(set(skills) - workflow_commands)
    for name in support_skill_names:
        skill = skills[name]
        coverage_ids = scenario_map.get(f"support.{name}.base-flow", [])
        add_variant(
            {
                "variant_id": f"support.{name}.base-flow",
                "surface_kind": "support-skill",
                "obligation_kind": "base-flow",
                "priority": support_priority("base-flow"),
                "phase": None,
                "step_id": None,
                "step_name": None,
                "target": name,
                "required": False,
                "repeatable": False,
                "description": skill["description"],
                "artifact": {},
                "skill_path": skill["path"],
                "implicit_allowed": skill["implicit_allowed"],
                "write_approval": skill["write_approval"],
                "coverage": {
                    "static": "present",
                    "spec": "present" if name in test_catalog else "missing",
                    "live_probe": evidence_status(
                        expected=["skill"],
                        present=probe_results,
                        key=("skill", name),
                    ),
                    "scenario": live_status_for_scenarios(coverage_ids, scenario_results),
                    "scenario_ids": coverage_ids,
                },
            }
        )

        if skill["write_approval"]:
            coverage_ids = scenario_map.get(f"support.{name}.write-approval", [])
            add_variant(
                {
                    "variant_id": f"support.{name}.write-approval",
                    "surface_kind": "support-skill",
                    "obligation_kind": "write-approval",
                    "priority": support_priority("write-approval"),
                    "phase": None,
                    "step_id": None,
                    "step_name": None,
                    "target": name,
                    "required": False,
                    "repeatable": False,
                    "description": skill["description"],
                    "artifact": {},
                    "skill_path": skill["path"],
                    "implicit_allowed": skill["implicit_allowed"],
                    "write_approval": True,
                    "coverage": {
                        "static": "present",
                        "spec": "present" if name in test_catalog else "missing",
                        "live_probe": evidence_status(
                            expected=["skill"],
                            present=probe_results,
                            key=("skill", name),
                        ),
                        "scenario": live_status_for_scenarios(coverage_ids, scenario_results),
                        "scenario_ids": coverage_ids,
                    },
                }
            )

    for name, agent in sorted(agents.items()):
        add_variant(
            {
                "variant_id": f"agent.{name}.subagent-spawn",
                "surface_kind": "custom-agent",
                "obligation_kind": "subagent-spawn",
                "priority": agent_priority(),
                "phase": None,
                "step_id": None,
                "step_name": None,
                "target": name,
                "required": False,
                "repeatable": False,
                "description": agent["description"],
                "artifact": {},
                "skill_path": None,
                "agent_path": agent["path"],
                "implicit_allowed": False,
                "write_approval": False,
                "coverage": {
                    "static": "present",
                    "spec": "n/a",
                    "live_probe": evidence_status(
                        expected=["agent"],
                        present=probe_results,
                        key=("agent", name),
                    ),
                    "scenario": "n/a",
                    "scenario_ids": [],
                },
            }
        )

    errors = list(scenario_errors)
    unknown_cover_refs = sorted(set(scenario_map) - variant_ids)
    for variant_id in unknown_cover_refs:
        errors.append(f"fixtures/e2e/scenarios: cover reference does not match any known variant id: {variant_id}")

    status_counts = Counter(row["status"] for row in variants)
    surface_counts = Counter(row["surface_kind"] for row in variants)
    priority_counts = Counter(row["priority"] for row in variants)
    uncovered_required = [
        row for row in variants if row["priority"] in {"critical", "high"} and row["status"] != "complete"
    ]

    unique_workflow_steps = len({(step["phase"], step["step_id"]) for step in workflow_steps})

    return {
        "repo_root": ".",
        "probe_summary_supplied": probe_summary_path is not None,
        "scenario_summary_supplied": scenario_summary_path is not None,
        "summary": {
            "skills_total": len(skills),
            "workflow_steps_total": unique_workflow_steps,
            "workflow_commands_total": len(workflow_commands),
            "support_skills_total": len(support_skill_names),
            "agents_total": len(agents),
            "variants_total": len(variants),
            "status_counts": dict(status_counts),
            "surface_counts": dict(surface_counts),
            "priority_counts": dict(priority_counts),
            "uncovered_required_total": len(uncovered_required),
        },
        "variants": variants,
        "errors": errors,
    }


def render_markdown(matrix: dict[str, Any]) -> str:
    summary = matrix["summary"]
    variants = matrix["variants"]
    uncovered = [
        row for row in variants if row["priority"] in {"critical", "high"} and row["status"] != "complete"
    ]
    uncovered.sort(
        key=lambda row: (
            {"critical": 0, "high": 1, "medium": 2, "low": 3}[row["priority"]],
            row["surface_kind"],
            row["target"],
            row["obligation_kind"],
        )
    )

    lines = [
        "<!-- Generated by scripts/build_workflow_matrix.py; do not edit by hand. -->",
        "# Workflow Coverage Matrix",
        "",
        "This file defines the repo's finite, machine-checkable workflow surface for Codex-native testing.",
        "",
        "The matrix treats the following as distinct coverage obligations:",
        "",
        "- `base-flow`: primary invocation path for a workflow step, support skill, or agent spawn",
        "- `repeatable-iteration`: repeatable phase-step behavior that should hold for subsequent runs",
        "- `write-approval`: the explicit human-approval gate before a skill writes files",
        "- `subagent-spawn`: successful custom-agent invocation through Codex subagent tooling",
        "",
        "## Summary",
        "",
        f"- Skills: `{summary['skills_total']}`",
        f"- Workflow steps: `{summary['workflow_steps_total']}`",
        f"- Workflow commands: `{summary['workflow_commands_total']}`",
        f"- Support skills: `{summary['support_skills_total']}`",
        f"- Custom agents: `{summary['agents_total']}`",
        f"- Coverage obligations: `{summary['variants_total']}`",
        f"- Complete obligations: `{summary['status_counts'].get('complete', 0)}`",
        f"- Partial obligations: `{summary['status_counts'].get('partial', 0)}`",
        f"- Missing obligations: `{summary['status_counts'].get('missing', 0)}`",
        f"- Critical/high obligations not complete: `{summary['uncovered_required_total']}`",
        "",
        "## Evidence Sources",
        "",
        f"- Probe summary supplied: `{str(matrix.get('probe_summary_supplied', False)).lower()}`",
        f"- Scenario summary supplied: `{str(matrix.get('scenario_summary_supplied', False)).lower()}`",
        "",
        "## Required Gaps",
        "",
        "| Priority | Variant | Target | Coverage |",
        "| --- | --- | --- | --- |",
    ]
    if uncovered:
        for row in uncovered[:40]:
            coverage = row["coverage"]
            coverage_text = (
                f"static={coverage['static']}, spec={coverage['spec']}, "
                f"probe={coverage['live_probe']}, scenario={coverage['scenario']}"
            )
            lines.append(
                f"| {row['priority']} | `{row['variant_id']}` | `{row['target']}` | {coverage_text} |"
            )
    else:
        lines.append("| none | - | - | - |")

    lines.extend(
        [
            "",
            "## Workflow Obligations",
            "",
            "| Phase | Step | Command | Obligation | Priority | Status | Scenario IDs |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in variants:
        if row["surface_kind"] != "workflow-step":
            continue
        scenario_ids = ", ".join(f"`{name}`" for name in row["coverage"]["scenario_ids"]) or "-"
        lines.append(
            "| "
            f"{row['phase']} | {row['step_id']} | `{row['target']}` | {row['obligation_kind']} | "
            f"{row['priority']} | {row['status']} | {scenario_ids} |"
        )

    lines.extend(
        [
            "",
            "## Support Skill Obligations",
            "",
            "| Skill | Obligation | Status | Scenario IDs |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in variants:
        if row["surface_kind"] != "support-skill":
            continue
        scenario_ids = ", ".join(f"`{name}`" for name in row["coverage"]["scenario_ids"]) or "-"
        lines.append(f"| `{row['target']}` | {row['obligation_kind']} | {row['status']} | {scenario_ids} |")

    lines.extend(
        [
            "",
            "## Custom Agent Obligations",
            "",
            "| Agent | Sandbox | Status | Live Probe |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in variants:
        if row["surface_kind"] != "custom-agent":
            continue
        agent_path = REPO_ROOT / row["agent_path"]
        agent_data = tomllib.loads(agent_path.read_text(encoding="utf-8"))
        sandbox_mode = str(agent_data.get("sandbox_mode", ""))
        lines.append(
            f"| `{row['target']}` | `{sandbox_mode}` | {row['status']} | {row['coverage']['live_probe']} |"
        )

    if matrix["errors"]:
        lines.extend(["", "## Matrix Errors", ""])
        for error in matrix["errors"]:
            lines.append(f"- {error}")

    return "\n".join(lines) + "\n"


def write_outputs(matrix: dict[str, Any], *, json_out: Path, markdown_out: Path) -> None:
    json_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(matrix, indent=2), encoding="utf-8")
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.write_text(render_markdown(matrix), encoding="utf-8")


def run_live_suite(args: argparse.Namespace) -> tuple[Path, Path]:
    temp_root = Path(tempfile.mkdtemp(prefix="codex-workflow-matrix-"))
    probe_dir = temp_root / "probes"
    scenario_dir = temp_root / "scenarios"
    probe_dir.mkdir(parents=True, exist_ok=True)
    scenario_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "run_codex_e2e.py"),
            "--mode",
            "all",
            "--timeout",
            str(args.probe_timeout),
            "--reasoning-effort",
            args.reasoning_effort,
            "--results-dir",
            str(probe_dir),
        ],
        cwd=REPO_ROOT,
        check=True,
    )
    subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "run_codex_scenarios.py"),
            "--timeout",
            str(args.scenario_timeout),
            "--reasoning-effort",
            args.reasoning_effort,
            "--model",
            args.scenario_model,
            "--results-dir",
            str(scenario_dir),
        ],
        cwd=REPO_ROOT,
        check=True,
    )
    return probe_dir / "summary.json", scenario_dir / "summary.json"


def main() -> int:
    args = parse_args()
    probe_summary = Path(args.probe_summary) if args.probe_summary else None
    scenario_summary = Path(args.scenario_summary) if args.scenario_summary else None

    if args.refresh_live:
        probe_summary, scenario_summary = run_live_suite(args)

    matrix = build_matrix(
        probe_summary_path=probe_summary,
        scenario_summary_path=scenario_summary,
    )
    write_outputs(
        matrix,
        json_out=Path(args.json_out),
        markdown_out=Path(args.markdown_out),
    )
    print(f"Wrote JSON matrix to {args.json_out}")
    print(f"Wrote Markdown matrix to {args.markdown_out}")
    if matrix["errors"]:
        for error in matrix["errors"]:
            print(f"ERROR: {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
