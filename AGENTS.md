# Codex Code Game Studios

Use this repository as a structured game-development studio for Codex CLI.

## First Moves

- If the user is new to the project, route through `$start`.
- If the user asks what comes next, use `$help` or `docs/studio/workflow-catalog.yaml`.
- If the project already exists, prefer `$project-stage-detect` before inventing a phase.

## Repo Surfaces

- Root operating guidance lives here in `AGENTS.md`.
- Path-specific standards live in nested `AGENTS.md` files under `src/`,
  `design/`, `assets/`, `tests/`, and `prototypes/`.
- Reusable workflows live in `.agents/skills/`.
- Custom agent definitions live in `.codex/agents/`.
- Shared project hooks live in `.codex/hooks.json`.
- Shared project defaults live in `.codex/config.toml`.

## Working Style

- Treat skills as the preferred entry point for recurring workflows.
- Keep design intent in `design/`, technical decisions in `docs/architecture/`,
  delivery state in `production/`, and implementation in `src/`.
- Do not silently make cross-discipline decisions when design, technical, and
  production priorities conflict. Surface options and call out tradeoffs.
- Keep generated or updated docs aligned with the existing templates in
  `docs/studio/templates/`.

## Studio Hierarchy

- Directors set direction: `creative-director`, `technical-director`,
  `producer`.
- Leads own domains such as design, programming, art, audio, narrative, QA,
  localization, and release.
- Specialists execute the work inside their discipline and escalate when a
  decision crosses boundaries.

## Migration Guardrails

- Use `AGENTS.md`, never `CLAUDE.md`, for shared repo guidance.
- Use `.agents/skills/`, never `.claude/skills/`, for repo skills.
- Keep only currently supported Codex hook events wired in `.codex/hooks.json`.
- When converting older docs, replace Claude-only workflow language with
  Codex-native instructions.
