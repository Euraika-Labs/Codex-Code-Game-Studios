---
name: steam-coming-soon
description: Create a Steam Coming Soon and review calendar covering Steam Direct readiness, store page review, build review, wishlist beats, and release timing. Use when planning the Steam pre-launch window.
---

> **Explicit invocation only**: Run this skill only when the user explicitly asks for `$steam-coming-soon`.

# Steam Coming Soon

## Phase 1: Load Context

Read:
- `production/releases/steam/steam-publish-plan.md` if it exists
- `production/releases/release-checklist-*.md` if relevant
- `docs/studio/steam-publishing-guide.md`
- `docs/studio/templates/steam-coming-soon-calendar-template.md`

If no Steam publish plan exists, continue but call out that the calendar is
being created without a previously approved app/package map.

## Phase 2: Build the Calendar

Generate a calendar that includes:
- store page draft complete date
- store page review submit date
- Coming Soon go-live target
- wishlist/announcement beats
- build review submit target
- release unlock target
- timing risks and slack

Use the template at `docs/studio/templates/steam-coming-soon-calendar-template.md`.

## Phase 3: Save the Artifact

Ask: `May I write this to production/releases/steam/coming-soon-calendar.md?`

If yes, write the file.

## Phase 4: Next Steps

Verdict: **COMPLETE** — Coming Soon calendar prepared.

- Run `$steam-store-assets` to fill the store page inputs.
- Run `$steam-review-ready` before submitting anything to Steam review.
