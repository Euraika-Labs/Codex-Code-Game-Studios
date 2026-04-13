# Universal Bootstrap Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add one universal bootstrap entrypoint that installs the global pack
and, when applicable, bootstraps the full studio into the current repository
with automatic cross-platform Codex-home detection.

**Architecture:** Extend the existing installer library with platform-aware
Codex-home resolution and auto-detection helpers, then add a new bootstrap
script and thin shell wrappers. Validation will cover explicit overrides,
Windows, WSL, Linux, and repo auto-detection behavior.

**Tech Stack:** Python 3, shell wrappers, PowerShell wrapper, Markdown docs,
existing repo validation scripts

---

### Task 1: Extend installer helpers for platform-aware resolution

**Files:**
- Modify: `global-pack/bin/_installer_lib.py`

**Step 1: Add environment and platform helpers**

Implement helpers for:

- detecting WSL
- detecting native Windows
- deriving the Windows user profile path from WSL
- resolving the preferred Codex home automatically
- detecting the git root for the current working directory

**Step 2: Keep existing behavior stable**

Preserve the current explicit `--codex-home` and `--source-repo` overrides.

**Step 3: Smoke-check imports**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
import sys
sys.path.insert(0, str(Path('global-pack/bin').resolve()))
import _installer_lib
print('ok')
PY
```

Expected: prints `ok`.

### Task 2: Add the universal bootstrap entrypoint

**Files:**
- Create: `global-pack/bin/bootstrap.py`

**Step 1: Implement the smart default flow**

The script should:

- resolve the source repo
- resolve the best Codex home
- install the global pack
- auto-detect the current repo root, if any
- install the repo-local studio when not in `--global-only` mode
- print a concise summary

**Step 2: Add bootstrap flags**

Support:

- `--dry-run`
- `--force`
- `--global-only`
- `--repo-only`
- `--codex-home`
- `--source-repo`
- `--target`

**Step 3: Check the CLI help**

Run: `python3 global-pack/bin/bootstrap.py --help`

Expected: help shows the smart bootstrap flags and purpose.

### Task 3: Add platform wrappers

**Files:**
- Create: `bootstrap.sh`
- Create: `bootstrap.ps1`

**Step 1: Add thin wrappers**

Make the wrappers call the Python bootstrap script with forwarded arguments.

**Step 2: Verify wrapper readability**

Run:

```bash
bash -n bootstrap.sh
```

Expected: no syntax errors.

### Task 4: Update validation and end-to-end tests

**Files:**
- Modify: `scripts/validate_codex_native.py`
- Modify: `scripts/test_hybrid_global_install.py`

**Step 1: Validate the new bootstrap surface**

Add checks for:

- `global-pack/bin/bootstrap.py`
- `bootstrap.sh`
- `bootstrap.ps1`

**Step 2: Expand the install test**

Add coverage for:

- explicit `CODEX_HOME`
- auto-detected repo root
- non-repo global-only bootstrap
- WSL-aware path selection logic through deterministic environment simulation

**Step 3: Run the tests**

Run:

```bash
python3 scripts/validate_codex_native.py
python3 scripts/test_hybrid_global_install.py
```

Expected: both pass.

### Task 5: Update docs

**Files:**
- Modify: `README.md`
- Modify: `docs/studio/global-install.md`
- Modify: `global-pack/README.md`

**Step 1: Document the one-command flow**

Explain:

- the universal bootstrap command
- how it behaves inside vs outside a repo
- what happens on Windows, WSL, Linux, and macOS
- when users should still use manual flags

**Step 2: Spot-check docs**

Run:

```bash
rg -n "bootstrap.py|bootstrap.sh|bootstrap.ps1|WSL|CODEX_HOME" README.md docs/studio/global-install.md global-pack/README.md
```

Expected: docs cover the new universal bootstrap path clearly.

### Task 6: Final validation and commit

**Files:**
- No new files; use the changed set above

**Step 1: Run the final validation bundle**

Run:

```bash
python3 scripts/validate_codex_native.py
python3 scripts/test_hybrid_global_install.py
python3 global-pack/bin/bootstrap.py --dry-run
```

Expected: all pass.

**Step 2: Commit**

```bash
git add docs/plans/2026-04-13-universal-bootstrap-design.md \
        docs/plans/2026-04-13-universal-bootstrap-implementation.md \
        global-pack/bin/_installer_lib.py \
        global-pack/bin/bootstrap.py \
        bootstrap.sh bootstrap.ps1 \
        scripts/validate_codex_native.py \
        scripts/test_hybrid_global_install.py \
        README.md docs/studio/global-install.md global-pack/README.md
git commit -m "feat: add universal bootstrap flow"
```
