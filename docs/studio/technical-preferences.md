# Technical Preferences

<!-- Populated by $setup-engine. Updated as the user makes decisions throughout development. -->
<!-- Keep the headings and bullet labels stable. Repo skills read them directly. -->

This is the shared technical configuration sheet for the current project.
Update it whenever engine, platform, performance, or testing expectations change.

## Engine & Language

- **Engine**: [TO BE CONFIGURED - run $setup-engine]
- **Language**: [TO BE CONFIGURED]
- **Rendering**: [TO BE CONFIGURED]
- **Physics**: [TO BE CONFIGURED]

## Input & Platform

<!-- Read by UX, testing, and team orchestration workflows. -->

- **Target Platforms**: [TO BE CONFIGURED - e.g., PC, Console, Mobile, Web]
- **Input Methods**: [TO BE CONFIGURED - e.g., Keyboard/Mouse, Gamepad, Touch, Mixed]
- **Primary Input**: [TO BE CONFIGURED - the dominant input for this game]
- **Gamepad Support**: [TO BE CONFIGURED - Full / Partial / None]
- **Touch Support**: [TO BE CONFIGURED - Full / Partial / None]
- **Platform Notes**: [TO BE CONFIGURED - any platform-specific UX constraints]

## Naming Conventions

- **Classes**: [TO BE CONFIGURED]
- **Variables**: [TO BE CONFIGURED]
- **Signals/Events**: [TO BE CONFIGURED]
- **Files**: [TO BE CONFIGURED]
- **Scenes/Prefabs**: [TO BE CONFIGURED]
- **Constants**: [TO BE CONFIGURED]

## Performance Budgets

- **Target Framerate**: [TO BE CONFIGURED]
- **Frame Budget**: [TO BE CONFIGURED]
- **Draw Calls**: [TO BE CONFIGURED]
- **Memory Ceiling**: [TO BE CONFIGURED]

## Testing

- **Framework**: [TO BE CONFIGURED]
- **Minimum Coverage**: [TO BE CONFIGURED]
- **Required Tests**: Balance formulas, gameplay systems, networking (if applicable)

## Forbidden Patterns

<!-- Add patterns that should never appear in this project's codebase. -->
- [None configured yet -- add as architectural decisions are made]

## Allowed Libraries / Addons

<!-- Add approved third-party dependencies here as they become real project needs. -->
- [None configured yet -- add as dependencies are approved]

## Architecture Decisions Log

<!-- Quick reference linking to full ADRs in docs/architecture/. -->
- [No ADRs yet -- use $architecture-decision to create one]

## Engine Specialists

<!-- Written by $setup-engine when engine is configured. -->
<!-- Read by review, architecture, and team skills to select engine-aware agents. -->

- **Primary**: [TO BE CONFIGURED - run $setup-engine]
- **Language/Code Specialist**: [TO BE CONFIGURED]
- **Shader Specialist**: [TO BE CONFIGURED]
- **UI Specialist**: [TO BE CONFIGURED]
- **Additional Specialists**: [TO BE CONFIGURED]
- **Routing Notes**: [TO BE CONFIGURED]

### File Extension Routing

<!-- If a row stays unconfigured, fall back to Primary for that file type. -->

| File Extension / Type | Specialist to Spawn |
|-----------------------|---------------------|
| Game code (primary language) | [TO BE CONFIGURED] |
| Shader / material files | [TO BE CONFIGURED] |
| UI / screen files | [TO BE CONFIGURED] |
| Scene / prefab / level files | [TO BE CONFIGURED] |
| Native extension / plugin files | [TO BE CONFIGURED] |
| General architecture review | Primary |
