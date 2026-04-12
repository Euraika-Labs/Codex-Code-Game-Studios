# Hook Input Schemas

This documents the Codex hook payloads this repository actually relies on.

## PreToolUse

Fired before a tool is executed. In current Codex releases, `PreToolUse`
intercepts Bash commands only.

### Example: Bash

```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "git commit -m 'feat: add player health system'",
    "description": "Commit changes with message",
    "timeout": 120000
  }
}
```

## PostToolUse

Fired after a tool completes. In current Codex releases, `PostToolUse`
currently emits `tool_name = "Bash"` only.

### Example: Bash

```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "git status --short"
  },
  "tool_output": " M README.md"
}
```

This repo does not currently wire `PostToolUse`, because file edits made
through `apply_patch` are not exposed as `Write` or `Edit` hook payloads in
current Codex runtime.

## SessionStart

Fired when a Codex session begins.

### Example

```json
{
  "session_id": "sess_123",
  "cwd": "/workspace/game",
  "hook_event_name": "SessionStart",
  "source": "startup"
}
```

Plain text on stdout is added as extra developer context for this event.

## Stop

Fired when the current turn stops.

### Example

```json
{
  "session_id": "sess_123",
  "turn_id": "turn_456",
  "cwd": "/workspace/game",
  "hook_event_name": "Stop"
}
```

This repo uses `Stop` for worktree validation because it reliably fires after a
turn even when file writes happened through `apply_patch`.

## Exit Code Reference

| Exit code | Meaning | Applicable events |
| --- | --- | --- |
| `0` | allow or succeed | all supported events |
| `2` | block | `PreToolUse` |
| other | treated as hook error | all supported events |

## Notes

- `matcher` is only meaningful for `SessionStart`, `PreToolUse`, and
  `PostToolUse`.
- `Stop` and `UserPromptSubmit` ignore `matcher` today.
- Use `timeout` in `hooks.json`. `timeoutSec` is accepted as the camelCase
  alias; `timeout_sec` is not.
- Repo-local hook commands should resolve from the git root instead of relying
  on a relative `.codex/hooks/...` path.
- Hooks are currently disabled on native Windows in the official Codex docs.
