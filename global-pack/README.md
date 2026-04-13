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

## Install the Global Pack

From the root of this repository:

```bash
python3 global-pack/bin/install_global_pack.py
```

By default this installs into `~/.codex`. Override with `--codex-home` if you
want a test or sandbox install.

## Bootstrap an Existing Repository

After the global pack is installed, either ask Codex to use `$install-studio`
from inside a target repository, or run:

```bash
python3 ~/.codex/bin/install_repo_studio.py --target /path/to/repo
```

Add `--dry-run` to preview changes and `--force` only if you want to overwrite
conflicting files.
