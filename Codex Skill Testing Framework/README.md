# Codex Skill Testing Framework

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
- If you rename or remove skills, update `catalog.yaml` to keep coverage honest.
