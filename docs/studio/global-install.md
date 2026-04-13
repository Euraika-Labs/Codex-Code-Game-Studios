# Global Install Guide

This guide explains the supported hybrid setup for making Codex Code Game
Studios available everywhere without forcing the whole repo into `~/.codex`.

## The Supported Model

There are two layers:

1. **Global layer in `~/.codex`**
   - small helper skills
   - small helper agent set
   - installer scripts
2. **Project layer inside a repo**
   - `AGENTS.md`
   - `.agents/skills`
   - `.codex/agents`, hooks, config
   - `docs/studio`
   - nested path-specific `AGENTS.md` guides

This split matters because most game workflows depend on repo-local templates,
docs, and directories.

## Step 1: Clone the Source Repo Normally

Keep this repository somewhere ordinary:

```bash
git clone https://github.com/Euraika-Labs/Codex-Code-Game-Studios.git ~/tooling/Codex-Code-Game-Studios
cd ~/tooling/Codex-Code-Game-Studios
```

Do not clone the entire repo into `~/.codex`.

## Step 2: Install the Global Pack

```bash
python3 global-pack/bin/install_global_pack.py
```

Optional flags:

- `--dry-run` to preview file actions
- `--force` to overwrite conflicting installed files
- `--codex-home` to install into a non-default Codex home
- `--source-repo` to point at a specific source clone

After a successful install, these should exist:

- `~/.codex/skills/studio-help/`
- `~/.codex/skills/install-studio/`
- `~/.codex/skills/adopt-studio/`
- `~/.codex/agents/studio-bootstrapper.toml`
- `~/.codex/bin/install_repo_studio.py`
- `~/.codex/bin/install_global_pack.py`

## Step 3: Bootstrap a Target Repository

Inside any target repo:

```bash
python3 ~/.codex/bin/install_repo_studio.py --target /path/to/repo
```

If the repo already has related files:

```bash
python3 ~/.codex/bin/install_repo_studio.py --target /path/to/repo --dry-run
```

Only use `--force` when you have explicitly decided to overwrite conflicting
files.

## Step 4: Use the Repo-Local Studio

Once installed, open Codex in the target repo and use the normal project skills:

- `$start`
- `$help`
- `$project-stage-detect`
- `$adopt`
- the rest of the game, QA, release, and Steam workflows

## What Gets Copied Into a Repo

The first installer version copies:

- root `AGENTS.md`
- `.agents/`
- `.codex/`
- `docs/studio/`
- `docs/AGENTS.md`
- `docs/WORKFLOW-GUIDE.md`
- nested `AGENTS.md` guides for design, source, tests, assets, docs, and prototypes
- starter directory structure for design, production, code, tests, assets, docs,
  build, and Steam release tracking

It intentionally does **not** generate project-specific design or production
documents. Those should be created by the repo skills after installation.

## Recommended Everyday Flow

1. Keep one checked-out copy of this repo as your source of truth
2. Run `install_global_pack.py` whenever you update it
3. Use `$install-studio` or `install_repo_studio.py` inside any new or existing repo
4. Switch back to the repo-local workflows after bootstrap
