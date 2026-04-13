# Steam Publishing Guide

This repo now includes a Steamworks-native release pack for projects shipping on
Steam. Use it as a specialization layer on top of the generic release skills.

## When To Use Which Flow

- Use `$steam-publish-plan` first when the project needs a Steam release plan.
- Use `$steam-coming-soon` when you are planning store review timing, Coming
  Soon visibility, and wishlist beats.
- Use `$steam-store-assets` when you need the Steam-specific copy and visual
  asset pack.
- Use `$steam-review-ready` before submitting the store page and build for review.
- Use `$steam-demo` when you want an open, public-facing demo with its own App ID.
- Use `$steam-playtest` when you want gated testing and signup waves without a
  full public demo funnel.
- Use `$steam-early-access` when the base product is launching in Early Access
  and needs the Steam Q&A, roadmap framing, and pricing caution.
- Use `$steam-dlc` for paid or free DLC planning, ownership gating, and depot strategy.
- Use `$steam-soundtrack` for a soundtrack app and music release coordination.
- Use `$steam-bundles-pricing` for regional pricing, launch discounts, and
  bundle/deluxe setup.
- Use `$steam-launch-ops` for launch-day release execution and post-launch monitoring.
- Use `$steam-deck-ready` for Steam Deck compatibility preparation and follow-up.

## Variant Selection Heuristic

- Choose **Playtest** when you want controlled access, limited cohorts, or
  server/load validation before broad public marketing.
- Choose **Demo** when you want broad discovery, conversion, and wishlist growth.
- Choose **Early Access** only when the base product is already a legitimate
  purchasable experience and you can explain the current state and roadmap clearly.
- Choose **DLC** when content ownership should attach to the base game after launch.
- Choose **Soundtrack** when music needs its own Steam release surface instead
  of being buried in a normal DLC plan.
- Choose **Bundles** when you need deluxe/complete-the-set packaging or price
  presentation across multiple Steam products.

## How This Fits The Existing Release Phase

The generic release phase still owns broad readiness:

- `$release-checklist`
- `$launch-checklist`
- `$patch-notes`
- `$changelog`
- `$team-release`

The Steam pack adds the storefront-specific work those generic skills do not
model in detail.
