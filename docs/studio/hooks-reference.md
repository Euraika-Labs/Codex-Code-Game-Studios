# Active Hooks

Current Codex releases support these hook events:

- `SessionStart`
- `PreToolUse`
- `PostToolUse`
- `UserPromptSubmit`
- `Stop`

This repository wires only the supported subset it actively uses in
`.codex/hooks.json`:

| Hook | Event | Trigger | Action |
| --- | --- | --- | --- |
| `session-start.sh` | `SessionStart` | every session start | loads git context, sprint context, and active session-state preview |
| `detect-gaps.sh` | `SessionStart` | every session start | detects fresh projects and missing documentation around real code/prototypes |
| `validate-commit.sh` | `PreToolUse` | Bash tool before `git commit` | validates design docs, data files, and common code hygiene issues |
| `validate-push.sh` | `PreToolUse` | Bash tool before `git push` | warns when pushing to protected branches |
| `validate-assets.sh` | `PostToolUse` | `Write` or `Edit` in `assets/` | checks naming conventions and JSON validity |
| `validate-skill-change.sh` | `PostToolUse` | `Write` or `Edit` in `.agents/skills/` | reminds maintainers to run `$skill-test` after skill edits |
| `session-stop.sh` | `Stop` | session end | appends a lightweight session summary to the audit trail |

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
