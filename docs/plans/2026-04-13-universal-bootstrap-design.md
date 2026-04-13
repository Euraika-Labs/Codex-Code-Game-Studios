# Universal Bootstrap Design

**Goal:** Replace the current two-step manual installer flow with one universal
bootstrap entrypoint that automatically picks the correct Codex home and, when
run inside a repository, bootstraps the full studio into that repository.

## Problem

The current hybrid installer works, but it still assumes the user understands:

- what `~/.codex` means
- when to run the global installer versus the repo installer
- how `CODEX_HOME` behaves
- how Windows and WSL differ

That is too much setup knowledge for a first-run experience.

## Design Principles

1. **One command should be enough**
   - The user should be able to run one bootstrap command and end up with the
     correct result for their environment.
2. **Respect explicit configuration**
   - If `CODEX_HOME` is already set, use it.
3. **Prefer shared Windows state from WSL when possible**
   - If running inside WSL and a Windows Codex home exists, prefer that so the
     user shares auth, config, and sessions with the Windows app.
4. **Fall back safely**
   - If the preferred shared home does not exist or is not writable, fall back
     to the local platform default.
5. **Do not overwrite user files silently**
   - Default to safe behavior and clear conflict reporting.

## Recommended Bootstrap Behavior

### Universal command

Add a new entrypoint:

- `global-pack/bin/bootstrap.py`

This command performs:

1. Resolve the source repo
2. Resolve the best Codex home for the current platform
3. Install or refresh the global pack into that Codex home
4. Detect whether the current working directory is inside a git repository
5. If yes, bootstrap the studio into that repo
6. Print a short summary of what happened and what to do next

### Automatic target selection

- If the current directory is inside a git repository, use the git root as the
  target repo automatically
- If not inside a repo, install only the global pack

### Codex home resolution order

1. `CODEX_HOME` if explicitly set
2. Native Windows:
   - `%USERPROFILE%\.codex`
3. WSL:
   - Prefer the Windows Codex home if it can be derived and already exists
   - Otherwise use Linux `~/.codex`
4. Linux and macOS:
   - `~/.codex`

### Why prefer the Windows home from WSL

OpenAI documents that WSL and native Windows use separate Codex homes by
default, and that sharing them requires pointing WSL at the Windows Codex home.
For a beginner-friendly bootstrap, using the shared home when it already exists
is the least surprising behavior.

### First-run WSL fallback

If the Windows Codex home does not exist yet, the bootstrap should use Linux
`~/.codex`. That avoids creating a Windows-side Codex home unexpectedly from
inside WSL.

## User Experience

### Case 1: User runs the bootstrap in a normal folder

Result:

- global pack installed
- no repo changes made
- output says the studio was not bootstrapped into a project because no git repo
  was detected

### Case 2: User runs the bootstrap inside a git repo

Result:

- global pack installed
- repo-local studio layer installed into the git root
- output points them to `$start`, `$help`, or `$project-stage-detect`

### Case 3: User reruns the bootstrap later

Result:

- identical files are skipped
- changed files update cleanly
- conflicts are reported if the target diverged and `--force` was not supplied

## CLI Surface

The bootstrap should support:

- `--dry-run`
- `--force`
- `--global-only`
- `--repo-only`
- `--source-repo`
- `--codex-home`
- `--target`

Defaults:

- no args = smart automatic behavior

## Wrapper Scripts

To make startup friendlier, add thin wrappers:

- `bootstrap.sh`
- `bootstrap.ps1`

These should call the Python bootstrap script using the platform’s common
Python launcher.

## Validation Strategy

The universal bootstrap is correct only if all of these pass:

1. Structural validation of the new bootstrap files
2. Automatic home detection unit-style checks for:
   - explicit `CODEX_HOME`
   - native Windows
   - WSL with existing Windows Codex home
   - WSL without Windows Codex home
   - Linux/macOS
3. End-to-end bootstrap in a temp directory outside git
4. End-to-end bootstrap in a temp git repository
5. The resulting repo passes existing Codex-native validation

## Risks

- Mistaking WSL for native Linux and splitting user state
- Creating a Windows-side Codex home from WSL when the user did not want that
- Overwriting an existing repo-local `.codex` or `AGENTS.md`
- Making output too opaque for troubleshooting

## Scope

In scope:

- one universal bootstrap
- automatic Codex-home detection
- automatic repo detection
- platform wrappers
- validation and docs updates

Out of scope:

- registry installation
- system-wide package installers
- modifying shell profiles automatically
