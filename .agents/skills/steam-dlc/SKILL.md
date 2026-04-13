---
name: steam-dlc
description: Create a Steam DLC plan covering DLC App ID setup, ownership gating, depot strategy, bundle effects, messaging, and QA focus. Use when planning a Steam DLC release.
---

> **Explicit invocation only**: Run this skill only when the user explicitly asks for `$steam-dlc`.

# Steam DLC

## Phase 1: Load Context

Read:
- `production/releases/steam/steam-publish-plan.md`
- `production/releases/steam/bundles-pricing.md` if it exists
- `docs/studio/templates/steam-dlc-plan-template.md`

If the base Steam publish plan is missing, report `Verdict: BLOCKED`.

## Phase 2: Generate the DLC Plan

Cover:
- DLC type and launch window
- dependency on the base game
- paid versus free positioning
- App ID, depot, and ownership-gate decisions
- save compatibility
- bundle impact and QA focus

Use `docs/studio/templates/steam-dlc-plan-template.md`.

## Phase 3: Save the Artifact

Ask: `May I write this to production/releases/steam/dlc-plan.md?`

If yes, write the file.

## Phase 4: Next Steps

Verdict: **COMPLETE** — Steam DLC plan prepared.

- Run `$steam-bundles-pricing` if the DLC affects deluxe editions or complete-the-set bundles.
- Run `$steam-review-ready` before the DLC release submission.
