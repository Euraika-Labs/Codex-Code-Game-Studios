# Hooks Reference

This repo uses the current Codex hook surface for lightweight automation and validation.

## Supported Events

- `SessionStart`
- `PreToolUse`
- `PostToolUse`
- `UserPromptSubmit`
- `Stop`

Hook registration lives in `.codex/hooks.json`. Hook scripts live in `.codex/hooks/`.

## What Hooks Do in This Repo

- session start hooks provide lightweight repo context
- tool hooks validate or summarize safe runtime behavior where supported
- stop hooks run end-of-turn checks such as asset or skill validation

## Design Rules

- commands should resolve from the git root when they call repo-local scripts
- hook scripts should fail clearly and avoid silent broken matchers
- only supported Codex hook events should remain wired
- hooks should assist the workflow, not replace explicit skills or approvals

## Validation

The validator checks hook integrity through `scripts/validate_codex_native.py`.

Use it after any hook or config change.
