# Directory Structure

```text
/
├── AGENTS.md                    # Root operating guide for Codex
├── .agents/
│   └── skills/                  # Repo skills (one directory per workflow)
├── .codex/
│   ├── agents/                  # Custom agent definitions (.toml)
│   ├── hooks/                   # Hook scripts
│   ├── config.toml              # Shared project defaults for Codex
│   └── hooks.json               # Shared hook registrations
├── src/                         # Game source code (core, gameplay, ai, networking, ui, tools)
├── assets/                      # Game assets (art, audio, vfx, shaders, data)
├── design/                      # Game design docs (gdd, narrative, levels, balance, ux)
├── docs/                        # Technical docs, workflow guides, architecture notes
│   └── studio/                  # Framework docs and templates
├── tests/                       # Test suites (unit, integration, performance, playtest)
├── tools/                       # Build and pipeline tools
├── prototypes/                  # Throwaway prototypes, isolated from src/
└── production/                  # Sprint plans, milestones, release tracking
    ├── session-state/           # Lightweight resumable session notes
    └── session-logs/            # Hook-generated audit trail (gitignored)
```
