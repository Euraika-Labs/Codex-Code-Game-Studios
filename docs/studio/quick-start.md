# Quick Start

This is the shortest practical path to using Codex Code Game Studios.

## 1. Open the repo in Codex

```bash
cd your-game-repo
codex
```

## 2. Pick the right starting command

- `$start` if you want guided routing
- `$help` if you want the next best action
- `$brainstorm` if the concept is still rough
- `$project-stage-detect` if the repo already contains code or docs
- `$setup-engine <engine> <version>` if the engine is already known

## 3. Follow the phase model

The framework organizes work into seven phases:

1. Concept
2. Systems Design
3. Technical Setup
4. Pre-Production
5. Production
6. Polish
7. Release

The full operating handbook lives in `docs/WORKFLOW-GUIDE.md`.

## 4. Know where artifacts go

- design docs: `design/`
- architecture: `docs/architecture/`
- implementation: `src/`
- tests and QA evidence: `tests/`
- production planning: `production/`
- shared framework docs: `docs/studio/`

## 5. Validate shared changes

If you edit shared skills, docs, agents, or install flows, run:

```bash
python3 scripts/sync_codex_metadata.py
python3 scripts/validate_codex_native.py
```

## 6. Use the reference docs when needed

- skills catalog: `docs/studio/skills-reference.md`
- agent roster: `docs/studio/agent-roster.md`
- phase gates: `docs/studio/director-gates.md`
- global bootstrap: `docs/studio/global-install.md`
- Steam publishing: `docs/studio/steam-publishing-guide.md`
