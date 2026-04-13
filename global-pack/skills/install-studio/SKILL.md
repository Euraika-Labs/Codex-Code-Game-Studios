---
name: install-studio
description: Global installer skill that bootstraps the full Codex Code Game Studios layer into the current repository by calling the installed repo bootstrap script.
---

# Install Studio

This skill is designed to live in `~/.codex/skills/install-studio`. It should
prefer the universal bootstrap at `../../bin/bootstrap.py`, which resolves the
best Codex home and installs the repo-local studio safely.

## Step 1: Resolve the Target Repository

1. Prefer `git rev-parse --show-toplevel`
2. If that fails, use the current working directory and tell the user you are
   treating it as the target project root

## Step 2: Inspect Existing Studio State

Check whether any of these already exist:

- `AGENTS.md`
- `.agents/skills/`
- `.codex/agents/`
- `docs/studio/`

## Step 3: Choose the Safe Installer Command

Default to a preview first when the repository already has any of those paths:

```bash
python3 ~/.codex/bin/bootstrap.py --target "<repo-root>" --dry-run
```

If the repo looks fresh, you may run the install directly:

```bash
python3 ~/.codex/bin/bootstrap.py --target "<repo-root>"
```

## Step 4: Handle Conflicts Carefully

- If the script reports conflicts, summarize them for the user
- Only suggest `--force` if the user explicitly wants to overwrite the
  conflicting files
- Never assume it is safe to replace an existing `.codex` or `AGENTS.md`

## Step 5: After a Successful Install

Tell the user:

- the studio layer is now installed in the target repo
- they can use repo-local workflows like `$start`, `$help`, `$project-stage-detect`,
  and `$adopt`

## Guardrails

- Do not fabricate project design docs as part of installation
- Do not overwrite conflicting files without explicit user approval
- Keep the installation scoped to the repository the user is currently working in
