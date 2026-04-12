# Codex Code Game Studios

Use this repository as a structured game-development studio for Codex CLI.

## First Moves

- If the user is new to the project, route through `$start`.
- If the user asks what comes next, use `$help` or `docs/studio/workflow-catalog.yaml`.
- If the project already exists, prefer `$project-stage-detect` before inventing a phase.

## Technology Stack

- **Engine**: [CHOOSE: Godot 4 / Unity / Unreal Engine 5]
- **Language**: [CHOOSE: GDScript / C# / C++ / Blueprint]
- **Version Control**: Git with trunk-based development
- **Build System**: [SPECIFY after choosing engine]
- **Asset Pipeline**: [SPECIFY after choosing engine]

> Engine-specialist agents exist for Godot, Unity, and Unreal. Use the set that
> matches the configured engine and keep this section in sync with
> `docs/studio/technical-preferences.md`.

## Engine Version Reference

docs/engine-reference/[TO BE CONFIGURED]/VERSION.md

## Technical Preferences

docs/studio/technical-preferences.md

## Coordination Rules

docs/studio/coordination-rules.md

## Coding Standards

docs/studio/coding-standards.md

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
- Keep repo skills Codex-native: if you edit a skill, sync and validate its
  metadata with `python3 scripts/sync_codex_metadata.py` and
  `python3 scripts/validate_codex_native.py`.
- Keep design intent in `design/`, technical decisions in `docs/architecture/`,
  delivery state in `production/`, and implementation in `src/`.
- Do not silently make cross-discipline decisions when design, technical, and
  production priorities conflict. Surface options and call out tradeoffs.
- Keep generated or updated docs aligned with the existing templates in
  `docs/studio/templates/`.
- Follow the collaboration rule of draft first, then ask for approval before
  writing project files.

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
