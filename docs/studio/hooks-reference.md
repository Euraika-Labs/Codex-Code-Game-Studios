# Active Hooks

Current Codex releases support these hook events:

- `SessionStart`
- `PreToolUse`
- `PostToolUse`
- `UserPromptSubmit`
- `Stop`

This repository enables hooks in `.codex/config.toml` with:

```toml
[features]
codex_hooks = true
```

It wires the actively used subset in `.codex/hooks.json`:

| Hook | Event | Trigger | Action |
| --- | --- | --- | --- |
| `session-start.sh` | `SessionStart` | every session start | loads git context, sprint context, and active session-state preview |
| `detect-gaps.sh` | `SessionStart` | every session start | detects fresh projects and missing documentation around real code/prototypes |
| `validate-commit.sh` | `PreToolUse` | Bash tool before `git commit` | blocks commits when Codex-native repo contracts or staged JSON files are invalid |
| `validate-push.sh` | `PreToolUse` | Bash tool before `git push` | warns when pushing to protected branches |
| `validate-assets.sh` | `Stop` | every turn stop | reviews changed `assets/` files and warns about invalid JSON or naming drift |
| `validate-skill-change.sh` | `Stop` | every turn stop | runs `scripts/validate_codex_native.py` when skills, agents, config, or hooks change |
| `session-stop.sh` | `Stop` | every turn stop | appends a lightweight per-turn audit entry to the audit trail |

## Important Runtime Notes

- Repo-local hook commands are resolved from the git root, not from a relative
  `.codex/hooks/...` path. This keeps them stable when Codex starts in a
  subdirectory.
- Current Codex runtime only emits `Bash` for `PreToolUse` and `PostToolUse`.
  That means `Edit|Write` matcher patterns are valid regex but runtime no-ops
  today.
- Because of that runtime limitation, this repo does file-oriented validation at
  `Stop` time and at `git commit` time instead of pretending file writes are
  intercepted live.
- Hooks are currently disabled on native Windows in the official Codex docs.
  Use macOS, Linux, or WSL if you rely on these repo hooks.

## Compatibility Scripts Kept In Repo

The following scripts are still present under `.codex/hooks/` as reference or
future-compatibility helpers, but they are **not** wired because their event
types are not part of the currently supported Codex hook surface:

- `pre-compact.sh`
- `post-compact.sh`
- `notify.sh`
- `log-agent.sh`
- `log-agent-stop.sh`

Hook input schema notes live in `docs/studio/hooks-reference/hook-input-schemas.md`.
