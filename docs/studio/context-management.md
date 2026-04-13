# Context Management

The framework depends on durable project context instead of conversational memory alone.

## Core Idea

Store important project knowledge in files the studio can re-read:

- `AGENTS.md` for operating rules
- design docs for intent
- ADRs for technical decisions
- production docs for delivery state
- templates and runbooks for repeatable outputs

## Why This Matters

Codex sessions are powerful, but they should not become the only place where project state lives. Durable artifacts keep the studio reliable across sessions, agents, and contributors.

## Context Layers

1. root guidance: `AGENTS.md`
2. path guidance: nested `AGENTS.md`
3. workflow guidance: skills
4. durable project artifacts: design, architecture, production, testing
5. optional personal/global setup: `~/.codex`

## Good Context Hygiene

- read only what is relevant
- keep summaries short when handing work to another agent
- write stable decisions into files instead of re-explaining them every session
- prefer one authoritative artifact over duplicate summaries in several places

## When to Create New Context

Create or update a durable artifact when:

- the decision will matter again later
- another discipline depends on it
- a future gate or release review will need it
- the repo already has a template for that artifact
