# Fixture-Based Codex Scenarios

This directory holds higher-fidelity E2E tests for Codex-native workflows.

## Layout

- `states/<name>/overlay/` -- files copied into a throwaway repo copy before a scenario runs
- `scenarios/*.json` -- scenario definitions with turn-by-turn user prompts and file assertions

## Intended Use

Run the suite with:

```bash
python3 scripts/run_codex_scenarios.py
```

Use `--scenario <name>` to run a subset, or `--keep-workdirs` to inspect the
temporary repo copies after a failure.
