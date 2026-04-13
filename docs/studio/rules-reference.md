# Rules Reference

Path-specific behavior in this repo is defined through nested `AGENTS.md` files.

## Why Nested Guidance Exists

Different areas of a game repo need different rules:

- code needs implementation standards
- design docs need artifact conventions
- tests need evidence expectations
- assets need pipeline and naming constraints

Nested `AGENTS.md` files let Codex pick up the right rules near the work being edited.

## Typical Guided Areas

- `src/`
- `design/`
- `assets/`
- `tests/`
- `docs/`
- `prototypes/`

## Rule Design Principles

- keep rules local to where they matter
- avoid repeating the root guide everywhere
- write rules as actionable behavior, not philosophy only
- update the rule near the path that changed
