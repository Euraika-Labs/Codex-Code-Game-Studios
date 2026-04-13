# Codex Code Game Studios

Use this repository as a structured game-development studio for Codex CLI.

## First Moves

- If the project is new or ambiguous, route through `$start`.
- If the user asks what comes next, use `$help` or inspect `docs/studio/workflow-catalog.yaml`.
- If the repo already contains meaningful code or docs, prefer `$project-stage-detect` before picking a phase.
- If engine choice is not locked yet, use `$setup-engine` before architecture or implementation work.

## Technology Stack

<!-- Keep these labels stable. Multiple skills read them verbatim. -->

- **Engine**: [CHOOSE: Godot 4 / Unity / Unreal Engine 5]
- **Language**: [CHOOSE: GDScript / C# / C++ / Blueprint]
- **Version Control**: Git with trunk-based development
- **Build System**: [SPECIFY after choosing engine]
- **Asset Pipeline**: [SPECIFY after choosing engine]

> Engine-specialist agents exist for Godot, Unity, and Unreal. Keep this section in sync with `docs/studio/technical-preferences.md`.

## Engine Version Reference

`docs/engine-reference/[TO BE CONFIGURED]/VERSION.md`

## Technical Preferences

`docs/studio/technical-preferences.md`

## Source-of-Truth Documents

- Engine and platform defaults: `docs/studio/technical-preferences.md`
- Workflow phases and routing: `docs/studio/workflow-catalog.yaml`
- Phase gates: `docs/studio/director-gates.md`
- Coordination rules: `docs/studio/coordination-rules.md`
- Coding standards: `docs/studio/coding-standards.md`
- Repo structure: `docs/studio/directory-structure.md`

## Coordination Rules

`docs/studio/coordination-rules.md`

## Coding Standards

`docs/studio/coding-standards.md`

## Repo Surfaces

- Root operating guidance lives here in `AGENTS.md`.
- Path-specific standards live in nested `AGENTS.md` files under `src/`, `design/`, `assets/`, `docs/`, `tests/`, and `prototypes/`.
- Reusable workflows live in `.agents/skills/`.
- Custom agent definitions live in `.codex/agents/`.
- Shared project hooks live in `.codex/hooks.json`.
- Shared project defaults live in `.codex/config.toml`.

## Working Agreements

- Prefer repo skills over ad-hoc prompting for recurring work.
- Keep design intent in `design/`, technical decisions in `docs/architecture/`, delivery state in `production/`, and implementation in `src/`.
- Surface tradeoffs when creative, technical, and production goals conflict.
- Use templates in `docs/studio/templates/` when creating first-class artifacts.
- Treat Steam release planning as part of the release phase, not as an external afterthought.

## Delegation Model

- Directors define direction and resolve cross-discipline conflicts.
- Leads own quality and coherence inside their domain.
- Specialists execute focused work and escalate when a task crosses boundaries.
- Use `$team-*` orchestration skills when the task genuinely spans multiple disciplines.

## Guardrails

- Validate shared changes with `python3 scripts/validate_codex_native.py`.
- After changing skill metadata, run `python3 scripts/sync_codex_metadata.py`.
- Do not weaken repo-local hooks, gates, or artifact contracts without updating the matching docs.
- Keep docs aligned with real paths, commands, and workflow names.

## Output Style

- Prefer concise, project-usable artifacts over abstract explanation.
- Make file destinations explicit when writing new docs or reports.
- When a workflow asks for approval before writing, stop at the draft boundary and ask clearly.
