# Local Overrides

Personal preferences belong in your Codex home, not in the shared project files.

## Use These for Personal Setup

- `~/.codex/config.toml`
- `~/.codex/hooks.json`
- `~/.codex/skills/`
- `~/.codex/agents/`

## Keep These Shared

- project `.codex/config.toml`
- project `.codex/hooks.json`
- repo skills and agents
- shared docs and templates

## Good Override Examples

- personal model or profile preferences
- local helper hooks that only you need
- personal skill packs unrelated to the shared repo contract

## Bad Override Examples

- hiding shared project defaults in your personal config and assuming the team sees them
- replacing shared hook behavior with undocumented local behavior
- treating local overrides as the source of truth for project process
