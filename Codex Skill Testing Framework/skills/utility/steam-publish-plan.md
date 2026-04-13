# Skill Spec: /steam-publish-plan

> Framework-maintenance reference for Codex Code Game Studios. Use this area when validating the skills, agents, and workflow contracts that ship with the framework itself.

> **Category**: utility
> **Priority**: medium
> **Spec written**: 2026-04-13

## Skill Summary

Builds the master Steamworks publishing plan for the base game and its release
variants. It maps the base app, child apps, packages, depots, review timing,
Coming Soon needs, and the next Steam-specific skills to run.

## Static Assertions

- [ ] YAML frontmatter includes `name` and `description`
- [ ] `agents/openai.yaml` exists and mentions `$steam-publish-plan`
- [ ] Uses `May I write` before saving
- [ ] Ends with `Verdict: COMPLETE` and next-step guidance

## Test Cases

### Case 1: Happy Path
- Fixture: generic release-stage repo with Steam as a target storefront
- Expected: generates `production/releases/steam/steam-publish-plan.md`

### Case 2: Blocked
- Fixture: project clearly not targeting Steam
- Expected: `Verdict: BLOCKED` with redirect to generic release skills

## Coverage Notes

Primary live scenario coverage comes from the fixture scenario that writes the
Steam publish plan in a throwaway repo copy.
