# Agent Coordination Map

This document explains which agent should lead which kind of work and when responsibilities should move from one role to another.

## Core Rule

The agent who owns the main decision should lead. Specialists support the lead. Directors step in when the decision crosses discipline boundaries or affects project direction.

## Common Leadership Patterns

| Situation | Lead Agent | Typical Supporting Agents |
| --- | --- | --- |
| new game concept | `creative-director` | `game-designer`, `producer` |
| architecture reset | `technical-director` | `lead-programmer`, engine specialist |
| sprint replanning | `producer` | `qa-lead`, `lead-programmer`, `game-designer` |
| new gameplay system | `game-designer` | `systems-designer`, `gameplay-programmer`, `qa-tester` |
| UI overhaul | `ux-designer` or `art-director` | `ui-programmer`, `accessibility-specialist` |
| release readiness | `release-manager` | `qa-lead`, `producer`, `devops-engineer`, `steam-publishing-manager` |
| Steam launch planning | `steam-publishing-manager` | `release-manager`, `community-manager`, `producer` |

## Escalation Rules

Escalate to a director when:

- a decision changes scope, staffing, or phase timing
- creative and technical goals conflict
- delivery pressure threatens product quality or identity

Escalate to a lead when:

- a specialist needs domain approval
- multiple specialists in one discipline need coordination
- a review must convert findings into a domain plan

## Team Skills

The repo already encodes the most common coordination bundles through `$team-*` skills. Use those when the collaboration pattern is known in advance.

## Keep Coordination Lightweight

- do not spawn multiple agents for work that one specialist can finish cleanly
- do not delegate the immediate blocking task if you need the result right away
- use leads to synthesize, not to duplicate specialist execution
