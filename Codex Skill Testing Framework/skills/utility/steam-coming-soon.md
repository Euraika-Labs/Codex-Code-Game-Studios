# Skill Spec: /steam-coming-soon

> Framework-maintenance reference for Codex Code Game Studios. Use this area when validating the skills, agents, and workflow contracts that ship with the framework itself.

> **Category**: utility
> **Priority**: medium
> **Spec written**: 2026-04-13

## Skill Summary

Produces the Steam pre-launch calendar covering store review, Coming Soon timing,
wishlist beats, and release slack.

## Static Assertions

- [ ] Frontmatter exists
- [ ] `agents/openai.yaml` exists
- [ ] Uses `May I write`
- [ ] Includes a next-step section

## Test Cases

### Case 1: Happy Path
- Fixture: Steam publish plan exists
- Expected: writes `production/releases/steam/coming-soon-calendar.md`

### Case 2: No Prior Plan
- Fixture: no publish plan
- Expected: still drafts the calendar but flags the missing upstream artifact

## Coverage Notes

Behavior is mostly document-generation logic and should be smoke-tested after
metadata sync and static validation.
