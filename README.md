# Codex Code Game Studios

Codex Code Game Studios is a Codex-native operating system for game development.
It gives you a structured studio layer on top of a normal repository:

- root and nested `AGENTS.md` guidance
- reusable repo skills in `.agents/skills/`
- custom agents in `.codex/agents/`
- hooks, validation gates, and workflow coverage
- templates for design, architecture, QA, release, and Steam publishing
- a hybrid global installer so Codex can help from any repo

This repository is designed to help you run a game project from concept through launch without rebuilding process from scratch every time.

## What This Repo Is

Use this repository in one of three ways:

1. as the root of a brand-new game project
2. as a studio layer installed into an existing game repository
3. as the source of a global Codex bootstrap for discovery and repo installation

If you want the shortest explanation:

- the full studio belongs inside a project repo
- the small global pack belongs in your Codex home
- the universal bootstrap sets both up correctly

## What You Get

| Category | Count | Notes |
| --- | --- | --- |
| Repo skills | 84 | Game design, engineering, QA, production, release, Steamworks, and adoption workflows |
| Custom agents | 50 | Directors, leads, specialists, engine experts, release, and Steam publishing roles |
| Global pack | 3 skills + 1 agent | Lightweight install and discovery layer for `~/.codex` |
| Hook events | 5 | `SessionStart`, `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop` |
| Templates | 35+ | Design, architecture, test, production, release, and Steam artifacts |
| Engine references | 3 engines | Godot, Unity, and Unreal |

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

## Choose Your Setup

### Option A: Start a New Game Project

Use this when you want this repository to be the actual root of your game project.

```bash
git clone https://github.com/Euraika-Labs/Codex-Code-Game-Studios.git my-game
cd my-game
```

Then install Codex CLI if needed:

```bash
npm install -g @openai/codex
```

Then run the bootstrap:

```bash
./bootstrap.sh
```

Or on Windows PowerShell:

```powershell
.\bootstrap.ps1
```

Then start Codex:

```bash
codex
```

Recommended first command:

- `$start`

### Option B: Add the Studio to an Existing Game Repo

Use this when you already have a repository with code, assets, docs, or prototypes.

From anywhere:

```bash
python3 /path/to/Codex-Code-Game-Studios/global-pack/bin/bootstrap.py --target /path/to/existing-game-repo
```

Or from inside this repository:

```bash
./bootstrap.sh --target /path/to/existing-game-repo
```

Or on Windows PowerShell:

```powershell
.\bootstrap.ps1 --target C:\path\to\existing-game-repo
```

After installation, open Codex in the target repo and start with:

1. `$project-stage-detect`
2. `$adopt`
3. `$help`

### Option C: Install Only the Global Helpers

Use this when you want Codex to know the installer and discovery skills globally, without installing the full studio into the current repo yet.

```bash
./bootstrap.sh --global-only
```

Or on Windows PowerShell:

```powershell
.\bootstrap.ps1 --global-only
```

This installs the lightweight global pack into your Codex home and makes the installer flows available from other repositories.

## Universal Bootstrap

The universal bootstrap is the recommended installation path.

You can run it from the repo:

```bash
./bootstrap.sh
```

Or with Python directly:

```bash
python3 global-pack/bin/bootstrap.py
```

The bootstrap automatically:

1. resolves the correct Codex home for the current platform
2. installs or refreshes the global pack
3. installs the full studio into the current git repo when appropriate

### Platform Resolution

The bootstrap resolves Codex home in this order:

1. `CODEX_HOME` if already set
2. native Windows: `%USERPROFILE%\\.codex`
3. WSL: shared Windows Codex home if it already exists, otherwise Linux `~/.codex`
4. Linux and macOS: `~/.codex`

This means users do not need to manually decide where the global Codex home should live.

### What Gets Installed Globally

The global pack installs:

- `~/.codex/skills/studio-help`
- `~/.codex/skills/install-studio`
- `~/.codex/skills/adopt-studio`
- `~/.codex/agents/studio-bootstrapper.toml`
- `~/.codex/bin/bootstrap.py`
- `~/.codex/bin/install_repo_studio.py`
- `~/.codex/bin/install_global_pack.py`

