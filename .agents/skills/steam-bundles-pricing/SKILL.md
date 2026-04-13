---
name: steam-bundles-pricing
description: Create a Steam pricing and bundle plan covering regional pricing, launch discounts, deluxe packages, soundtrack or DLC bundles, and Steam-specific pricing risks. Use when setting commercial terms on Steam.
---

> **Explicit invocation only**: Run this skill only when the user explicitly asks for `$steam-bundles-pricing`.

# Steam Bundles and Pricing

## Phase 1: Load Context

Read:
- `production/releases/steam/steam-publish-plan.md`
- any existing `production/releases/steam/*plan*.md`
- `docs/studio/templates/steam-bundles-pricing-template.md`

## Phase 2: Generate the Pricing Plan

Cover:
- base price and launch-discount proposal
- regional pricing notes and approvals
- bundle types and included products
- Early Access or discount-window caveats
- open commercial decisions

Use `docs/studio/templates/steam-bundles-pricing-template.md`.

## Phase 3: Save the Artifact

Ask: `May I write this to production/releases/steam/bundles-pricing.md?`

If yes, write the file.

## Phase 4: Next Steps

Verdict: **COMPLETE** — Steam pricing plan prepared.

- Run `$steam-launch-ops` once pricing, bundles, and release timing are aligned.
- Revisit `$steam-early-access` if the project changes price during Early Access.
