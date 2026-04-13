# Skill Spec: /steam-dlc

> Framework-maintenance reference for Codex Code Game Studios. Use this area when validating the skills, agents, and workflow contracts that ship with the framework itself.

> **Category**: utility
> **Priority**: medium
> **Spec written**: 2026-04-13

## Skill Summary

Creates the DLC plan for ownership gating, depot strategy, bundle impact, and QA.

## Static Assertions

- [ ] Frontmatter exists
- [ ] `agents/openai.yaml` exists
- [ ] Uses `May I write`
- [ ] Can emit `Verdict: BLOCKED`

## Test Cases

### Case 1: Happy Path
- Fixture: Steam publish plan exists
- Expected: writes `production/releases/steam/dlc-plan.md`

### Case 2: Bundle Impact
- Fixture: bundle plan already exists
- Expected: DLC plan references bundle interaction instead of ignoring it

## Coverage Notes

Useful manual review area: day-one DLC perception caveats and separate-depot
versus entitlement-gate recommendations.
