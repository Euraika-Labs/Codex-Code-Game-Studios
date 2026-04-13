# Hybrid Global Installer Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a hybrid global distribution layer that installs a curated Codex home pack and bootstraps the full studio into any target repository.

**Architecture:** The implementation adds a repo-managed `global-pack/` source tree plus two Python installers: one for syncing global assets into `~/.codex`, and one for installing repo-local studio assets into a target repository. Validation and docs will treat the global pack as a first-class supported surface.

**Tech Stack:** Python 3, Markdown, YAML frontmatter, TOML, existing Codex repo validation scripts

---

### Task 1: Add the global-pack source tree

**Files:**
- Create: `global-pack/README.md`
- Create: `global-pack/skills/studio-help/SKILL.md`
- Create: `global-pack/skills/studio-help/agents/openai.yaml`
- Create: `global-pack/skills/install-studio/SKILL.md`
- Create: `global-pack/skills/install-studio/agents/openai.yaml`
- Create: `global-pack/skills/adopt-studio/SKILL.md`
- Create: `global-pack/skills/adopt-studio/agents/openai.yaml`
- Create: `global-pack/agents/studio-bootstrapper.toml`

**Step 1: Write the source assets**

Add self-contained global skills and one global helper agent that do not depend
on repo-local templates.

**Step 2: Verify the assets look like valid Codex files**

Run: `python3 - <<'PY'\nfrom pathlib import Path\nfor path in Path('global-pack').rglob('*'):\n    print(path)\nPY`

Expected: the new global-pack files exist at the intended paths.

**Step 3: Commit**

```bash
git add global-pack
git commit -m "feat: add global Codex pack sources"
```

### Task 2: Add installers for global sync and repo bootstrap

**Files:**
- Create: `global-pack/bin/install_global_pack.py`
- Create: `global-pack/bin/install_repo_studio.py`

**Step 1: Write the installers**

Implement:

- a global sync command that copies curated assets into `~/.codex/skills` and
  `~/.codex/agents`
- a repo installer that copies `AGENTS.md`, `.agents`, `.codex`,
  `docs/studio`, and starter folders into a target repo
- support for `--dry-run`
- idempotent directory creation and file copy

**Step 2: Smoke-test the CLI help**

Run:

```bash
python3 global-pack/bin/install_global_pack.py --help
python3 global-pack/bin/install_repo_studio.py --help
```

Expected: both scripts print usable help and exit successfully.

**Step 3: Commit**

```bash
git add global-pack/bin
git commit -m "feat: add global and repo studio installers"
```

### Task 3: Wire validation into the existing repo contracts

**Files:**
- Modify: `scripts/validate_codex_native.py`

**Step 1: Extend validation**

Add checks for:

- required `global-pack/` files
- global skill frontmatter and `openai.yaml`
- global agent TOML parsing
- installer script presence

**Step 2: Run the validator**

Run: `python3 scripts/validate_codex_native.py`

Expected: PASS, including the new global pack checks.

**Step 3: Commit**

```bash
git add scripts/validate_codex_native.py
git commit -m "test: validate hybrid global pack contracts"
```

### Task 4: Add install documentation

**Files:**
- Modify: `README.md`
- Create: `docs/studio/global-install.md`

**Step 1: Document the new flows**

Document:

- what goes into `~/.codex`
- what stays repo-local
- how to sync the global pack
- how to bootstrap an existing repo
- expected resulting directory layouts

**Step 2: Spot-check the docs**

Run: `rg -n "global-pack|~/.codex|install_repo_studio|install_global_pack" README.md docs/studio/global-install.md`

Expected: the docs cover both user-level and repo-level installation.

**Step 3: Commit**

```bash
git add README.md docs/studio/global-install.md
git commit -m "docs: explain hybrid global studio installation"
```

### Task 5: Validate with throwaway installs

**Files:**
- Create: `scripts/test_hybrid_global_install.py`

**Step 1: Add the end-to-end test harness**

The test should:

- create a temporary fake Codex home
- run `install_global_pack.py` into it
- assert that global skills and agents were installed
- create a temporary git repo
- run `install_repo_studio.py` into it
- assert that required studio files were installed

**Step 2: Run the install test**

Run: `python3 scripts/test_hybrid_global_install.py`

Expected: PASS with both the global install and repo bootstrap assertions.

**Step 3: Run the full validation set**

Run:

```bash
python3 scripts/validate_codex_native.py
python3 scripts/test_hybrid_global_install.py
```

Expected: both commands pass.

**Step 4: Commit**

```bash
git add scripts/test_hybrid_global_install.py
git commit -m "test: verify hybrid global installer end to end"
```
