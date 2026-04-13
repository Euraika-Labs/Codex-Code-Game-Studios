# Setup Requirements

These are the tools that make the framework fully usable. Missing optional tools should not break the repo, but they will reduce guardrails and convenience.

## Required

| Tool | Purpose | Install |
| --- | --- | --- |
| Git | version control and repo-aware workflows | [git-scm.com](https://git-scm.com/) |
| Codex CLI | the agent runtime for this framework | `npm install -g @openai/codex` |

## Recommended

| Tool | Used By | Purpose | Install |
| --- | --- | --- | --- |
| jq | hooks and lightweight JSON checks | fast JSON parsing in shell hooks | see platform commands below |
| Python 3 | validators, install tests, structured checks | repo validation and helper scripts | [python.org](https://www.python.org/) |
| Bash | hooks and bootstrap scripts | cross-platform shell execution | included on macOS/Linux, via Git Bash on Windows |

## jq Installation

### Windows

```bash
winget install jqlang.jq
choco install jq
scoop install jq
```

### macOS

```bash
brew install jq
```

### Linux

```bash
sudo apt install jq
sudo dnf install jq
sudo pacman -S jq
```

## Platform Notes

### Windows

- Git for Windows provides Git Bash, which is enough for the shared hook scripts.
- PowerShell users can run the universal bootstrap with `bootstrap.ps1`.
- If you also use WSL, decide whether you want a shared Codex home or separate ones.

### WSL

- WSL can share the Windows Codex home when that home already exists.
- The universal bootstrap handles that resolution automatically.
- For active coding, keep repositories in the Linux filesystem when possible.

### macOS and Linux

- Bash is available natively.
- Use the shell bootstrap directly.

## Verify the Toolchain

```bash
git --version
codex --version
bash --version
jq --version
python3 --version
```

## If Optional Tools Are Missing

| Missing Tool | Effect |
| --- | --- |
| jq | some shell-level validation becomes weaker or falls back to simpler checks |
| Python 3 | validator and install-test scripts cannot run |
| Both | the repo still functions, but shared validation is much weaker |

## Editors

The framework works with any editor, but the most common setups are:

- Codex desktop app
- terminal Codex CLI plus VS Code
- terminal Codex CLI plus Cursor
