# Skill Spec: /steam-playtest

> **Category**: utility
> **Priority**: medium
> **Spec written**: 2026-04-13

## Skill Summary

Creates the Steam Playtest operations plan for gated cohorts, admission waves,
feedback loops, and exit criteria.

## Static Assertions

- [ ] Frontmatter exists
- [ ] `agents/openai.yaml` exists
- [ ] Uses `May I write`
- [ ] References follow-up testing flow

## Test Cases

### Case 1: Happy Path
- Fixture: Steam publish plan exists
- Expected: writes `production/releases/steam/playtest-plan.md`

### Case 2: Online Test Focus
- Fixture: project includes multiplayer or load-test concerns
- Expected: plan surfaces wave control and operational risk areas

## Coverage Notes

Follow-up live runs should ensure the skill nudges the user toward
`$playtest-report` after each cohort.
