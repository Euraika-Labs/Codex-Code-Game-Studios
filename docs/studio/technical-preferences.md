# Technical Preferences

This is the shared technical configuration sheet for the current project.
Keep it current whenever the engine, platform targets, performance budgets, or build strategy change.

## Project Configuration

| Field | Value |
| --- | --- |
| Engine | `[set with $setup-engine]` |
| Engine Version | `[set with $setup-engine]` |
| Primary Language | `[set after engine selection]` |
| Target Platforms | `[pc / console / mobile / deck / web]` |
| Build and Packaging | `[toolchain or CI path]` |
| Input Model | `[mouse+keyboard / controller / touch / mixed]` |
| Networking Model | `[single-player / peer-to-peer / dedicated / hybrid]` |

## Performance and Quality Budgets

| Area | Target |
| --- | --- |
| Frame rate | `[e.g. 60 FPS]` |
| Resolution targets | `[e.g. 1080p / 1440p / dynamic]` |
| Load-time expectations | `[e.g. under 10 seconds]` |
| Memory budget | `[set per platform]` |
| Save compatibility expectations | `[strict / flexible / no guarantees during prototype]` |

## Architecture Preferences

Record the defaults the engineering side should assume until an ADR overrides them.

- module boundaries
- data-driven vs hard-coded preferences
- plugin policy
- live-ops or telemetry expectations
- test strategy expectations

## Engine Reference

Link the active version reference here once the engine is configured.
