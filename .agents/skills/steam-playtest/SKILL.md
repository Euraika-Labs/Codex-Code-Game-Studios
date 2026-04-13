---
name: steam-playtest
description: Create a Steam Playtest operations plan covering signup messaging, cohort waves, build cadence, feedback collection, and exit criteria. Use when planning gated Steam testing before launch.
---

> **Explicit invocation only**: Run this skill only when the user explicitly asks for `$steam-playtest`.

# Steam Playtest

## Phase 1: Load Context

Read:
- `production/releases/steam/steam-publish-plan.md` if it exists
- `production/qa/` playtest notes if they exist
- `docs/studio/templates/steam-playtest-plan-template.md`

## Phase 2: Generate the Playtest Plan

Cover:
- what the playtest is trying to prove
- signup messaging and admission policy
- approval-wave design
- build cadence and feedback collection
- exit criteria and transition path to demo or launch

Use `docs/studio/templates/steam-playtest-plan-template.md`.

## Phase 3: Save the Artifact

Ask: `May I write this to production/releases/steam/playtest-plan.md?`

If yes, write the file.

## Phase 4: Next Steps

Verdict: **COMPLETE** — Steam Playtest plan prepared.

- Run `$playtest-report` after each cohort wave.
- Run `$steam-launch-ops` once the playtest transitions into launch preparation.
