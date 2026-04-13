# Upgrading Codex Code Game Studios

This guide covers the two supported upgrade paths for the framework:

1. updating an existing `Codex-Code-Game-Studios` repo to a newer release
2. adopting the framework into an existing game repository that did not start from this repo

## Upgrade Strategy

Treat the framework as shared studio infrastructure.

- overwrite the framework layer freely when it has not been customized
- merge carefully where your project added its own rules, templates, or conventions
- keep game-specific content separate from framework content whenever possible

## Path 1: Update an Existing Framework Repo

If your project already uses the full layout, update it like a normal upstream template:

```bash
git remote add template <codex-code-game-studios-remote>
git fetch template
git merge template/main
```

If you only want selected updates:

```bash
git fetch template
git cherry-pick <commit-sha>
```

### Usually safe to overwrite

```text
AGENTS.md
.agents/skills/
.codex/agents/
.codex/hooks/
.codex/hooks.json
docs/studio/
docs/examples/
docs/engine-reference/
global-pack/
README.md
UPGRADING.md
```

### Merge carefully

```text
.codex/config.toml
design/
docs/architecture/
production/
src/
tests/
nested AGENTS.md files you customized for your game
```

## Path 2: Adopt the Framework Into an Existing Game Repo

If you already have code, docs, or production assets, use the hybrid installer and brownfield workflow.

### Step 1: Install the studio layer

Run the universal bootstrap inside the target repo:

```bash
python3 ~/.codex/bin/bootstrap.py --target /path/to/game-repo
```

Or, from the framework repo on macOS, Linux, or WSL:

```bash
./bootstrap.sh --target /path/to/game-repo
```

### Step 2: Audit the project state

Inside the target repo, run:

- `$project-stage-detect`
- `$adopt`
- `$help`

`project-stage-detect` identifies what exists. `adopt` checks whether those artifacts are usable by the studio workflows. `help` tells you what to do next.

### Step 3: Merge the framework with your existing project conventions

Review these shared surfaces first:

- `AGENTS.md`
- `.codex/config.toml`
- nested `AGENTS.md` files
- `docs/studio/technical-preferences.md`
- release and testing templates you plan to keep

## Upgrade Checklist

After any framework update, verify:

1. `AGENTS.md` still reflects the current project reality.
2. `.agents/skills/` matches the workflows you actually want to keep customized.
3. `.codex/agents/` still uses the desired models, nicknames, and sandbox settings.
4. `.codex/hooks.json` still points only at supported hook events and valid repo scripts.
5. `.codex/config.toml` still separates personal preferences from shared project defaults.
6. docs, templates, and examples still point at the correct file paths for your repo.

## Personal Overrides

Keep personal setup outside the shared repo layer:

- `~/.codex/config.toml` for user defaults and profiles
- `~/.codex/hooks.json` for user hooks
- `~/.codex/skills/` and `~/.codex/agents/` for personal global capabilities

Keep the project `.codex/` layer reserved for shared team behavior.

## If the Repo Drifts

The fastest recovery path is:

1. restore `AGENTS.md`
2. restore `.agents/skills/`
3. restore `.codex/agents/`
4. restore `.codex/hooks.json`
5. re-run the bootstrap if global installation drifted
6. run the validation suite

```bash
python3 scripts/validate_codex_native.py
python3 scripts/test_hybrid_global_install.py
```
