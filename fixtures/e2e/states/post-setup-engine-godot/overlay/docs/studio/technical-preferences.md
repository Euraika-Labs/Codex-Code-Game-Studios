# Technical Preferences

<!-- Populated by $setup-engine. Updated as the user makes decisions throughout development. -->
<!-- All agents reference this file for project-specific standards and conventions. -->

## Engine & Language

- **Engine**: Godot 4.6
- **Language**: GDScript
- **Rendering**: Forward+
- **Physics**: Godot Physics

## Input & Platform

- **Target Platforms**: PC
- **Input Methods**: Keyboard/Mouse
- **Primary Input**: Keyboard/Mouse
- **Gamepad Support**: None
- **Touch Support**: None
- **Platform Notes**: Desktop-first development target

## Naming Conventions

- **Classes**: PascalCase
- **Variables**: snake_case
- **Signals/Events**: snake_case
- **Files**: snake_case
- **Scenes/Prefabs**: PascalCase
- **Constants**: SCREAMING_SNAKE_CASE

## Performance Budgets

- **Target Framerate**: 60 FPS
- **Frame Budget**: 16.6 ms
- **Draw Calls**: < 1000
- **Memory Ceiling**: 2 GB

## Testing

- **Framework**: GdUnit4
- **Minimum Coverage**: 80%
- **Required Tests**: Balance formulas, gameplay systems, networking (if applicable)

## Forbidden Patterns

- [None configured yet -- add as architectural decisions are made]

## Allowed Libraries / Addons

- [None configured yet -- add as dependencies are approved]

## Architecture Decisions Log

- [No ADRs yet -- use $architecture-decision to create one]

## Engine Specialists

- **Primary**: godot-specialist
- **Language/Code Specialist**: godot-gdscript-specialist
- **Shader Specialist**: godot-shader-specialist
- **UI Specialist**: godot-specialist
- **Additional Specialists**: godot-csharp-specialist, godot-gdextension-specialist
- **Routing Notes**: Prefer Godot specialists for all engine-facing work.

### File Extension Routing

| File Extension / Type | Specialist to Spawn |
|-----------------------|---------------------|
| Game code (primary language) | godot-gdscript-specialist |
| Shader / material files | godot-shader-specialist |
| UI / screen files | godot-specialist |
| Scene / prefab / level files | godot-specialist |
| Native extension / plugin files | godot-gdextension-specialist |
| General architecture review | Primary |
