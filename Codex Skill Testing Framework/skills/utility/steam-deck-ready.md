# Skill Spec: /steam-deck-ready

> **Category**: utility
> **Priority**: medium
> **Spec written**: 2026-04-13

## Skill Summary

Creates the Steam Deck readiness summary for controller support, readability,
performance, suspend-resume behavior, and remaining compatibility blockers.

## Static Assertions

- [ ] Frontmatter exists
- [ ] `agents/openai.yaml` exists
- [ ] Uses `May I write`
- [ ] Includes re-run guidance for late changes

## Test Cases

### Case 1: Happy Path
- Fixture: technical preferences exist
- Expected: writes `production/releases/steam/steam-deck-ready.md`

### Case 2: Late Risk Scan
- Fixture: late-stage release with unresolved performance concerns
- Expected: summary clearly lists blockers instead of over-claiming readiness

## Coverage Notes

This skill should remain advisory and should not imply Valve review outcomes.
