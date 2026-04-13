<p align="center">
  <h1 align="center">Codex Code Game Studios</h1>
  <p align="center">
    Turn a single Codex CLI session into a structured game development studio.
    <br />
    50 custom agents. 84 reusable skills. One consistent workflow.
  </p>
</p>

<p align="center">
  <a href=".codex/agents"><img src="https://img.shields.io/badge/agents-50-blueviolet" alt="50 agents"></a>
  <a href=".agents/skills"><img src="https://img.shields.io/badge/skills-84-green" alt="84 skills"></a>
  <a href="docs/studio/hooks-reference.md"><img src="https://img.shields.io/badge/supported%20hooks-5-orange" alt="5 supported hooks"></a>
  <a href="docs/studio/rules-reference.md"><img src="https://img.shields.io/badge/path%20guides-11-red" alt="11 path guides"></a>
  <a href="https://github.com/openai/codex"><img src="https://img.shields.io/badge/built%20for-Codex%20CLI-black" alt="Built for Codex CLI"></a>
</p>

---

## What This Repo Is

This repository is a Codex-native port of the original studio framework that
was built for Claude Code. The core idea is unchanged: instead of one generic
AI session, you work with a full studio model that has directors, leads,
specialists, reusable workflows, document templates, and lightweight
automation.

What changed is the surface area:

| Original concept | Codex-native equivalent |
| --- | --- |
| `CLAUDE.md` | `AGENTS.md` |
| `.claude/skills/*/SKILL.md` | `.agents/skills/*/SKILL.md` |
| `.claude/agents/*.md` | `.codex/agents/*.toml` |
| `.claude/rules/*.md` | nested `AGENTS.md` files near the relevant paths |
| `.claude/hooks/*` | `.codex/hooks/*` plus `.codex/hooks.json` |
| Claude-only prompts like `AskUserQuestion` | direct Codex conversation flow with explicit option-setting in skills |

## What Is Included

| Category | Count | Notes |
| --- | --- | --- |
| Custom agents | 49 | Directors, department leads, specialists, and engine experts |
| Skills | 84 | Reusable repo skills for design, engineering, QA, release, orchestration, and Steam publishing |
| Supported hooks | 5 events | `SessionStart`, `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop` are the current Codex hook surfaces |
| Path guides | 11 | Nested `AGENTS.md` files for code, docs, shaders, data, tests, and prototypes |
| Studio docs | 60+ | Workflow docs, templates, gate definitions, and references |

## Codex-Native Layout

```text
/
├── AGENTS.md                     # Root operating guide for Codex
├── .agents/
│   └── skills/                  # 84 repo skills
├── .codex/
│   ├── agents/                  # 49 custom agent definitions (.toml)
│   ├── hooks/                   # Hook scripts kept in repo
│   ├── config.toml              # Project defaults for Codex
│   └── hooks.json               # Hook registration file
├── docs/
│   └── studio/                  # Workflow docs, templates, references
├── design/                      # GDDs, UX, narrative, level docs
├── src/                         # Game source code
├── assets/                      # Art, audio, shaders, data
├── tests/                       # QA and automated tests
├── prototypes/                  # Isolated throwaway experiments
└── production/                  # Sprints, milestones, release tracking
```

## Getting Started

### 1. Install Codex CLI

```bash
npm install -g @openai/codex
```

