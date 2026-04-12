# Codex Code Game Studios Quick Start

## What You Get

This framework gives Codex a studio-shaped operating model:

- 49 custom agents in `.codex/agents/`
- 72 reusable skills in `.agents/skills/`
- nested `AGENTS.md` guides for path-specific standards
- project hooks wired through `.codex/hooks.json`

## 1. Open the Repo in Codex

```bash
cd your-game-repo
codex
```

## 2. Start With the Right Skill

Mention the workflow you want directly in your prompt. In Codex CLI you can use
`/skills`, type `$`, or mention the workflow by name:

- `$start` if this is a fresh project or you want guided routing
- `$help` if you want the next best step
- `$brainstorm` if you only have a rough concept
- `$project-stage-detect` if you already have code or docs
- `$setup-engine unity 6` or another engine/version if setup is already clear

Most heavy studio workflows are now **explicit-only** in `agents/openai.yaml`.
That keeps large authoring and orchestration skills from auto-triggering during
small requests, while lightweight review/analysis skills stay implicitly
available when their descriptions match.

## 3. Use the Studio Flow

The recommended order is:

1. concept
2. systems design
3. technical setup
4. pre-production
5. production
6. polish
7. release

The phase definitions and required artifacts live in:

- `docs/studio/workflow-catalog.yaml`
- `docs/WORKFLOW-GUIDE.md`
- `docs/studio/director-gates.md`

## 4. Know Where Things Go

```text
AGENTS.md                    # Root guide for Codex
.agents/skills/             # Repo skills
.codex/agents/              # Custom agents
.codex/config.toml          # Shared project defaults
.codex/hooks.json           # Shared hooks
design/gdd/                 # Game design docs
docs/architecture/          # ADRs and technical decisions
production/                 # Sprints, milestones, release plans
src/                        # Implementation
tests/                      # QA and automated checks
```

## 5. Prefer Skills Over Ad-Hoc Prompts

The fastest path to consistent output is to reuse the repo skills instead of
re-explaining the workflow every time. If you are about to ask for:

- a new game concept, use `$brainstorm`
- a system GDD, use `$design-system`
- an ADR, use `$architecture-decision`
- story generation, use `$create-epics` and `$create-stories`
- implementation against a story, use `$dev-story`
- release readiness, use `$gate-check` or `$release-checklist`

## 6. Customize Safely

- change repo-wide behavior in `AGENTS.md`
- change domain-specific standards in nested `AGENTS.md`
- change workflows in `.agents/skills/`
- change shared Codex defaults in `.codex/config.toml`
- change shared automation in `.codex/hooks.json`

For personal overrides, use `~/.codex/config.toml` and `~/.codex/hooks.json`
instead of editing shared project files.

## 7. Validate Codex Contracts

After changing repo skills or custom agents, run:

```bash
python3 scripts/sync_codex_metadata.py
python3 scripts/validate_codex_native.py
```

This keeps `agents/openai.yaml`, agent nicknames, sandbox declarations, and
project defaults aligned with the Codex-native contract the repo expects.
