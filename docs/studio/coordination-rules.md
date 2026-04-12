# Agent Coordination Rules

1. **Vertical Delegation**: Leadership agents delegate to department leads, who
   delegate to specialists. Never skip a tier for complex decisions.
2. **Horizontal Consultation**: Agents at the same tier may consult each other
   but must not make binding decisions outside their domain.
3. **Conflict Resolution**: When two agents disagree, escalate to the shared
   parent. If no shared parent, escalate to `creative-director` for design
   conflicts or `technical-director` for technical conflicts.
4. **Change Propagation**: When a design change affects multiple domains, the
   `producer` agent coordinates the propagation.
5. **No Unilateral Cross-Domain Changes**: An agent must never modify files
   outside its designated directories without explicit delegation.

## Codex Model Profiles

Use these neutral profile names in studio docs. The actual `.codex/agents/*.toml`
files remain the source of truth for model selection.

| Profile | Default model | When to use |
|------|-------|-------------|
| **Fast** | `gpt-5.3-codex-spark` | Quick read-only checks, status summaries, lightweight operational tasks |
| **Standard** | `gpt-5.4-mini` | Default for most implementation, design authoring, and single-domain analysis |
| **Flagship** | `gpt-5.4` | High-stakes multi-document synthesis, phase gates, and cross-discipline decisions |

Recommended defaults:

- Use **Fast** for utility/status workflows such as `$help`,
  `$project-stage-detect`, `$changelog`, and other mostly read-and-format tasks.
- Use **Flagship** for director-grade reviews such as `$review-all-gdds`,
  `$architecture-review`, and `$gate-check`.
- Use **Standard** for everything else unless a specific agent file overrides it.

## Subagents vs External Agent Teams

This project uses two distinct multi-agent patterns:

### Subagents (built-in, preferred)

Spawn focused subagents within a single Codex session. Use built-in agent types
or project-scoped custom agents from `.codex/agents/`. Subagents inherit the
parent session's approval, sandbox, and most runtime context unless a custom
agent overrides specific settings.

**When to run subagents in parallel**: If two subagents can begin without each
other's output, start both before waiting. Example: independent review phases
that inspect different artifacts.

### External Agent Teams (optional, project-managed)

If you want true multi-session parallelism, orchestrate multiple Codex sessions
outside the CLI and coordinate them with a shared task list or supervisor
process. This is a project convention, not a built-in Codex CLI feature, so
document the launcher, ownership rules, and merge protocol before using it.

**Use external agent teams when**:

- Work spans multiple subsystems that will not touch the same files
- Each workstream is long-running enough to justify true parallel sessions
- A coordinating agent or human is available to integrate results

**Do not use external agent teams when**:

- One session's output is required as input for another
- The work fits comfortably in one session with built-in subagents
- The extra coordination cost outweighs the time saved

## Parallel Subagent Protocol

When an orchestration skill spawns multiple independent subagents:

1. Issue all independent subagent calls before waiting for any result
2. Collect all results before proceeding to dependent phases
3. If any agent is BLOCKED, surface it immediately and do not silently skip it
4. Always produce a partial report if some agents complete and others block
