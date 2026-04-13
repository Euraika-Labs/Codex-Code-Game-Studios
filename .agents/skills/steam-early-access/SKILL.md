---
name: steam-early-access
description: Create a Steam Early Access plan covering the Early Access Q and A, roadmap framing, save-compatibility strategy, update cadence, and price-change risks. Use when the base game will launch in Early Access.
---

> **Explicit invocation only**: Run this skill only when the user explicitly asks for `$steam-early-access`.

# Steam Early Access

## Phase 1: Load Context

Read:
- `production/releases/steam/steam-publish-plan.md`
- `production/releases/steam/coming-soon-calendar.md` if it exists
- `docs/studio/templates/steam-early-access-template.md`

If the publish plan is missing, report `Verdict: BLOCKED` and ask the user to
run `$steam-publish-plan` first.

## Phase 2: Generate the Early Access Plan

Fill in:
- current playable state
- what remains unfinished
- path to 1.0
- Steam Early Access Q and A draft answers
- save compatibility and update cadence
- pricing and discount cautions

Use `docs/studio/templates/steam-early-access-template.md`.

## Phase 3: Save the Artifact

Ask: `May I write this to production/releases/steam/early-access-plan.md?`

If yes, write the file.

## Phase 4: Next Steps

Verdict: **COMPLETE** — Steam Early Access plan prepared.

- Run `$steam-store-assets` to align the store page with the Early Access message.
- Run `$steam-bundles-pricing` before committing to launch discounts or price changes.
