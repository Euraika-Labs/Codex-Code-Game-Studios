# Skill Spec: /steam-review-ready

> **Category**: utility
> **Priority**: medium
> **Spec written**: 2026-04-13

## Skill Summary

Generates the Steam review-readiness packet covering store page completeness,
build readiness, and reviewer-facing risks.

## Static Assertions

- [ ] Frontmatter exists
- [ ] `agents/openai.yaml` exists
- [ ] Uses `May I write`
- [ ] Can emit `Verdict: BLOCKED`

## Test Cases

### Case 1: Happy Path
- Fixture: Steam publish plan exists
- Expected: writes `production/releases/steam/review-ready.md`

### Case 2: Missing Publish Plan
- Fixture: no upstream Steam plan
- Expected: stops with `Verdict: BLOCKED`

## Coverage Notes

This skill is a key guardrail before release submission and should stay
grounded in actual release artifacts.
