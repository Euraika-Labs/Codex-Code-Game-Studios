<p align="center">
  <h1 align="center">Codex Code Game Studios</h1>
  <p align="center">
    A Codex-native operating system for game teams, solo developers, and agent-driven production.
    <br />
    Skills, agents, hooks, templates, workflow gates, Steam publishing support, and a global bootstrap in one repo.
  </p>
</p>

<p align="center">
  <a href=".codex/agents"><img src="https://img.shields.io/badge/agents-50-blueviolet" alt="50 agents"></a>
  <a href=".agents/skills"><img src="https://img.shields.io/badge/skills-84-green" alt="84 skills"></a>
  <a href="docs/studio/hooks-reference.md"><img src="https://img.shields.io/badge/hook%20events-5-orange" alt="5 supported hooks"></a>
  <a href="docs/studio/steam-publishing-guide.md"><img src="https://img.shields.io/badge/steam-ready-yes-black" alt="Steam publishing support"></a>
  <a href="https://github.com/openai/codex"><img src="https://img.shields.io/badge/built%20for-Codex%20CLI-black" alt="Built for Codex CLI"></a>
</p>

---

## What This Repository Does

Codex Code Game Studios turns a normal Codex session into a structured game studio.
Instead of relying on ad-hoc prompts, the repo gives you a repeatable operating model:

- a root `AGENTS.md` and nested path guides
- reusable skills for concepting, design, engineering, QA, production, release, and Steamworks
- custom agents for directors, discipline leads, engine experts, and publishing specialists
- hook-based guardrails for validation and session hygiene
- templates and examples that keep artifacts consistent
- an optional global bootstrap so the installer flows are available from any repo

The result is a repo that can support the full lifecycle of a game project:

1. concept and systems design
2. technical setup and architecture
3. sprint planning and implementation
4. QA, polish, and gate reviews
5. launch preparation and Steam publishing

## What You Get

| Category | Count | Notes |
| --- | --- | --- |
| Custom agents | 50 | Leadership, leads, specialists, engine experts, release, and Steam publishing |
| Repo skills | 84 | Reusable workflows under `.agents/skills/` |
| Global pack | 3 skills + 1 agent | Lightweight install/discovery layer for `~/.codex` |
| Hooks | 5 supported events | `SessionStart`, `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop` |
| Templates | 35+ | Design, architecture, QA, production, release, and Steam artifacts |
| Engine references | 3 engines | Godot, Unity, and Unreal guidance for setup and implementation |

## Repository Layout

```text
/
├── AGENTS.md
├── .agents/skills/
├── .codex/agents/
├── .codex/hooks/
├── .codex/config.toml
├── .codex/hooks.json
├── docs/
│   ├── WORKFLOW-GUIDE.md
│   ├── studio/
│   ├── examples/
│   └── engine-reference/
├── design/
├── src/
├── assets/
├── tests/
├── prototypes/
├── production/
└── global-pack/
```

Use the repo as a project template, a studio layer inside an existing game repo, or a source repository for the global installer.

## Fast Start

### 1. Install Codex CLI

```bash
npm install -g @openai/codex
```

### 2. Clone the repo into a normal working directory

```bash
git clone https://github.com/Euraika-Labs/Codex-Code-Game-Studios.git my-game-studio
cd my-game-studio
```

Do not clone the entire repository directly into `~/.codex`. Project-local content and global Codex home content are separate concerns.

### 3. Start Codex in the repo

```bash
codex
```

### 4. Use a skill as the entry point

Start with one of these:

- `$start` for guided routing
- `$help` for the next recommended action
- `$brainstorm` for concept discovery
- `$project-stage-detect` for an existing project
- `$setup-engine godot 4.6` or the engine/version you already chose

The short onboarding route lives in [docs/studio/quick-start.md](docs/studio/quick-start.md).

## Global Installation

This repo ships a hybrid installation model:

- a small global pack in `~/.codex`
- the full studio installed into each target game repo

The recommended path is the universal bootstrap.

### macOS, Linux, and WSL

```bash
./bootstrap.sh
```

### Windows PowerShell

```powershell
.ootstrap.ps1
```

### Direct Python fallback

```bash
python3 global-pack/bin/bootstrap.py
```

The bootstrap automatically:

- resolves the correct Codex home for the current platform
- installs or refreshes the global installer pack
- bootstraps the full studio into the current git repo when appropriate

Full instructions: [docs/studio/global-install.md](docs/studio/global-install.md)

## Recommended Workflow

The studio works best when you follow the phase model defined in [docs/WORKFLOW-GUIDE.md](docs/WORKFLOW-GUIDE.md):

1. Concept
2. Systems Design
3. Technical Setup
4. Pre-Production
5. Production
6. Polish
7. Release

Typical command flow for a brand-new game:

1. `$start`
2. `$brainstorm`
3. `$setup-engine`
4. `$map-systems`
5. `$design-system`
6. `$create-architecture`
7. `$create-epics`
8. `$create-stories`
9. `$dev-story`
10. `$gate-check`

Typical command flow for an existing game repo:

1. run the bootstrap inside the repo
2. `$project-stage-detect`
3. `$adopt`
4. `$help`
5. continue from the recommended phase

## Steam Publishing

Steamworks is a first-class part of the repo, not an afterthought. The Steam pack covers:

- base game release planning
- Coming Soon timing
- store assets and copy
- review-readiness
- demo and playtest strategy
- Early Access planning
- DLC and soundtrack releases
- pricing, bundles, and launch operations
- Steam Deck readiness

Start with `$steam-publish-plan`, then branch into the relevant release variants.
Reference guide: [docs/studio/steam-publishing-guide.md](docs/studio/steam-publishing-guide.md)

## Core Docs Map

| Need | Start Here |
| --- | --- |
| Quick onboarding | [docs/studio/quick-start.md](docs/studio/quick-start.md) |
| Full operating model | [docs/WORKFLOW-GUIDE.md](docs/WORKFLOW-GUIDE.md) |
| Repo layout | [docs/studio/directory-structure.md](docs/studio/directory-structure.md) |
| Skills catalog | [docs/studio/skills-reference.md](docs/studio/skills-reference.md) |
| Agent map | [docs/studio/agent-roster.md](docs/studio/agent-roster.md) |
| Coordination rules | [docs/studio/coordination-rules.md](docs/studio/coordination-rules.md) |
| Global install | [docs/studio/global-install.md](docs/studio/global-install.md) |
| Hook behavior | [docs/studio/hooks-reference.md](docs/studio/hooks-reference.md) |
| Upgrade path | [UPGRADING.md](UPGRADING.md) |
| Templates | [docs/studio/templates/](docs/studio/templates/) |
| Examples | [docs/examples/README.md](docs/examples/README.md) |

## Validation and Maintenance

After changing shared skills, agents, docs, or install flows, run:

```bash
python3 scripts/sync_codex_metadata.py
python3 scripts/validate_codex_native.py
python3 scripts/test_hybrid_global_install.py
```

If you changed workflow coverage, scenario setup, or release docs, also run:

```bash
python3 scripts/build_workflow_matrix.py
python3 scripts/run_codex_scenarios.py --list
```

## Who This Is For

This repo is designed for:

- solo developers who want a disciplined studio workflow
- small teams that want shared AI-assisted process without inventing it from scratch
- technical leads who want Codex-native agents, skills, and hooks with real repo structure
- teams shipping to Steam that want release flows tied to the rest of development

## License

MIT. See [LICENSE](LICENSE).
