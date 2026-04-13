---
name: steam-soundtrack
description: Create a Steam soundtrack release plan covering soundtrack app setup, rights checks, album assets, pricing, and bundle coordination. Use when releasing a soundtrack on Steam.
---

> **Explicit invocation only**: Run this skill only when the user explicitly asks for `$steam-soundtrack`.

# Steam Soundtrack

## Phase 1: Load Context

Read:
- `production/releases/steam/steam-publish-plan.md`
- `docs/studio/templates/steam-soundtrack-template.md`

## Phase 2: Generate the Soundtrack Plan

Cover:
- soundtrack app shape
- relation to the base game
- rights and asset readiness
- pricing and release timing
- bundle inclusion and launch sequencing

Use `docs/studio/templates/steam-soundtrack-template.md`.

## Phase 3: Save the Artifact

Ask: `May I write this to production/releases/steam/soundtrack-plan.md?`

If yes, write the file.

## Phase 4: Next Steps

Verdict: **COMPLETE** — Steam soundtrack plan prepared.

- Run `$steam-bundles-pricing` if the soundtrack will ship inside a deluxe bundle.
- Run `$steam-review-ready` before the soundtrack review submit.
