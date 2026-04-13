# Agent Spec: /steam-publishing-manager

> Framework-maintenance reference for Codex Code Game Studios. Use this area when validating the skills, agents, and workflow contracts that ship with the framework itself.

## Summary

Steamworks-specialist operations agent for store planning, app relationships,
review sequencing, launch variants, pricing, and launch-day readiness.

## Static Assertions

- [ ] TOML exists under `.codex/agents/steam-publishing-manager.toml`
- [ ] TOML includes `name`, `description`, `developer_instructions`, `sandbox_mode`
- [ ] TOML includes `nickname_candidates`

## Core Cases

### Case 1: Premium launch planning
- Expected: agent can decompose base app, packages, depots, review timing, and launch ops

### Case 2: Variant release planning
- Expected: agent distinguishes demo, playtest, Early Access, DLC, soundtrack, and bundles

### Case 3: Storefront-specific risk scan
- Expected: agent surfaces Steam-specific blockers without overreaching into non-Steam decisions

## Coverage Notes

Best verified indirectly through the Steam skill pack and any future targeted
subagent probe additions.
