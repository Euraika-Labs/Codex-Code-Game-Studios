# Hybrid Global Installer Design

**Goal:** Make Codex Code Game Studios usable globally through a small self-contained user-level pack plus a repo installer that can bootstrap the full studio into any target repository.

## Problem

The current studio is intentionally project-scoped. Most workflows assume repo-local
artifacts such as `AGENTS.md`, `.agents/skills`, `.codex/agents`,
`docs/studio/templates`, `design/`, and `production/`. That makes the studio
excellent inside a prepared repo, but not directly reusable from `~/.codex`
across arbitrary repositories.

OpenAI's current Codex model supports both project-scoped and user-scoped
customization:

- Global skills belong in `~/.codex/skills`
- Global custom agents belong in `~/.codex/agents`
- Project skills belong in `.agents/skills`
- Project custom agents belong in `.codex/agents`

That means a correct "global" solution should not move the entire studio into
`~/.codex`. Instead it should separate truly global capabilities from
repo-coupled workflows.

## Recommended Architecture

### 1. Global bootstrap pack

Add a new repo-managed distribution layer that can be installed into the user's
Codex home:

- `global-pack/skills/`
- `global-pack/agents/`
- `global-pack/templates/`
- `global-pack/bin/`

This pack contains only self-contained capabilities that make sense everywhere:

- studio discovery / help
- repo bootstrap / install
- repo audit / adopt
- studio sync / update
- lightweight orchestration helpers that do not require project-local templates

These assets should be installable into:

- `~/.codex/skills`
- `~/.codex/agents`

### 2. Repo installer

Provide a supported installer path that can copy or sync the full studio layer
into any target repository. The installer should be callable both from the
command line and from a global skill.

The installer will provision:

- `AGENTS.md`
- `.agents/`
- `.codex/`
- `docs/studio/`
- optional starter folders such as `design/`, `production/`, `backlog/`,
  `qa/`, and `build/`

The installer must support:

- first-time install into an existing repo
- update / sync against a newer studio version
- dry-run preview
- selective modes if needed later

### 3. Clear boundary between global and project workflows

The global pack should not pretend that all existing skills are safe everywhere.
Instead:

- global skills perform discovery, setup, audit, and installation
- project workflows stay repo-local after installation
- docs explain this boundary explicitly

This keeps the current studio design intact while still delivering an "available
everywhere" experience.

## User Experience

### Flow A: Enable the studio in an existing repo

1. User starts Codex in any git repo.
2. Codex can invoke a global installer skill from `~/.codex/skills`.
3. The skill runs an installer script from the managed global pack.
4. The script copies or syncs the studio layer into that repo.
5. From that point on, the repo-local skills and agents load normally.

### Flow B: Keep the global pack updated

1. User runs a global sync command or asks Codex to update the global pack.
2. Installer refreshes `~/.codex/skills` and `~/.codex/agents` from this repo's
   `global-pack/` source.
3. Validation confirms that global assets remain parseable and discoverable.

## Components

### Source assets in the repo

- `global-pack/skills/install-studio/`
- `global-pack/skills/adopt-studio/`
- `global-pack/skills/studio-help/`
- `global-pack/agents/studio-bootstrapper.toml`
- `global-pack/bin/install_global_pack.py`
- `global-pack/bin/install_repo_studio.py`

### Validation and maintenance

- Extend `scripts/validate_codex_native.py`
- Verify global-pack file integrity
- Verify generated target layout contracts
- Add scenario coverage for install and sync flows

### Documentation

- Update `README.md` with global install and repo bootstrap instructions
- Add a dedicated guide under `docs/studio/global-install.md`
- Clarify the difference between `~/.codex/*` and repo-local `.codex/*`

## Design Decisions

### Why not move everything into `~/.codex`

Because many current skills depend on project files and templates. Forcing all
84 skills into a global-only model would require a large refactor, duplicate
templates, and a riskier maintenance story.

### Why keep a repo installer

Because the existing studio is already optimized around a project root. An
installer preserves those assumptions while making setup fast and repeatable.

### Why keep the global pack small

Because only self-contained capabilities should be global. This reduces broken
invocations, makes updates safer, and keeps the mental model simple.

## Validation Strategy

We should consider the work complete only if all of these pass:

1. Structural validation of the new `global-pack/` tree
2. Install the global pack into a throwaway Codex home
3. Confirm Codex discovers the installed global skills and agents
4. Install the studio into a throwaway git repo
5. Confirm the installed repo passes `scripts/validate_codex_native.py`
6. Confirm at least one global bootstrap scenario and one installed repo
   scenario run successfully

## Risks

- Drift between the repo source and the installed global pack
- Copying repo-only assets into places where they do not belong
- Overwriting user-managed `~/.codex` assets unexpectedly
- Making the installer too clever before the first version proves useful

## First Version Scope

The first version should intentionally stay narrow:

- install a curated global pack
- install the full studio into an existing repo
- support `--dry-run`
- support idempotent reruns
- document exactly what gets copied

Out of scope for the first version:

- bidirectional merge logic
- selective per-skill installation
- automatic remote update channels
- Windows-only shell wrappers beyond the Python entrypoint
