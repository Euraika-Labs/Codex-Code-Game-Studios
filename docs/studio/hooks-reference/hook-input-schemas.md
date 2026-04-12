# Hook Input Schemas

This documents the Codex hook payloads this repository actually relies on.

## PreToolUse

Fired before a tool is executed. `PreToolUse` hooks can allow execution with
exit code `0` or block execution with exit code `2`.

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

### Example: Write

```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "src/gameplay/health.gd",
    "content": "extends Node\n..."
  }
}
```

### Example: Edit

```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "src/gameplay/health.gd",
    "old_string": "var health = 100",
    "new_string": "var health: int = 100"
  }
}
```

## PostToolUse

Fired after a tool completes. These hooks are advisory in this repo.

### Example: Write

```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "assets/data/enemy_stats.json",
    "content": "{\"goblin\": {\"health\": 50}}"
  },
  "tool_output": "File written successfully"
}
```

### Example: Edit

```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "assets/data/enemy_stats.json",
    "old_string": "\"health\": 50",
    "new_string": "\"health\": 75"
  },
  "tool_output": "File edited successfully"
}
```

## SessionStart

Fired when a Codex session begins. No stdin payload is required; stdout is
shown back to Codex as extra context.

## Stop

Fired when the Codex session ends. No stdin payload is required; use it for
logging or cleanup.

## Exit Code Reference

| Exit code | Meaning | Applicable events |
| --- | --- | --- |
| `0` | allow or succeed | all supported events |
| `2` | block | `PreToolUse` |
| other | treated as hook error | all supported events |

## Notes

- Hooks receive JSON on stdin when the event carries tool data.
- `jq` is optional; grep-based fallbacks keep the scripts Windows Git Bash
  friendly.
- Normalize Windows paths with `sed 's|\\|/|g'` before comparing them.
- This repo intentionally does not document unsupported legacy events such as
  `PreCompact`, `PostCompact`, notification hooks, or subagent lifecycle hooks
  as part of the active Codex hook contract.
