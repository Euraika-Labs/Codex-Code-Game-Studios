---
name: adopt-studio
description: Global read-only audit skill that checks whether a repository is ready for Codex Code Game Studios and routes to installation or the repo-local adopt flow.
---

# Adopt Studio

This skill is a global preflight check. Use it when the user wants to know if an
existing repository is ready for the studio layer.

## What To Check

1. Resolve the repo root with `git rev-parse --show-toplevel`, or fall back to
   the current working directory
2. Check for:
   - `AGENTS.md`
   - `.agents/skills/`
   - `.codex/agents/`
   - `docs/studio/`
3. If those exist, note that the repo can now use the project-local `$adopt`
   skill for a deeper brownfield audit

## What To Say

- If the studio layer is missing:
  - say the repo is not studio-enabled yet
  - recommend `$install-studio`
- If the studio layer is present:
  - say the repo is ready for a deeper brownfield audit
  - recommend the repo-local `$adopt`

## Guardrails

- Read-only only
- Do not run the repo-local `$adopt` automatically
- Do not claim the repo is fully compatible unless the studio layer is present