### What Gets Installed Into a Repo

When the bootstrap targets a repository, it installs the full studio layer:

- `AGENTS.md`
- `.agents/`
- `.codex/`
- `docs/studio/`
- nested `AGENTS.md` path guides
- starter directories such as `design/`, `production/`, `src/`, `tests/`, and `build/`

## Do Not Install It This Way

Do not clone the whole repository directly into `~/.codex`.

That is the wrong shape for this framework because:

- the full studio expects project-local paths and artifacts
- the global pack is intentionally much smaller than the full repo
- the bootstrap already knows how to place each part in the correct location

If your goal is “make this available everywhere,” use the bootstrap instead of cloning into `~/.codex`.

## First Commands Inside Codex

Once you are inside a studio-enabled repo, these are the normal entry points:

- `$start`
  Use for guided routing when you are starting fresh or unsure where to begin.

- `$help`
  Use when the repo is already set up and you want the next best action.

- `$brainstorm`
  Use when the concept is rough or still undefined.

- `$project-stage-detect`
  Use when the repo already contains meaningful code, docs, prototypes, or planning.

- `$setup-engine <engine> <version>`
  Use when the engine choice is already known and you want to pin the project.

Examples:

```text
$start
$brainstorm cozy farming game with light automation
$project-stage-detect
$setup-engine godot 4.6
```

## Recommended Workflow

The studio follows the phase model in [docs/WORKFLOW-GUIDE.md](docs/WORKFLOW-GUIDE.md):

1. Concept
2. Systems Design
3. Technical Setup
4. Pre-Production
5. Production
6. Polish
7. Release

### Typical Flow for a New Game

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

### Typical Flow for an Existing Repo

1. run the bootstrap for that repo
2. `$project-stage-detect`
3. `$adopt`
4. `$help`
5. continue from the recommended phase

## Steam Publishing

Steamworks is a first-class workflow family in this repository.

The Steam pack covers:

- base game release planning
- Coming Soon timing
- store assets and copy
- review readiness
- demo and playtest strategy
- Early Access planning
- DLC and soundtrack releases
- pricing and bundle decisions
- launch operations
- Steam Deck readiness

Recommended starting command:

- `$steam-publish-plan`

Reference guide:

- [docs/studio/steam-publishing-guide.md](docs/studio/steam-publishing-guide.md)

## Core Documentation Map

| Need | Start Here |
| --- | --- |
| Quick onboarding | [docs/studio/quick-start.md](docs/studio/quick-start.md) |
| Full operating model | [docs/WORKFLOW-GUIDE.md](docs/WORKFLOW-GUIDE.md) |
| Global bootstrap and install | [docs/studio/global-install.md](docs/studio/global-install.md) |
| Repo layout | [docs/studio/directory-structure.md](docs/studio/directory-structure.md) |
| Skills catalog | [docs/studio/skills-reference.md](docs/studio/skills-reference.md) |
| Agent roster | [docs/studio/agent-roster.md](docs/studio/agent-roster.md) |
| Coordination rules | [docs/studio/coordination-rules.md](docs/studio/coordination-rules.md) |
| Hook behavior | [docs/studio/hooks-reference.md](docs/studio/hooks-reference.md) |
| Templates | [docs/studio/templates/](docs/studio/templates/) |
| Examples | [docs/examples/README.md](docs/examples/README.md) |
| Upgrade notes | [UPGRADING.md](UPGRADING.md) |

## Validation

If you change shared skills, agents, install flows, or docs, run:

```bash
python3 scripts/sync_codex_metadata.py
python3 scripts/validate_codex_native.py
python3 scripts/test_hybrid_global_install.py
```

If you change scenario fixtures, workflow coverage, or release behavior, also run:

```bash
python3 scripts/build_workflow_matrix.py
python3 scripts/run_codex_scenarios.py
```

## Who This Is For

This repository is a good fit for:

- solo developers who want a disciplined studio workflow
- small teams that want shared AI-assisted process inside a real repo
- technical leads who want Codex-native skills, agents, hooks, and validation
- teams shipping to Steam that want publishing flows connected to the rest of development

## License

MIT. See [LICENSE](LICENSE).
