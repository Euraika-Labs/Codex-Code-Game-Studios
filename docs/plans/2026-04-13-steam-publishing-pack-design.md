# Steam Publishing Pack Design

**Date:** 2026-04-13
**Status:** Approved for implementation
**Scope:** Add Steamworks-native Codex flows for premium launch, demo, Steam Playtest, Early Access, DLC, soundtrack, bundles, pricing, review readiness, launch operations, and Steam Deck readiness.

## Goals

- Add explicit Codex skills for the Steam-specific release objects and decision points that the generic release flows do not model today.
- Preserve the current generic release pipeline while making Steam the first fully modeled storefront.
- Ship templates, docs, and scenario coverage so the new workflows stay maintainable and testable.

## Non-Goals

- Do not automate Steamworks partner actions or require direct Steam API access.
- Do not redesign the existing cross-store release architecture for Epic/GOG/console in this pass.
- Do not replace the generic release skills; layer Steam-specific workflows on top of them.

## Chosen Approach

Create a separate Steam publishing pack that integrates with the existing release phase rather than overloading `$release-checklist`, `$launch-checklist`, and `$team-release`.

This pack adds:

- New Steam-specific repo skills for planning, store readiness, demo/playtest/Early Access/DLC variants, and launch operations.
- A dedicated `steam-publishing-manager` custom agent for Steamworks-specific reasoning and orchestration support.
- Steam-specific templates for app/package/depot planning, review calendars, store assets, Early Access answers, and ownership/release variants.
- Workflow guide and skills-reference updates so users can discover the Steam layer naturally.
- Validation and scenario coverage so the new skills are part of the repo's Codex-native contracts.

## Why This Approach

- It keeps the existing generic release skills readable and broadly applicable.
- It maps cleanly to Steamworks' own object model: base app, child apps, packages, depots, reviews, release states, and variants.
- It scales to demo, Early Access, DLC, soundtrack, bundles, and launch operations without turning one checklist into an unreadable mega-skill.

## Planned Skill Surface

- `$steam-publish-plan`
- `$steam-coming-soon`
- `$steam-store-assets`
- `$steam-review-ready`
- `$steam-demo`
- `$steam-playtest`
- `$steam-early-access`
- `$steam-dlc`
- `$steam-soundtrack`
- `$steam-bundles-pricing`
- `$steam-launch-ops`
- `$steam-deck-ready`

## Planned Templates

- `steam-publish-plan-template.md`
- `steam-coming-soon-calendar-template.md`
- `steam-store-assets-template.md`
- `steam-review-ready-template.md`
- `steam-demo-plan-template.md`
- `steam-playtest-plan-template.md`
- `steam-early-access-template.md`
- `steam-dlc-plan-template.md`
- `steam-soundtrack-template.md`
- `steam-bundles-pricing-template.md`
- `steam-launch-ops-template.md`
- `steam-deck-ready-template.md`

## Integration Points

- Keep generic release skills as the cross-store baseline.
- Add Steam references from the workflow guide's release section.
- Add Steam skills to the skills reference and testing catalog.
- Extend workflow coverage and scenario fixtures with Steam-specific obligations.

## Validation Strategy

- Keep static validation via `scripts/validate_codex_native.py`.
- Regenerate metadata with `scripts/sync_codex_metadata.py`.
- Add at least one live scenario that exercises the Steam planning flow in a blank-project fixture.
- Rebuild the workflow matrix after the new skills and scenarios are in place.

## Risks and Mitigations

- Risk: Steam rules change over time.
  Mitigation: capture current Steamworks facts in references/templates, keep the skills procedural rather than over-prescriptive, and note where users must verify live partner settings.

- Risk: too many narrow skills could become noisy.
  Mitigation: keep each skill explicit-invocation-only by default and organize them as a coherent release pack.

- Risk: coverage drifts as the pack grows.
  Mitigation: update catalog, scenario coverage, workflow matrix, and validation together in the same change set.
