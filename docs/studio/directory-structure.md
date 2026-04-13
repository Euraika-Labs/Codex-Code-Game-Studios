# Directory Structure

This repo separates workflow infrastructure from project artifacts.
That separation is what makes the skills, gates, and templates predictable.

```text
/
├── AGENTS.md
├── .agents/skills/
├── .codex/agents/
├── .codex/hooks/
├── .codex/config.toml
├── .codex/hooks.json
├── design/
├── src/
├── assets/
├── tests/
├── prototypes/
├── production/
├── docs/
└── global-pack/
```

## Key Areas

### `AGENTS.md`

Root operating guidance for the repo. This is the first place to update when the project changes in a way the framework should know about.

### `.agents/skills/`

Repo-local workflows. Each skill is a reusable operating procedure with a clear scope.

### `.codex/agents/`

Custom agents for leadership, disciplines, engine expertise, release, and specialized analysis.

### `design/`

Design intent and content planning.

Typical subfolders:

- `design/gdd/`
- `design/ux/`
- `design/narrative/`
- `design/levels/`
- `design/balance/`

### `src/`

Implementation code and nested path guidance for discipline-specific standards.

### `assets/`

Art, audio, VFX, shaders, and data that support the game.

### `tests/`

Automated tests, QA utilities, evidence, and nested rules for validation work.

### `prototypes/`

Short-lived experimentation. Keep throwaway proof-of-concept work here instead of mixing it into stable game code.

### `production/`

Delivery state and planning.

Common uses:

- sprint plans
- milestones
- release checklists
- launch runbooks
- playtest reports

### `docs/`

Shared references and durable documentation.

Important subareas:

- `docs/studio/` for the framework handbook and templates
- `docs/examples/` for demonstration sessions and flows
- `docs/engine-reference/` for engine-specific references
- `docs/architecture/` for project ADRs and architecture docs

### `global-pack/`

The lightweight cross-repo install layer for `~/.codex`.

## Keep This Boundary Intact

The framework stays understandable when these lines remain clear:

- design lives in `design/`
- implementation lives in `src/`
- production tracking lives in `production/`
- framework references live in `docs/studio/`
- shared runtime behavior lives in `AGENTS.md`, `.agents/`, and `.codex/`
