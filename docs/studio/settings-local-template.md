# Local Codex Config Template

Use this document as a starting point when creating your own `~/.codex/config.toml`.
It is a personal reference, not a shared repo file.

## Suggested Pattern

```toml
model = "gpt-5.4"
reasoning_effort = "medium"
web_search = "live"

[profiles.fast]
model = "gpt-5.4-mini"
reasoning_effort = "low"

[profiles.deep]
model = "gpt-5.4"
reasoning_effort = "high"
```

## Use Personal Config For

- default model choice
- personal profiles
- local tool preferences
- user-specific integrations and experiments

Keep project behavior in the repo-local `.codex/` files instead.
