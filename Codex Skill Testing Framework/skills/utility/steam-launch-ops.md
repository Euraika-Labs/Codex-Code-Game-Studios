# Skill Spec: /steam-launch-ops

> Framework-maintenance reference for Codex Code Game Studios. Use this area when validating the skills, agents, and workflow contracts that ship with the framework itself.

> **Category**: utility
> **Priority**: medium
> **Spec written**: 2026-04-13

## Skill Summary

Creates the Steam launch-day runbook covering unlock timing, go-live checks,
war-room ownership, monitoring, escalation, and hotfix triggers.

## Static Assertions

- [ ] Frontmatter exists
- [ ] `agents/openai.yaml` exists
- [ ] Uses `May I write`
- [ ] Points to `$team-release` or `$hotfix`

## Test Cases

### Case 1: Happy Path
- Fixture: Steam publish plan and review packet exist
- Expected: writes `production/releases/steam/launch-ops.md`

### Case 2: Sparse Inputs
- Fixture: publish plan exists but review packet is missing
- Expected: runbook still drafts, but flags missing final storefront evidence

## Coverage Notes

This skill is a strong candidate for future live scenario coverage because it
touches real launch operations.
