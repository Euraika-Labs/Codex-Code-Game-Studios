# Root Guidance Reference

This reference explains what belongs in the root `AGENTS.md` and what should move into nearby path-specific guidance instead.

## Root Guide Responsibilities

Keep the root guide focused on repo-wide operating behavior:

- first-step routing
- stable machine-readable anchors for engine setup and gate checks
- source-of-truth documents
- shared workflow expectations
- validation expectations
- broad collaboration rules

## What Does Not Belong in the Root Guide

Move these closer to the work instead:

- file-type-specific coding rules
- path-specific asset constraints
- test-only expectations
- design-only formatting instructions

Those belong in nested `AGENTS.md` files or in the matching reference docs under `docs/studio/`.

## Related References

- `docs/studio/directory-structure.md`
- `docs/studio/rules-reference.md`
- `docs/studio/technical-preferences.md`
- `docs/studio/coordination-rules.md`
- `docs/studio/coding-standards.md`

## Required Runtime Anchors

The root `AGENTS.md` must keep these headings and labels stable because repo skills and E2E scenarios read them directly:

- `## Technology Stack`
- `## Engine Version Reference`
- `## Technical Preferences`
- `- **Engine**: ...`
- `- **Language**: ...`

The same rule applies to `docs/studio/technical-preferences.md`, especially:

- `## Engine & Language`
- `## Input & Platform`
- `## Engine Specialists`
- `### File Extension Routing`
