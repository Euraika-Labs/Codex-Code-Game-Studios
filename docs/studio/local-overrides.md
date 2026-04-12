# Local Overrides

Project-local `CLAUDE.local.md` style overrides are not part of the Codex
layout for this repo.

Use the supported Codex layers instead:

- shared repo guidance in `AGENTS.md`
- shared repo config in `.codex/config.toml`
- shared repo hooks in `.codex/hooks.json`
- personal config in `~/.codex/config.toml`
- personal hooks in `~/.codex/hooks.json`

If you want private hooks to run outside this repo too, enable them in your
user config:

```toml
[features]
codex_hooks = true
```

If you need a personal profile for this repo, prefer a user-level profile:

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

Then launch the project with:

```bash
codex -p game-studio
```

Use this layer for personal-only Codex ergonomics:

- disable repo skills you do not want implicitly available with `[[skills.config]]`
- lower or raise `[agents].max_threads` for your machine and plan limits
- set `tui.alternate_screen = "never"` if you prefer preserved scrollback
