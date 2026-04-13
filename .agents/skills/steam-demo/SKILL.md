---
name: steam-demo
description: Create a Steam demo plan covering demo App ID strategy, depot sharing, CTA back to the base game, QA scope, and event timing. Use when planning a public Steam demo.
---

> **Explicit invocation only**: Run this skill only when the user explicitly asks for `$steam-demo`.

# Steam Demo

## Phase 1: Load Context

Read:
- `production/releases/steam/steam-publish-plan.md` if it exists
- `production/releases/steam/coming-soon-calendar.md` if it exists
- `docs/studio/templates/steam-demo-plan-template.md`

## Phase 2: Generate the Demo Plan

Cover:
- the demo's funnel goal and CTA to the base game
- separate demo App ID assumptions
- shared depots and shared cloud-save assumptions if relevant
- demo availability window and event tie-ins
- QA scope and success metrics

Use `docs/studio/templates/steam-demo-plan-template.md`.

## Phase 3: Save the Artifact

Ask: `May I write this to production/releases/steam/demo-plan.md?`

If yes, write the file.

## Phase 4: Next Steps

Verdict: **COMPLETE** — Steam demo plan prepared.

- Run `$steam-store-assets` for demo-facing store messaging if the demo has a
  separate store page.
- Run `$steam-review-ready` before demo submission.
