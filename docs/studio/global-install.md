# Global Installation

Codex Code Game Studios uses a hybrid installation model:

- a small global pack in your Codex home for discovery and installation helpers
- the full studio installed into each target repository

This keeps global state small while preserving the repo-local context that the full workflows need.

## Recommended Path: Universal Bootstrap

Run the bootstrap from the framework repo or from an installed global Codex home.

### macOS, Linux, and WSL

```bash
./bootstrap.sh
```

### Windows PowerShell

```powershell
.ootstrap.ps1
```

### Direct Python fallback

```bash
python3 global-pack/bin/bootstrap.py
```

## What the Bootstrap Does

The bootstrap will:

1. resolve the correct Codex home for the current platform
2. install or refresh the global pack there
3. if you are inside a git repo, install the full studio into that repo

## Platform Resolution Rules

The Codex home resolution order is:

1. `CODEX_HOME` if already set
2. native Windows: `%USERPROFILE%\.codex`
3. WSL: shared Windows Codex home if it already exists, otherwise Linux `~/.codex`
4. Linux and macOS: `~/.codex`

This matches the Codex split between Windows and WSL while preferring a shared setup when that is already present.

## What Gets Installed Globally

The global pack installs:

- `~/.codex/skills/studio-help`
- `~/.codex/skills/install-studio`
- `~/.codex/skills/adopt-studio`
- `~/.codex/agents/studio-bootstrapper.toml`
- `~/.codex/bin/bootstrap.py`
- `~/.codex/bin/install_repo_studio.py`
- `~/.codex/bin/install_global_pack.py`

## What Gets Installed Into a Repo

When the bootstrap targets a git repository, it installs the full studio layer there:

- `AGENTS.md`
- `.agents/`
- `.codex/`
- `docs/studio/`
- nested `AGENTS.md` path guides
- starter directories such as `design/`, `production/`, `src/`, `tests/`, and `build/`

## Useful Flags

```bash
python3 global-pack/bin/bootstrap.py --dry-run
python3 global-pack/bin/bootstrap.py --global-only
python3 global-pack/bin/bootstrap.py --repo-only
python3 global-pack/bin/bootstrap.py --target /path/to/repo
python3 global-pack/bin/bootstrap.py --codex-home /tmp/codex-home
python3 global-pack/bin/bootstrap.py --force
```

Use `--force` when you intentionally want to refresh already-installed files.

## Typical Scenarios

### Install the global helpers only

```bash
./bootstrap.sh --global-only
```

### Install the studio into an existing game repo

```bash
./bootstrap.sh --target /path/to/existing-game-repo
```

### Refresh both global and local installation from the framework repo

```bash
./bootstrap.sh --force
```

## After Installation

If the target repo is new to the framework, start with:

- `$project-stage-detect`
- `$adopt`
- `$help`

If the target repo is new game work, start with:

- `$start`
- `$brainstorm`

## Validation

Validate the installer layer with:

```bash
python3 scripts/validate_codex_native.py
python3 scripts/test_hybrid_global_install.py
```
