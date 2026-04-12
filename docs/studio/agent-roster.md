# Agent Roster

The following agents are available. Each has a dedicated TOML definition in
`.codex/agents/`. Use the agent best suited to the task at hand. When a task
spans multiple domains, the coordinating agent (usually `producer` or the
domain lead) should delegate to specialists.

The model values below reflect the current `.codex/agents/*.toml` files. If a
TOML file changes, treat the file as the source of truth and update this roster.
Each agent file also declares `sandbox_mode` and `nickname_candidates` so
spawned sessions have explicit runtime defaults and more readable thread labels.

## Tier 1 -- Leadership Agents (`gpt-5.4`)

| Agent | Domain | When to Use |
|-------|--------|-------------|
| `creative-director` | High-level vision | Major creative decisions, pillar conflicts, tone and direction |
| `technical-director` | Technical vision | Architecture decisions, tech stack choices, performance strategy |
| `producer` | Production management | Sprint planning, milestone tracking, risk management, coordination |

## Tier 2 -- Department Lead Agents (`gpt-5.4-mini`)

| Agent | Domain | When to Use |
|-------|--------|-------------|
| `game-designer` | Game design | Mechanics, systems, progression, economy, balancing |
| `lead-programmer` | Code architecture | System design, code review, API design, refactoring |
| `art-director` | Visual direction | Style guides, art bible, asset standards, UI/UX direction |
| `audio-director` | Audio direction | Music direction, sound palette, audio implementation strategy |
| `narrative-director` | Story and writing | Story arcs, world-building, character design, dialogue strategy |
| `qa-lead` | Quality assurance | Test strategy, bug triage, release readiness, regression planning |
| `release-manager` | Release pipeline | Build management, versioning, changelogs, deployment, rollbacks |
| `localization-lead` | Internationalization | String externalization, translation pipeline, locale testing |

## Tier 3 -- Specialist Agents

| Agent | Domain | Model | When to Use |
|-------|--------|-------|-------------|
| `systems-designer` | Systems design | `gpt-5.4-mini` | Specific mechanic implementation, formula design, loops |
| `level-designer` | Level design | `gpt-5.4-mini` | Level layouts, pacing, encounter design, flow |
| `economy-designer` | Economy/balance | `gpt-5.4-mini` | Resource economies, loot tables, progression curves |
| `gameplay-programmer` | Gameplay code | `gpt-5.4-mini` | Feature implementation, gameplay systems code |
| `engine-programmer` | Engine systems | `gpt-5.4-mini` | Core engine, rendering, physics, memory management |
| `ai-programmer` | AI systems | `gpt-5.4-mini` | Behavior trees, pathfinding, NPC logic, state machines |
| `network-programmer` | Networking | `gpt-5.4-mini` | Netcode, replication, lag compensation, matchmaking |
| `tools-programmer` | Dev tools | `gpt-5.4-mini` | Editor extensions, pipeline tools, debug utilities |
| `ui-programmer` | UI implementation | `gpt-5.4-mini` | UI framework, screens, widgets, data binding |
| `technical-artist` | Tech art | `gpt-5.4-mini` | Shaders, VFX, optimization, art pipeline tools |
| `sound-designer` | Sound design | `gpt-5.3-codex-spark` | SFX design docs, audio event lists, mixing notes |
| `writer` | Dialogue/lore | `gpt-5.4-mini` | Dialogue writing, lore entries, item descriptions |
| `world-builder` | World/lore design | `gpt-5.4-mini` | World rules, faction design, history, geography |
| `qa-tester` | Test execution | `gpt-5.4-mini` | Writing test cases, bug reports, test checklists |
| `performance-analyst` | Performance | `gpt-5.4-mini` | Profiling, optimization recommendations, memory analysis |
| `devops-engineer` | Build/deploy | `gpt-5.3-codex-spark` | CI/CD, build scripts, version control workflow |
| `analytics-engineer` | Telemetry | `gpt-5.4-mini` | Event tracking, dashboards, A/B test design |
| `ux-designer` | UX flows | `gpt-5.4-mini` | User flows, wireframes, accessibility, input handling |
| `prototyper` | Rapid prototyping | `gpt-5.4-mini` | Throwaway prototypes, mechanic testing, feasibility validation |
| `security-engineer` | Security | `gpt-5.4-mini` | Anti-cheat, exploit prevention, save encryption, network security |
| `accessibility-specialist` | Accessibility | `gpt-5.4-mini` | WCAG compliance, colorblind modes, remapping, text scaling |
| `live-ops-designer` | Live operations | `gpt-5.4-mini` | Seasons, events, battle passes, retention, live economy |
| `community-manager` | Community | `gpt-5.3-codex-spark` | Patch notes, player feedback, crisis comms, community health |

## Engine-Specific Agents (use the set matching your engine)

### Engine Leads

| Agent | Engine | Model | When to Use |
| ---- | ---- | ---- | ---- |
| `unreal-specialist` | Unreal Engine 5 | `gpt-5.4-mini` | Blueprint vs C++, GAS overview, UE subsystems, Unreal optimization |
| `unity-specialist` | Unity | `gpt-5.4-mini` | MonoBehaviour vs DOTS, Addressables, URP/HDRP, Unity optimization |
| `godot-specialist` | Godot 4 | `gpt-5.4-mini` | GDScript patterns, node/scene architecture, signals, Godot optimization |

### Unreal Engine Sub-Specialists

| Agent | Subsystem | Model | When to Use |
| ---- | ---- | ---- | ---- |
| `ue-gas-specialist` | Gameplay Ability System | `gpt-5.4-mini` | Abilities, gameplay effects, attribute sets, tags, prediction |
| `ue-blueprint-specialist` | Blueprint Architecture | `gpt-5.4-mini` | BP/C++ boundary, graph standards, naming, BP optimization |
| `ue-replication-specialist` | Networking/Replication | `gpt-5.4-mini` | Property replication, RPCs, prediction, relevancy, bandwidth |
| `ue-umg-specialist` | UMG/CommonUI | `gpt-5.4-mini` | Widget hierarchy, data binding, CommonUI input, UI performance |

### Unity Sub-Specialists

| Agent | Subsystem | Model | When to Use |
| ---- | ---- | ---- | ---- |
| `unity-dots-specialist` | DOTS/ECS | `gpt-5.4-mini` | Entity Component System, Jobs, Burst compiler, hybrid renderer |
| `unity-shader-specialist` | Shaders/VFX | `gpt-5.4-mini` | Shader Graph, VFX Graph, URP/HDRP customization, post-processing |
| `unity-addressables-specialist` | Asset Management | `gpt-5.4-mini` | Addressable groups, async loading, memory, content delivery |
| `unity-ui-specialist` | UI Toolkit/UGUI | `gpt-5.4-mini` | UI Toolkit, UXML/USS, UGUI Canvas, data binding, cross-platform input |

### Godot Sub-Specialists

| Agent | Subsystem | Model | When to Use |
| ---- | ---- | ---- | ---- |
| `godot-gdscript-specialist` | GDScript | `gpt-5.4-mini` | Static typing, design patterns, signals, coroutines, GDScript performance |
| `godot-csharp-specialist` | C#/.NET | `gpt-5.4-mini` | Assemblies, exported properties, signals, interop, C# performance |
| `godot-shader-specialist` | Shaders/Rendering | `gpt-5.4-mini` | Godot shading language, visual shaders, particles, post-processing |
| `godot-gdextension-specialist` | GDExtension | `gpt-5.4-mini` | C++/Rust bindings, native performance, custom nodes, build systems |
