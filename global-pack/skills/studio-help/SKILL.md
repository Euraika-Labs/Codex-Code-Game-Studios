---
name: studio-help
description: Global helper for explaining how the Codex Code Game Studios pack works, whether the current repo is already studio-enabled, and which installer flow to use next.
---

# Studio Help

Use this skill anywhere. It is safe in `~/.codex/skills` because it only reads
the current repository state and explains the next action.

## What To Check

1. Try to identify the current project root:
   - Prefer `git rev-parse --show-toplevel`
   - If git is unavailable, use the current working directory
2. Check whether the repository already contains:
   - `AGENTS.md`
   - `.agents/skills/`
   - `.codex/agents/`
   - `docs/studio/`

## What To Say

- If the repo is already studio-enabled:
  - say that the full project-local studio is available
  - recommend repo-local skills like `$start`, `$help`, or `$project-stage-detect`
- If the repo is missing the studio layer:
  - explain that the global pack is installed correctly, but the heavy game
    workflows still need to be bootstrapped into this repository
  - recommend `$install-studio` or `python3 ~/.codex/bin/bootstrap.py --target "<repo-root>"`
- If the user asks how the hybrid model works:
  - explain that global skills and agents live in `~/.codex`
  - explain that project workflows live in the repo after installation

## Guardrails

- Do not write files in this skill
- Do not pretend the whole studio runs globally without project install
- If the user wants setup to happen now, route them to `$install-studio`
