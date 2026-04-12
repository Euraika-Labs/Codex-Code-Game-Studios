# Local Overrides

Project-local `CLAUDE.local.md` style overrides are not part of the Codex
layout for this repo.

Use the supported Codex layers instead:

- shared repo guidance in `AGENTS.md`
- shared repo config in `.codex/config.toml`
- shared repo hooks in `.codex/hooks.json`
- personal config in `~/.codex/config.toml`
- personal hooks in `~/.codex/hooks.json`

If you need a personal profile for this repo, prefer a user-level profile:

```toml
[profiles.game-studio]
model = "gpt-5.4"
model_reasoning_effort = "high"
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[projects."/absolute/path/to/Codex-Code-Game-Studios"]
trust_level = "trusted"
```

Then launch the project with:

```bash
codex -p game-studio
```
