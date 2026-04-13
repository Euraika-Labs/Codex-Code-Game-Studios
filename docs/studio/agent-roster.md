# Agent Roster

This roster explains the role of each custom agent family. The TOML files in `.codex/agents/` remain the source of truth for runtime configuration.

## How to Choose an Agent

- use a director for cross-discipline conflicts or strategic decisions
- use a lead for domain ownership and review
- use a specialist for focused execution
- use an engine-specific specialist when implementation depends on Godot, Unity, or Unreal specifics

## Directors

| Agent | Role | Use For |
| --- | --- | --- |
| `creative-director` | creative alignment | pillars, tone, cohesion, major design tradeoffs |
| `technical-director` | technical alignment | architecture, scalability, performance strategy |
| `producer` | delivery alignment | scope, milestone risk, sequencing, coordination |

## Leads

| Agent | Role | Use For |
| --- | --- | --- |
| `game-designer` | design leadership | systems, progression, core loops |
| `lead-programmer` | engineering leadership | code quality, implementation strategy, refactors |
| `art-director` | visual leadership | style, art bible, asset standards |
| `audio-director` | audio leadership | audio palette, implementation priorities |
| `narrative-director` | story leadership | worldbuilding, narrative consistency, dialogue strategy |
| `qa-lead` | QA leadership | test strategy, risk reviews, release quality |
| `release-manager` | release leadership | builds, launch process, rollback and evidence planning |
| `localization-lead` | localization leadership | string strategy, locale readiness, translation pipeline |

## Domain Specialists

| Agent | Domain |
| --- | --- |
| `systems-designer` | systems and formulas |
| `level-designer` | level flow and encounter pacing |
| `economy-designer` | progression and economy balancing |
| `gameplay-programmer` | gameplay implementation |
| `engine-programmer` | engine-level code and foundations |
| `ai-programmer` | AI behavior and supporting systems |
| `network-programmer` | multiplayer and replication |
| `tools-programmer` | dev tools and internal workflow support |
| `ui-programmer` | UI implementation |
| `technical-artist` | shaders, VFX, optimization, and pipeline glue |
| `sound-designer` | SFX structure and implementation notes |
| `writer` | dialogue and authored text |
| `world-builder` | world logic, lore, factions |
| `qa-tester` | test execution and evidence |
| `performance-analyst` | profiling and optimization guidance |
| `devops-engineer` | CI, build, packaging, release automation |
| `analytics-engineer` | telemetry and instrumentation |
| `steam-publishing-manager` | Steam app/package/depot planning and store operations |
| `ux-designer` | interaction flows and usability |
| `prototyper` | fast throwaway exploration |
| `security-engineer` | exploit, anti-cheat, and data safety concerns |
| `accessibility-specialist` | accessibility and inclusive design |
| `live-ops-designer` | post-launch events and retention systems |
| `community-manager` | outward-facing player communication |

## Engine Specialists

### Unreal

- `unreal-specialist`
- `ue-gas-specialist`
- `ue-blueprint-specialist`
- `ue-replication-specialist`
- `ue-umg-specialist`

### Unity

- `unity-specialist`
- `unity-dots-specialist`
- `unity-shader-specialist`
- `unity-addressables-specialist`
- `unity-ui-specialist`

### Godot

- `godot-specialist`
- `godot-gdscript-specialist`
- `godot-csharp-specialist`
- `godot-shader-specialist`
- `godot-gdextension-specialist`

## Choosing Between Skills and Agents

- use a skill when you need a repeatable workflow
- use an agent when you need judgment within a domain
- use a team skill when multiple agents should coordinate under one theme

## Related Docs

- `docs/studio/skills-reference.md`
- `docs/studio/agent-coordination-map.md`
- `docs/studio/coordination-rules.md`
