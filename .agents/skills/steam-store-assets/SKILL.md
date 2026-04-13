---
name: steam-store-assets
description: Build a Steam store asset and copy pack covering capsule messaging, screenshots, trailers, library assets, and proof points. Use when preparing Steam store-facing creative and metadata.
---

> **Explicit invocation only**: Run this skill only when the user explicitly asks for `$steam-store-assets`.

# Steam Store Assets

## Phase 1: Load Context

Read:
- `AGENTS.md`
- `production/releases/steam/steam-publish-plan.md` if it exists
- `design/gdd/game-concept.md` if it exists
- `docs/studio/templates/steam-store-assets-template.md`

## Phase 2: Draft the Asset Pack

Create a Steam-specific asset pack covering:
- capsule messaging and short description
- long description outline and feature bullets
- screenshot/trailer coverage plan
- visual asset checklist with owners and status
- claims or store messages that need proof or caution

Use `docs/studio/templates/steam-store-assets-template.md`.

## Phase 3: Save the Artifact

Ask: `May I write this to production/releases/steam/store-assets.md?`

If yes, write the file.

## Phase 4: Next Steps

Verdict: **COMPLETE** — Steam store asset pack prepared.

- Run `$steam-review-ready` after the actual assets and copy are assembled.
- Run `$steam-coming-soon` if the store campaign calendar still needs to be planned.
