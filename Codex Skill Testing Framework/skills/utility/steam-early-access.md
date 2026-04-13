# Skill Spec: /steam-early-access

> **Category**: utility
> **Priority**: medium
> **Spec written**: 2026-04-13

## Skill Summary

Builds the Early Access plan, including the Steam Q and A, roadmap framing,
save strategy, cadence, and price-change cautions.

## Static Assertions

- [ ] Frontmatter exists
- [ ] `agents/openai.yaml` exists
- [ ] Uses `May I write`
- [ ] Can emit `Verdict: BLOCKED`

## Test Cases

### Case 1: Happy Path
- Fixture: Steam publish plan exists
- Expected: writes `production/releases/steam/early-access-plan.md`

### Case 2: Missing Upstream Plan
- Fixture: no Steam publish plan
- Expected: `Verdict: BLOCKED`

## Coverage Notes

Manual review should check that the price and discount language stays cautious
and does not promise unsupported Steam behavior.
