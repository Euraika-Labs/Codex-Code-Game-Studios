# Skill Spec: /steam-bundles-pricing

> Framework-maintenance reference for Codex Code Game Studios. Use this area when validating the skills, agents, and workflow contracts that ship with the framework itself.

> **Category**: utility
> **Priority**: medium
> **Spec written**: 2026-04-13

## Skill Summary

Creates the Steam pricing and bundle plan, including regional pricing notes,
launch discounts, deluxe bundles, and pricing caveats.

## Static Assertions

- [ ] Frontmatter exists
- [ ] `agents/openai.yaml` exists
- [ ] Uses `May I write`
- [ ] Includes commercial-risk section

## Test Cases

### Case 1: Happy Path
- Fixture: Steam publish plan exists
- Expected: writes `production/releases/steam/bundles-pricing.md`

### Case 2: Early Access Pricing Risk
- Fixture: project is using Early Access
- Expected: plan surfaces pricing and discount caution

## Coverage Notes

This is a policy-heavy skill, so periodic manual review against current
Steamworks guidance is valuable.
