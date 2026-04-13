# Hook Input Schemas

This file summarizes the payload shapes the repo expects from the current Codex hook events.

## SessionStart

Session-start hooks should be prepared to handle startup and resume contexts.

Typical needs:

- detect repo root
- summarize branch and recent commit state
- avoid assumptions about a specific shell or editor

## PreToolUse and PostToolUse

In the current Codex runtime, repo hook matchers should assume the emitted tool surface they are written for and avoid no-op regex patterns.

Typical needs:

- identify the invoked tool or shell command when available
- short-circuit safely when the payload does not contain the expected fields
- avoid destructive behavior inside hook scripts

## UserPromptSubmit

Use this event for light prompt-time validation or logging only.

## Stop

Treat stop as a turn-level checkpoint, not a session archive event.

Typical uses:

- validate changed repo artifacts
- summarize end-of-turn warnings
- trigger lightweight maintenance checks
