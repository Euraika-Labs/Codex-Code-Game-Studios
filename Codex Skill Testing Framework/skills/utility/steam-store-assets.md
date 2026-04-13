# Skill Spec: /steam-store-assets

> Framework-maintenance reference for Codex Code Game Studios. Use this area when validating the skills, agents, and workflow contracts that ship with the framework itself.

> **Category**: utility
> **Priority**: medium
> **Spec written**: 2026-04-13

## Skill Summary

Creates the Steam store copy and asset pack checklist, including capsule
messaging, screenshots, trailers, and proof-sensitive claims.

## Static Assertions

- [ ] Frontmatter exists
- [ ] `agents/openai.yaml` exists
- [ ] Uses `May I write`
- [ ] Has a clear output artifact

## Test Cases

### Case 1: Happy Path
- Fixture: Steam publish plan plus base game concept
- Expected: writes `production/releases/steam/store-assets.md`

### Case 2: Sparse Context
- Fixture: only AGENTS.md exists
- Expected: produces a draft checklist with explicit gaps instead of hallucinating assets

## Coverage Notes

Useful follow-up live testing would verify the skill stays grounded when art and
marketing docs are missing.
