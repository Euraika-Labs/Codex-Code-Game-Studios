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

[projects."/absolute/path/to/Codex-Code-Game-Studios"]
trust_level = "trusted"
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

Use project `.codex/hooks.json` for hooks that should run for everyone in the
repo. Use user `~/.codex/hooks.json` for private notifications or local-only
automation.
