# Codex Code Game Studios Workflow Guide

This guide explains how the framework moves a game project from concept to release.
It is the operational handbook for the repo.

## How to Read This Guide

Use this document in three ways:

- as a phase map for a new project
- as a routing reference for an existing project
- as the high-level operating model behind `$start`, `$help`, and `$gate-check`

The authoritative workflow catalog remains `docs/studio/workflow-catalog.yaml`. This guide explains how to use it in practice.

## Entry Points

Choose the command that matches the current situation:

| Situation | Start Here |
| --- | --- |
| Brand-new game idea | `$start` or `$brainstorm` |
| You know the game but not the structure | `$setup-engine`, then `$map-systems` |
| Existing repo with unknown maturity | `$project-stage-detect` |
| Existing repo with lots of files but unclear format quality | `$adopt` |
| You only need the next recommended action | `$help` |

## The Seven Phases

### 1. Concept

Purpose: define the game, its pillars, target audience, and core fantasy.

Typical commands:

- `$brainstorm`
- `$design-review` for concept-level docs

Expected artifacts:

- `design/gdd/game-concept.md`
- `design/gdd/game-pillars.md`
- `design/gdd/player-journey.md`

Exit condition:

- the team can explain what the game is, who it is for, and why it is worth building

### 2. Systems Design

Purpose: decompose the concept into production-ready systems and design documents.

Typical commands:

- `$map-systems`
- `$design-system`
- `$review-all-gdds`
- `$propagate-design-change`

Expected artifacts:

- `design/gdd/systems-index.md`
- one or more system GDDs
- related UX specs when the system has player-facing complexity

Exit condition:

- the game is described as a set of coherent, scoped systems with dependencies and priorities

### 3. Technical Setup

Purpose: lock the engine, platform assumptions, architecture direction, and test baseline.

Typical commands:

- `$setup-engine`
- `$create-architecture`
- `$architecture-decision`
- `$test-setup`
- `$create-control-manifest`

Expected artifacts:

- `docs/studio/technical-preferences.md`
- `docs/architecture/` ADRs
- test harness and CI foundations

Exit condition:

- the project has clear technical boundaries, architectural decisions, and testing strategy

### 4. Pre-Production

Purpose: translate design and architecture into executable work.

Typical commands:

- `$create-epics`
- `$create-stories`
- `$story-readiness`
- `$sprint-plan`
- `$estimate`

Expected artifacts:

- epics and story files under `production/epics/`
- sprint plan under `production/sprints/`
- readiness-reviewed work items

Exit condition:

- the team can move into production with scoped, testable, reviewable work

### 5. Production

Purpose: implement features, keep stories moving, and maintain visibility on risk and scope.

Typical commands:

- `$dev-story`
- `$story-done`
- `$sprint-status`
- `$milestone-review`
- `$tech-debt`
- `$bug-report` and `$bug-triage`

Supporting review loops:

- `$code-review`
- `$design-review`
- `$consistency-check`
- `$scope-check`

Exit condition:

- core features are implemented, documented, and converging toward content-complete or feature-complete targets

### 6. Polish

Purpose: raise quality, stability, accessibility, UX clarity, and performance.

Typical commands:

- `$qa-plan`
- `$smoke-check`
- `$soak-test`
- `$regression-suite`
- `$ux-review`
- `$perf-profile`
- `$team-polish`
- `$team-qa`

Exit condition:

- quality risks are understood and the game is approaching release readiness

### 7. Release

Purpose: prepare, validate, publish, and support the launch.

Typical commands:

- `$release-checklist`
- `$launch-checklist`
- `$changelog`
- `$patch-notes`
- `$team-release`
- Steam-specific commands as needed

Steam branch commands:

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

Exit condition:

- the release package, store presence, QA evidence, and launch operations are ready for live execution

## Phase Gates

Use `$gate-check` when you think the project is ready to move forward.
The detailed gate rules live in `docs/studio/director-gates.md`, but the core idea is simple:

- every phase has minimum artifact expectations
- every gate checks quality, not just existence
- unresolved blockers should be fixed before crossing the phase boundary

## Brownfield Projects

Existing game repos do not need to restart from phase one.

The recommended brownfield path is:

1. install the studio into the repo
2. run `$project-stage-detect`
3. run `$adopt`
4. use `$help` to continue from the recommended phase

`project-stage-detect` answers “what is here?”
`adopt` answers “is what is here shaped correctly for the framework?”

## Teaming and Agent Use

The studio model is designed to keep delegation readable and intentional.

- use a lead or director when work spans multiple domains
- use a specialist when the task is bounded and discipline-specific
- use `$team-*` skills when the output genuinely needs coordinated multi-agent work

Reference:

- `docs/studio/agent-roster.md`
- `docs/studio/agent-coordination-map.md`

## Common Operating Loops

### Feature loop

1. design the change
2. confirm architecture impact
3. create or refine story scope
4. implement with the correct specialist
5. review, test, and mark story done

### Quality loop

1. identify risk or regression
2. generate QA plan or evidence target
3. run smoke or regression checks
4. triage issues
5. re-run phase or release gate if needed

### Release loop

1. validate the build and documentation
2. prepare store or platform assets
3. assemble evidence and runbooks
4. confirm launch readiness
5. publish and monitor

## Documents to Keep Current

The framework works best when these stay current:

- `AGENTS.md`
- `docs/studio/technical-preferences.md`
- `design/gdd/systems-index.md`
- architecture ADRs
- sprint plans and story files
- release checklists and runbooks

## Related References

- `docs/studio/quick-start.md`
- `docs/studio/skills-reference.md`
- `docs/studio/director-gates.md`
- `docs/studio/steam-publishing-guide.md`
- `docs/studio/review-workflow.md`
