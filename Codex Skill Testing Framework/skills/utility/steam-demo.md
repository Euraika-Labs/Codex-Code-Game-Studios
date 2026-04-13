# Skill Spec: /steam-demo

> **Category**: utility
> **Priority**: medium
> **Spec written**: 2026-04-13

## Skill Summary

Creates a Steam demo release plan that captures the demo goal, App ID strategy,
depot-sharing assumptions, CTA back to the base game, and QA scope.

## Static Assertions

- [ ] Frontmatter exists
- [ ] `agents/openai.yaml` exists
- [ ] Uses `May I write`
- [ ] Ends with next steps

## Test Cases

### Case 1: Happy Path
- Fixture: Steam publish plan exists
- Expected: writes `production/releases/steam/demo-plan.md`

### Case 2: Event-Tied Demo
- Fixture: calendar exists with a festival or announcement beat
- Expected: includes availability-window notes and event timing

## Coverage Notes

The skill should remain distinct from `$steam-playtest`; this distinction is a
good manual review point.
