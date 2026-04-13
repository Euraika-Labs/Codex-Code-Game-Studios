# Global Pack

This directory contains the user-level distribution for Codex Code Game
Studios.

It is intentionally smaller than the full project template:

- `skills/` contains self-contained global skills for discovery, installation,
  and repo bootstrap.
- `agents/` contains global helper agents that are safe to load from
  `~/.codex/agents`.
- `bin/` contains the supported installers.
- `manifest.json` defines exactly what gets installed globally and what gets
  copied into a target repository.

## Universal Bootstrap

From the root of this repository:

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

This command automatically:

- picks the correct Codex home for your platform
- installs or refreshes the global pack there
- bootstraps the current git repo if you are inside one

Use `--global-only` if you want only the user-level install.

## Bootstrap an Existing Repository

After the global pack is installed, either ask Codex to use `$install-studio`
from inside a target repository, or run:

```bash
python3 ~/.codex/bin/bootstrap.py --target /path/to/repo
```

Add `--dry-run` to preview changes and `--force` only if you want to overwrite
conflicting files.
