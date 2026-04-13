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

## Step 2: Run the Universal Bootstrap

On macOS, Linux, and WSL:

```bash
./bootstrap.sh
```

On Windows PowerShell:

```powershell
.\bootstrap.ps1
```

Fallback:

```bash
python3 global-pack/bin/bootstrap.py
```

Optional flags:

- `--dry-run` to preview file actions
- `--force` to overwrite conflicting installed files
- `--global-only` to install just the global pack
- `--repo-only` to bootstrap only a repo
- `--codex-home` to install into a non-default Codex home
- `--source-repo` to point at a specific source clone
- `--target` to bootstrap a specific repo instead of the current git root

The universal bootstrap automatically:

- resolves the best Codex home for the current platform
- installs or refreshes the global pack
- bootstraps the current git repo if one is detected

### Platform defaults

- `CODEX_HOME` wins if already set
- native Windows uses `%USERPROFILE%\.codex`
- WSL prefers the Windows Codex home if it already exists
- otherwise WSL uses Linux `~/.codex`
- Linux and macOS use `~/.codex`

After a successful install, these should exist:

- `~/.codex/skills/studio-help/`
- `~/.codex/skills/install-studio/`
- `~/.codex/skills/adopt-studio/`
- `~/.codex/agents/studio-bootstrapper.toml`
- `~/.codex/bin/bootstrap.py`
- `~/.codex/bin/install_repo_studio.py`
- `~/.codex/bin/install_global_pack.py`

## Step 3: Bootstrap a Target Repository

If you ran the universal bootstrap inside a git repo, this already happened
automatically.

If you want to target a specific repo manually:

```bash
python3 global-pack/bin/bootstrap.py --target /path/to/repo
```

If the repo already has related files:

```bash
python3 global-pack/bin/bootstrap.py --target /path/to/repo --dry-run
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
2. Run `./bootstrap.sh` or `.\bootstrap.ps1` whenever you update it
3. Use `$install-studio` or `bootstrap.py --target ...` inside any new or existing repo
4. Switch back to the repo-local workflows after bootstrap
