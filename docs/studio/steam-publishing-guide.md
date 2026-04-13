# Steam Publishing Guide

Steam publishing is built into the release layer of the framework.
Use this guide to decide which Steam skills to run and in what order.

## Start Here

Always begin with:

- `$steam-publish-plan`

That command creates the base planning artifact for the game and establishes whether you also need variant tracks such as demo, playtest, Early Access, DLC, soundtrack, or bundle work.

## Core Release Sequence

Typical premium release flow:

1. `$steam-publish-plan`
2. `$steam-coming-soon`
3. `$steam-store-assets`
4. `$steam-review-ready`
5. `$steam-launch-ops`
6. `$steam-deck-ready`

## Variant Tracks

### Demo

Use when you want an openly available, player-facing slice of the game.

- `$steam-demo`

### Playtest

Use when you want a gated testing program without the same public-store pressure as a demo.

- `$steam-playtest`

### Early Access

Use when the product will launch publicly before full feature completion.

- `$steam-early-access`

### DLC

Use when planning paid or free post-launch content as separate Steam app relationships.

- `$steam-dlc`

### Soundtrack

Use when releasing soundtrack content through Steam’s soundtrack app model.

- `$steam-soundtrack`

### Pricing and Bundles

Use when planning launch discounts, deluxe packs, bundles, and regional pricing considerations.

- `$steam-bundles-pricing`

## Typical Artifact Location

Steam outputs generally live under:

- `production/releases/steam/`

Use the matching templates in `docs/studio/templates/` when the skill asks for or generates a first-class artifact.

## Release Readiness Reminders

Steam work should stay connected to the rest of the release process:

- validate the build
- keep QA evidence current
- keep launch operations explicit
- reflect platform constraints in technical preferences and release notes

## Related Docs

- `docs/WORKFLOW-GUIDE.md`
- `docs/studio/skills-reference.md`
- `docs/studio/director-gates.md`
