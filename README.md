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
| Custom agents | 50 | Directors, department leads, specialists, engine experts, and Steam publishing support |
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
│   ├── agents/                  # 50 custom agent definitions (.toml)
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

## Steam Publishing Setup

If you want to use the new Steamworks-native flows, this is the exact setup
order to follow.

### 1. Prepare the Base Project Context

Before you run any Steam-specific skill, make sure these core project inputs
exist or are at least mostly accurate:

- `AGENTS.md`
- `docs/studio/technical-preferences.md`
- `design/gdd/game-concept.md`
- your normal release artifacts under `production/releases/` if you already
  have them

If the project is still very early, that is fine. The Steam skills can still
draft planning artifacts, but the better your concept and platform info are,
the better the Steam output will be.

### 2. Start With the Base Steam Plan

Run this first:

```bash
codex
```

Then prompt:

```text
Use $steam-publish-plan for this repository. We are shipping a premium Steam PC game.
```

Common variants:

- Premium launch only:
  `Use $steam-publish-plan premium for this repository.`
- Premium + public demo:
  `Use $steam-publish-plan mixed for this repository. We are shipping a premium game with a public demo.`
- Early Access:
  `Use $steam-publish-plan early-access for this repository.`

This creates the master planning artifact at:

- `production/releases/steam/steam-publish-plan.md`

That file is the anchor for everything else in the Steam pack.

### 3. Run the Core Steam Release Sequence

For a normal Steam release, use this order:

1. `$steam-publish-plan`
2. `$steam-coming-soon`
3. `$steam-store-assets`
4. `$steam-review-ready`
5. `$steam-bundles-pricing`
6. `$steam-launch-ops`
7. `$team-release`

Typical prompts:

```text
Use $steam-coming-soon for this repository.
Use $steam-store-assets for this repository.
Use $steam-review-ready for this repository.
Use $steam-bundles-pricing for this repository.
Use $steam-launch-ops for this repository.
```

These write to:

- `production/releases/steam/coming-soon-calendar.md`
- `production/releases/steam/store-assets.md`
- `production/releases/steam/review-ready.md`
- `production/releases/steam/bundles-pricing.md`
- `production/releases/steam/launch-ops.md`

### 4. Add the Variant Flows You Actually Need

Only run the variant skills that match your release shape.

#### Demo

Use when you want a public-facing Steam demo:

```text
Use $steam-demo for this repository.
```

Writes:

- `production/releases/steam/demo-plan.md`

#### Steam Playtest

Use when you want gated signups, invite waves, or load testing before public release:

```text
Use $steam-playtest for this repository.
```

Writes:

- `production/releases/steam/playtest-plan.md`

#### Early Access

Use when the base game itself launches in Early Access:

```text
Use $steam-early-access for this repository.
```

Writes:

- `production/releases/steam/early-access-plan.md`

#### DLC

Use when you are planning paid or free DLC tied to the base game:

```text
Use $steam-dlc for this repository.
```

Writes:

- `production/releases/steam/dlc-plan.md`

#### Soundtrack

Use when the soundtrack should be released as its own Steam product:

```text
Use $steam-soundtrack for this repository.
```

Writes:

- `production/releases/steam/soundtrack-plan.md`

#### Steam Deck

Use when you want an explicit Steam Deck readiness pass:

```text
Use $steam-deck-ready for this repository.
```

Writes:

- `production/releases/steam/steam-deck-ready.md`

### 5. Map Each Release Shape To The Right Flow

- Premium launch only:
  `$steam-publish-plan` -> `$steam-coming-soon` -> `$steam-store-assets` -> `$steam-review-ready` -> `$steam-bundles-pricing` -> `$steam-launch-ops`
- Premium + demo:
  same as above, plus `$steam-demo`
- Premium + gated testing:
  same as above, plus `$steam-playtest`
- Early Access:
  `$steam-publish-plan` -> `$steam-early-access` -> `$steam-coming-soon` -> `$steam-store-assets` -> `$steam-review-ready` -> `$steam-bundles-pricing` -> `$steam-launch-ops`
- Post-launch DLC:
  `$steam-publish-plan` -> `$steam-dlc` -> `$steam-bundles-pricing` -> `$steam-review-ready` -> `$steam-launch-ops`
- Soundtrack:
  `$steam-publish-plan` -> `$steam-soundtrack` -> `$steam-bundles-pricing` -> `$steam-review-ready`

### 6. Keep the Generic Release Flow

The Steam pack does not replace the normal release skills. Keep using:

- `$release-checklist`
- `$launch-checklist`
- `$patch-notes`
- `$changelog`
- `$team-release`

The pattern is:

- generic release skills for broad cross-discipline readiness
- Steam skills for Steamworks-specific app/package/depot/store/review/timing work

### 7. Validate After Editing The Steam Pack

If you change the Steam skills, templates, agent, or docs, run:

```bash
python3 scripts/sync_codex_metadata.py
python3 scripts/validate_codex_native.py
python3 scripts/run_codex_scenarios.py --scenario steam-publish-plan
```

For the full workflow matrix refresh:

```bash
python3 scripts/build_workflow_matrix.py
```

### 8. Where To Read More

- `docs/studio/steam-publishing-guide.md`
- `docs/WORKFLOW-GUIDE.md`
- `docs/studio/templates/steam-*.md`

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
