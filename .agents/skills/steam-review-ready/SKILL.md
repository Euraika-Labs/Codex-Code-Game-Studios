---
name: steam-review-ready
description: Produce a Steam review-readiness packet covering store page completeness, build submission readiness, depot/package checks, and reviewer-facing risks. Use before Steam review submission.
---

> **Explicit invocation only**: Run this skill only when the user explicitly asks for `$steam-review-ready`.

# Steam Review Ready

## Phase 1: Load Context

Read:
- `production/releases/steam/steam-publish-plan.md`
- `production/releases/steam/store-assets.md` if it exists
- `production/releases/release-checklist-*.md` if it exists
- `docs/studio/templates/steam-review-ready-template.md`

If the publish plan is missing, report `Verdict: BLOCKED` and tell the user to
run `$steam-publish-plan` first.

## Phase 2: Generate Review Packet

Summarize:
- store page completeness
- build/depot/package readiness
- known reviewer risks or disclosures
- open blockers before review submit

Use `docs/studio/templates/steam-review-ready-template.md`.

## Phase 3: Save the Artifact

Ask: `May I write this to production/releases/steam/review-ready.md?`

If yes, write the file.

## Phase 4: Next Steps

Verdict: **COMPLETE** — Steam review packet prepared.

- If the store page is still in flux, run `$steam-store-assets`.
- If the launch path includes a demo, playtest, or Early Access setup, run the
  corresponding Steam variant skill before the final submit.
