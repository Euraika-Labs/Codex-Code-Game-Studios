# Upgrading Codex Code Game Studios

This guide covers two upgrade paths:

1. migrating an older `Claude-Code-Game-Studios` project into the Codex-native
   structure
2. pulling newer updates into an existing `Codex-Code-Game-Studios` repo

---

## One-Time Migration From the Claude Version

Use this table as the source-of-truth mapping:

| Claude-oriented file/folder | Codex-native replacement |
| --- | --- |
| `CLAUDE.md` | `AGENTS.md` |
| `design/CLAUDE.md`, `src/CLAUDE.md`, `docs/CLAUDE.md` | nested `AGENTS.md` files in those directories |
| `.claude/skills/*/SKILL.md` | `.agents/skills/*/SKILL.md` |
| `.claude/agents/*.md` | `.codex/agents/*.toml` |
| `.claude/rules/*.md` | nested `AGENTS.md` files scoped to the matching directories |
| `.claude/hooks/*` | `.codex/hooks/*` and `.codex/hooks.json` |
| `.claude/docs/*` | `docs/studio/*` |
| `settings.local.json` overrides | `~/.codex/config.toml` and optional `~/.codex/hooks.json` |
| Claude-only prompt helpers like `AskUserQuestion` | direct Codex conversation flow inside repo skills |

### Recommended Migration Steps

1. Copy `AGENTS.md`, `.agents/`, `.codex/`, and `docs/studio/` into your
   project.
2. Rename any remaining `CLAUDE.md` files to `AGENTS.md`.
3. Move repo workflows from `.claude/skills/` into `.agents/skills/`.
4. Convert markdown agent definitions into `.codex/agents/*.toml`.
5. Replace path-scoped rule files with nested `AGENTS.md` files.
6. Keep only currently supported Codex hook events in `.codex/hooks.json`.
7. Re-read and update any project-specific docs that still mention
   `.claude/`, slash commands, or `settings.local.json`.

### Safe To Overwrite During Migration

These files are framework infrastructure and usually contain no game-specific
content:

```text
AGENTS.md
.agents/skills/
.codex/agents/
.codex/hooks/
.codex/hooks.json
docs/studio/
README.md
UPGRADING.md
```

### Merge Carefully

These often contain project-specific decisions and should be reviewed manually:

```text
.codex/config.toml
design/
docs/architecture/
production/
src/
tests/
nested AGENTS.md files you already customized
```

---

## Upgrading Between Codex Releases

If your project already uses the Codex-native layout, pull updates like any
other template-based repo:

```bash
git remote add template <codex-code-game-studios-remote>
git fetch template
git merge template/main
```

If you only need specific workflows or docs:

```bash
git fetch template
git cherry-pick <commit-sha>
```

---

## Upgrade Checklist

After pulling an update, verify these items:

1. `AGENTS.md` still reflects your project-specific rules.
2. `.agents/skills/` only contains the workflows you want to keep customized.
3. `.codex/agents/` still matches your preferred model and reasoning defaults.
4. `.codex/hooks.json` only wires supported Codex hook events.
5. `.codex/config.toml` does not accidentally override personal preferences you
   meant to keep in `~/.codex/config.toml`.
6. No docs still reference `.claude/`, `CLAUDE.md`, slash commands, or
   `settings.local.json`.

---

## Personal Overrides

Do not re-introduce project-local `settings.local.json`.

Use these Codex-native override points instead:

- `~/.codex/config.toml` for user-specific defaults and profiles
- `~/.codex/hooks.json` for personal hooks
- project `.codex/config.toml` for shared repo defaults
- project `.codex/hooks.json` for shared repo hooks

---

## If You Hit Drift

The fastest way to recover from a half-migrated state is:

1. restore `AGENTS.md`
2. restore `.agents/skills/`
3. restore `.codex/agents/`
4. restore `.codex/hooks.json`
5. re-run a grep for old Claude-only surfaces:

```bash
rg -n --hidden '\.claude|CLAUDE\.md|settings\.local\.json|AskUserQuestion|slash command'
```
