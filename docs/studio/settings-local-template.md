# Codex Configuration Notes

The old `settings.local.json` pattern is not used in this repo.

Use Codex's layered configuration instead:

- shared project defaults live in `.codex/config.toml`
- shared project hooks live in `.codex/hooks.json`
- personal defaults live in `~/.codex/config.toml`
- personal hooks live in `~/.codex/hooks.json`

## Example Personal Config

```toml
[profiles.game-studio]
model = "gpt-5.4"
model_reasoning_effort = "high"
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[agents]
max_threads = 4
max_depth = 1

[tui]
alternate_screen = "never"

[tools.web_search]
context_size = "medium"

[projects."/absolute/path/to/Codex-Code-Game-Studios"]
trust_level = "trusted"

[[skills.config]]
name = "team-ui"
enabled = false
```

Run the project with that profile using:

```bash
codex -p game-studio
```

## What Belongs Where

Use project `.codex/config.toml` for settings the whole team should share:

- default model or reasoning level for the studio
- default sandbox and approval posture for this repo
- feature flags required by the framework

Use user `~/.codex/config.toml` for settings only you should control:

- trust declarations for local paths
- personal profiles
- local model-provider choices
- personal approval preferences
- personal skill enables/disables via `[[skills.config]]`
- terminal UI preferences such as `tui.alternate_screen`
- personal subagent tuning such as `[agents].max_threads`

Use project `.codex/hooks.json` for hooks that should run for everyone in the
repo. Use user `~/.codex/hooks.json` for private notifications or local-only
automation.

Notes:

- `skills.config` is user-level on purpose. Use it when a repo ships useful
  skills that you do not want implicitly active in your personal workflow.
- `tui.alternate_screen = "never"` is helpful in Zellij or other multiplexers
  where you want reliable scrollback.
