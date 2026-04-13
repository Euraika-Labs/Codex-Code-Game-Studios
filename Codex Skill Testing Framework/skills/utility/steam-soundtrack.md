# Skill Spec: /steam-soundtrack

> **Category**: utility
> **Priority**: medium
> **Spec written**: 2026-04-13

## Skill Summary

Creates the soundtrack release plan for a Steam soundtrack app, music rights,
artwork, pricing, and bundle inclusion.

## Static Assertions

- [ ] Frontmatter exists
- [ ] `agents/openai.yaml` exists
- [ ] Uses `May I write`
- [ ] Includes bundle follow-up guidance

## Test Cases

### Case 1: Happy Path
- Fixture: Steam publish plan exists
- Expected: writes `production/releases/steam/soundtrack-plan.md`

### Case 2: Deluxe Bundle Dependency
- Fixture: soundtrack is part of a deluxe bundle
- Expected: plan references `$steam-bundles-pricing`

## Coverage Notes

This skill should stay distinct from DLC planning because the Steam soundtrack
surface has its own packaging model.