You can also install via Homebrew or a release binary from the official
[OpenAI Codex repository](https://github.com/openai/codex).

### 2. Clone the Repo

```bash
git clone <your-repo-url> my-game
cd my-game
```

### 3. Start Codex in the Project Root

```bash
codex
```

### 4. Kick Off the Workflow

Mention a repo skill directly in your prompt:

- `$start` for first-time routing
- `$help` for “what should I do next?”
- `$brainstorm` to shape a new concept
- `$project-stage-detect` to audit an existing game project
- `$setup-engine godot 4.6` or another engine-specific setup

The skills live in `.agents/skills/`, so you can inspect or customize them just
like any other part of the project.

## How This Repo Uses Codex

- Root guidance lives in `AGENTS.md`.
- Path-specific rules live in nested `AGENTS.md` files, so Codex picks up the
  closest instructions for gameplay code, shaders, tests, narrative docs, and
  other domains.
- Custom agent definitions live in `.codex/agents/*.toml`.
- Project hooks are wired from `.codex/hooks.json`, and `.codex/config.toml`
  explicitly enables `features.codex_hooks = true`.
- Project defaults are stored in `.codex/config.toml`.

Only hook events supported by current Codex releases are wired by default.
Legacy compatibility scripts are still kept under `.codex/hooks/` for reference,
but unsupported Claude-specific hook events are not registered.

## Codex-Native Ergonomics

- Every repo skill now ships `agents/openai.yaml`, so Codex can use metadata for
  UI labels, default prompts, and invocation policy.
- Heavy orchestration workflows are marked explicit-only by default. Lightweight
  review and analysis skills remain eligible for implicit triggering.
- Every custom agent TOML now declares `sandbox_mode` and
  `nickname_candidates`, which makes spawned threads more predictable and easier
  to distinguish in the UI.
- Project defaults now pin `[agents].max_threads = 6` and `max_depth = 1` to
  match current Codex guidance for predictable fan-out.
- Repo-local hook commands now resolve from the git root instead of relative
  `.codex/hooks/...` paths, which keeps them stable when Codex is launched from
  a subdirectory.
- File-based validation now runs at `Stop` and `git commit` time instead of
  pretending `PostToolUse` can see `Write` and `Edit`. Current Codex hook
  runtime only emits `Bash` for `PreToolUse` and `PostToolUse`, so this repo now
  avoids no-op hook matchers.
- Run `python3 scripts/validate_codex_native.py` after repo-level skill or
  agent changes to catch contract drift early, including hook feature flags,
  matcher no-ops, unsupported hook keys, and hook script syntax.

## Workflow Overview

The studio model is organized around seven phases:

1. Concept
2. Systems Design
3. Technical Setup
4. Pre-Production
5. Production
6. Polish
7. Release

The docs that drive those phases live in:

- `docs/studio/quick-start.md`
- `docs/WORKFLOW-GUIDE.md`
- `docs/studio/workflow-catalog.yaml`
- `docs/studio/director-gates.md`

## Customizing the Studio

- Edit `AGENTS.md` to change the repo-wide operating model.
- Edit nested `AGENTS.md` files to change domain-specific standards.
- Add or refine workflows in `.agents/skills/`.
- Tune project defaults in `.codex/config.toml`.
- Add or remove supported hooks in `.codex/hooks.json`.

If you change a skill description, invocation policy, or agent metadata, run:

```bash
python3 scripts/sync_codex_metadata.py
python3 scripts/validate_codex_native.py
```

For higher-fidelity workflow testing in throwaway repo copies, run:

```bash
python3 scripts/run_codex_scenarios.py
```

To generate the repo's machine-checkable workflow coverage matrix, run:

```bash
python3 scripts/build_workflow_matrix.py
```

To refresh the matrix against live skill probes and fixture scenarios in one go, run:

```bash
python3 scripts/build_workflow_matrix.py --refresh-live
```

This performs the full sequential live sweep (skills, agents, then fixture scenarios), so expect it to take noticeably longer than static validation.

The generated outputs land in:

- `docs/studio/workflow-coverage-matrix.json`
- `docs/studio/workflow-coverage-matrix.md`

The fixture overlays and scenario definitions live under `fixtures/e2e/`.

## Attribution

This repository preserves the studio architecture and workflow intent of the
original `Claude-Code-Game-Studios` project while translating it to Codex CLI
concepts and project structure.

## License

Released under the [MIT License](LICENSE).
