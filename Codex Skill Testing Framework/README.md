# Codex Skill Testing Framework

> Framework-maintenance reference for Codex Code Game Studios. Use this area when validating the skills, agents, and workflow contracts that ship with the framework itself.

Quality-assurance infrastructure for **Codex Code Game Studios** itself.
It tests the skills and agents in this framework, not the game built on top of
it.

> **This folder is self-contained and optional.**
> If you do not want to maintain framework tests in your game repo, you can
> remove `Codex Skill Testing Framework/` without breaking the main studio
> layout.

---

## Contents

```text
Codex Skill Testing Framework/
├── README.md              ← you are here
├── AGENTS.md              ← operating guide for this testing sub-framework
├── catalog.yaml           ← registry of skills, agents, and test coverage
├── quality-rubric.md      ← pass/fail metrics by category
├── skills/                ← behavioral specs for skills
├── agents/                ← behavioral specs for agents
├── templates/             ← templates for new spec files
└── results/               ← test outputs (gitignored)
```

---

## Supported Test Workflows

### Structural validation

```text
$ python3 scripts/validate_codex_native.py
$skill-test static [skill-name]
$skill-test static all
```

### Behavioral spec checks

```text
$skill-test spec gate-check
$skill-test spec design-review
```

### Category rubric checks

```text
$skill-test category gate-check
$skill-test category all
```

### Coverage audit

```text
$skill-test audit
```

### Improve a failing skill

```text
$skill-improve gate-check
```

---

## Notes

- The framework assumes Codex-native repo skills in `.agents/skills/`.
- The framework assumes Codex-native custom agents in `.codex/agents/`.
- The framework assumes each skill also ships `agents/openai.yaml`.
- The framework assumes each agent TOML declares `sandbox_mode` and
  `nickname_candidates`.
- If you rename or remove skills, update `catalog.yaml` to keep coverage honest.
