---
name: steam-publish-plan
description: Build a Steamworks publishing plan covering app relationships, packages, depots, review sequencing, Coming Soon timing, and which Steam variant flows apply. Use when preparing a Steam release for a premium game, demo, playtest, Early Access, DLC, soundtrack, or bundle.
---

> **Explicit invocation only**: Run this skill only when the user explicitly asks for `$steam-publish-plan`.

# Steam Publish Plan

## Phase 1: Parse Arguments

Read the release shape from the argument: `premium`, `demo`, `playtest`,
`early-access`, `dlc`, `soundtrack`, `bundle`, or `mixed`. If missing, default
to `mixed`.

## Phase 2: Load Project Context

Read:
- `AGENTS.md`
- `docs/studio/technical-preferences.md` if it exists
- `production/releases/` current release artifacts if they exist
- `docs/studio/steam-publishing-guide.md`
- `docs/studio/templates/steam-publish-plan-template.md`

If the project is not targeting PC storefronts or Steam is not in scope, report:
`Verdict: BLOCKED` and tell the user to continue with the generic release flows.

## Phase 3: Build the Plan

Generate a Steam publishing plan that covers:
- the base game release shape
- child app candidates: demo, playtest, DLC, soundtrack
- package and depot planning
- store page and build review sequencing
- Coming Soon timing
- variant decisions: which downstream Steam skills should run next
- risk register and owners

Use the template structure from `docs/studio/templates/steam-publish-plan-template.md`.

## Phase 4: Save the Artifact

Present the draft and ask: `May I write this to production/releases/steam/steam-publish-plan.md?`

If yes, write the file and create the directory if needed.

## Phase 5: Next Steps

Verdict: **COMPLETE** — Steam publishing plan prepared.

- Run `$steam-coming-soon` for the calendar and review sequence.
- Run the relevant variant skills next: `$steam-demo`, `$steam-playtest`,
  `$steam-early-access`, `$steam-dlc`, `$steam-soundtrack`, or
  `$steam-bundles-pricing`.
