---
name: steam-launch-ops
description: Create a Steam launch operations runbook covering release unlock timing, go-live checks, on-call ownership, monitoring, escalation thresholds, and hotfix triggers. Use right before a Steam launch.
---

> **Explicit invocation only**: Run this skill only when the user explicitly asks for `$steam-launch-ops`.

# Steam Launch Ops

## Phase 1: Load Context

Read:
- `production/releases/steam/steam-publish-plan.md`
- `production/releases/steam/review-ready.md` if it exists
- `production/releases/steam/bundles-pricing.md` if it exists
- `docs/studio/templates/steam-launch-ops-template.md`

## Phase 2: Generate the Runbook

Cover:
- release unlock timing
- owners on call
- store/build/pricing checks
- community and dashboard timing
- first-24-hour monitoring and escalation thresholds
- hotfix trigger conditions

Use `docs/studio/templates/steam-launch-ops-template.md`.

## Phase 3: Save the Artifact

Ask: `May I write this to production/releases/steam/launch-ops.md?`

If yes, write the file.

## Phase 4: Next Steps

Verdict: **COMPLETE** — Steam launch runbook prepared.

- Run `$team-release` to coordinate the final cross-functional release path.
- Run `$hotfix` if the launch runbook identifies a likely day-one patch path.
