# Skills Reference

This file maps the repo skills to the work they are meant to drive.
Mention skills directly in Codex prompts, for example `$start` or `$design-system`.

## Onboarding and Navigation

| Command | Purpose |
| --- | --- |
| `$start` | guided first-step router for new or ambiguous projects |
| `$help` | context-aware “what next?” assistant |
| `$project-stage-detect` | phase and artifact audit for existing repos |
| `$setup-engine` | lock engine and version, then align technical references |
| `$adopt` | brownfield audit for existing repos that need framework alignment |

## Design and Discovery

| Command | Purpose |
| --- | --- |
| `$brainstorm` | concept generation and refinement |
| `$map-systems` | systems inventory, dependencies, and priorities |
| `$design-system` | full system GDD authoring |
| `$quick-design` | smaller-scoped design note for limited changes |
| `$review-all-gdds` | cross-document design coherence review |
| `$propagate-design-change` | impact review after a design update |

## UX

| Command | Purpose |
| --- | --- |
| `$ux-design` | write UX specifications and interaction flows |
| `$ux-review` | check UX outputs for consistency, accessibility, and clarity |

## Architecture and Technical Direction

| Command | Purpose |
| --- | --- |
| `$create-architecture` | author the master architecture document |
| `$architecture-decision` | create a focused ADR |
| `$architecture-review` | review ADR quality and coverage |
| `$create-control-manifest` | flatten accepted decisions into programmer guidance |
| `$reverse-document` | document architecture or design from existing code |

## Planning and Delivery

| Command | Purpose |
| --- | --- |
| `$create-epics` | convert design and architecture into epics |
| `$create-stories` | break epics into implementable stories |
| `$story-readiness` | confirm a story is ready for pickup |
| `$dev-story` | implement a story using the appropriate coding specialist |
| `$story-done` | verify a story is complete and update status |
| `$sprint-plan` | build or refresh a sprint plan |
| `$sprint-status` | summarize sprint health |
| `$estimate` | produce a structured effort estimate |

## Review, Quality, and Risk

| Command | Purpose |
| --- | --- |
| `$design-review` | review a design doc |
| `$code-review` | review a file or changeset from a code-quality perspective |
| `$balance-check` | inspect formulas, tuning, and game economies |
| `$asset-audit` | check asset naming, budgets, and pipeline consistency |
| `$content-audit` | compare planned content against implemented content |
| `$scope-check` | detect scope creep or mismatched delivery expectations |
| `$perf-profile` | identify performance risks and likely bottlenecks |
| `$tech-debt` | identify and prioritize debt |
| `$consistency-check` | scan for contradictions across design artifacts |
| `$gate-check` | evaluate readiness to cross a phase boundary |

## QA and Testing

| Command | Purpose |
| --- | --- |
| `$qa-plan` | build a QA plan |
| `$smoke-check` | critical-path smoke gate |
| `$soak-test` | extended-session test protocol |
| `$regression-suite` | identify missing regression protection |
| `$test-setup` | scaffold project testing and CI foundations |
| `$test-helpers` | create engine-specific helpers for the test suite |
| `$test-evidence-review` | review test evidence quality |
| `$test-flakiness` | investigate unstable tests |
| `$skill-test` | validate repo skill definitions and behavior |

## Production and Team Health

| Command | Purpose |
| --- | --- |
| `$milestone-review` | assess milestone progress and risk |
| `$retrospective` | run a retrospective |
| `$bug-report` | generate a structured bug report |
| `$bug-triage` | prioritize and route bugs |
| `$playtest-report` | summarize or analyze playtest findings |
| `$onboard` | create onboarding guidance for a new contributor |
| `$localize` | plan and validate localization work |

## Release and Live Operations

| Command | Purpose |
| --- | --- |
| `$release-checklist` | build the pre-release checklist |
| `$launch-checklist` | validate launch readiness across disciplines |
| `$changelog` | generate internal change history |
| `$patch-notes` | produce player-facing notes |
| `$hotfix` | execute emergency fix workflow with audit trail |

## Steam Publishing Pack

| Command | Purpose |
| --- | --- |
| `$steam-publish-plan` | master Steamworks plan for the base game and release variants |
| `$steam-coming-soon` | coming-soon timing, review lead time, wishlist beats |
| `$steam-store-assets` | store copy and asset pack planning |
| `$steam-review-ready` | submission-readiness packet |
| `$steam-demo` | demo strategy and setup |
| `$steam-playtest` | gated playtest strategy and cohorts |
| `$steam-early-access` | Early Access positioning and Q&A planning |
| `$steam-dlc` | DLC structure and release impact |
| `$steam-soundtrack` | soundtrack release planning |
| `$steam-bundles-pricing` | pricing, discounts, and bundle strategy |
| `$steam-launch-ops` | launch-day runbook and monitoring |
| `$steam-deck-ready` | Steam Deck readiness summary |

## Team Orchestration

Team skills coordinate groups of agents around a shared theme:

- `$team-combat`
- `$team-narrative`
- `$team-ui`
- `$team-release`
- `$team-polish`
- `$team-audio`
- `$team-level`
- `$team-live-ops`
- `$team-qa`

Use these when a task genuinely needs multiple disciplines in one coordinated pass.
