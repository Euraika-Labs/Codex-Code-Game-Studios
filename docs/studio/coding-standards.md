# Coding Standards

These standards apply to implementation work generated or reviewed through the framework.

## General Principles

- favor clarity over cleverness
- keep behavior close to the code that owns it
- make data flow easy to trace
- avoid hidden coupling between systems
- write for maintainers, not only for current speed

## Game-Project Expectations

- keep gameplay logic separate from presentation where the engine allows it
- make tuning values explicit and easy to change
- isolate platform- or engine-specific behavior behind clear boundaries
- document assumptions that can affect content, balance, or save compatibility

## Review Expectations

Good implementation output should include:

- a clear description of what changed
- enough tests or evidence to support the change
- references to the relevant story, design doc, or ADR when appropriate

## Stability Rules

- do not mix refactors with feature work unless the change genuinely requires it
- avoid broad incidental cleanup during deadline-sensitive work
- protect save data, networking behavior, and progression logic from silent breaking changes

## Collaboration Rules

- if a change conflicts with design, escalate instead of guessing
- if a change touches release risk, inform production and QA surfaces
- if a change affects player-facing behavior, update the relevant docs or notes
