# Path-Specific Guides

Path-scoped behavior is no longer stored in `.claude/rules/`.

In the Codex-native layout, those instructions live in nested `AGENTS.md`
files placed near the directories they govern:

| Directory | Nested guide | Enforces |
| --- | --- | --- |
| `src/gameplay/` | `src/gameplay/AGENTS.md` | data-driven values, delta time discipline, no UI leakage |
| `src/core/` | `src/core/AGENTS.md` | zero-alloc hot paths, API stability, thread safety |
| `src/ai/` | `src/ai/AGENTS.md` | debuggability, tuning visibility, performance budgets |
| `src/networking/` | `src/networking/AGENTS.md` | server authority, message versioning, security |
| `src/ui/` | `src/ui/AGENTS.md` | localization-ready UI, accessibility, no game-state ownership |
| `design/gdd/` | `design/gdd/AGENTS.md` | required sections, formula format, edge-case coverage |
| `design/narrative/` | `design/narrative/AGENTS.md` | canon consistency, voice, lore discipline |
| `assets/data/` | `assets/data/AGENTS.md` | schema hygiene, naming conventions, data validation |
| `assets/shaders/` | `assets/shaders/AGENTS.md` | naming, performance targets, cross-platform concerns |
| `tests/` | `tests/AGENTS.md` | test naming, fixture discipline, evidence expectations |
| `prototypes/` | `prototypes/AGENTS.md` | relaxed standards, README requirements, hypothesis framing |

If you add a new high-signal directory with its own standards, create another
local `AGENTS.md` in that subtree instead of introducing a separate rules
system.
