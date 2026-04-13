---
name: steam-deck-ready
description: Create a Steam Deck readiness summary covering input, readability, performance, suspend-resume behavior, compatibility risks, and follow-up actions. Use when preparing Steam Deck support or review positioning.
---

> **Explicit invocation only**: Run this skill only when the user explicitly asks for `$steam-deck-ready`.

# Steam Deck Ready

## Phase 1: Load Context

Read:
- `AGENTS.md`
- `docs/studio/technical-preferences.md` if it exists
- `production/releases/steam/steam-publish-plan.md` if it exists
- `docs/studio/templates/steam-deck-ready-template.md`

## Phase 2: Generate the Readiness Summary

Cover:
- current Steam Deck compatibility status
- input model and controller assumptions
- readability and UI scale risks
- performance and suspend-resume concerns
- remaining blockers and recommended follow-up

Use `docs/studio/templates/steam-deck-ready-template.md`.

## Phase 3: Save the Artifact

Ask: `May I write this to production/releases/steam/steam-deck-ready.md?`

If yes, write the file.

## Phase 4: Next Steps

Verdict: **COMPLETE** — Steam Deck readiness summary prepared.

- Run `$steam-launch-ops` before launch if Steam Deck is part of the platform promise.
- Re-run this skill after any major UI, input, or performance changes late in production.
