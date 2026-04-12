#!/bin/bash
# Codex CLI Stop hook: validate changed Codex contract files in the worktree.
# This replaces the old Write/Edit matcher pattern because current Codex
# PostToolUse only emits Bash tool names.
#
# Exit behavior:
#   exit 0 = success or advisory warnings only
#
# Output:
#   Emits a JSON systemMessage on stdout when Codex-native validation fails.

find_python() {
    for cmd in python3 python py; do
        if command -v "$cmd" >/dev/null 2>&1; then
            echo "$cmd"
            return 0
        fi
    done
    return 1
}

emit_system_message() {
    local message="$1"

    if command -v python3 >/dev/null 2>&1; then
        python3 - "$message" <<'PY'
import json
import sys

print(json.dumps({"systemMessage": sys.argv[1]}))
PY
        return 0
    fi

    if command -v python >/dev/null 2>&1; then
        python - "$message" <<'PY'
import json
import sys

print(json.dumps({"systemMessage": sys.argv[1]}))
PY
        return 0
    fi

    if command -v jq >/dev/null 2>&1; then
        jq -Rn --arg msg "$message" '{systemMessage: $msg}'
        return 0
    fi

    local escaped
    escaped=$(printf '%s' "$message" | sed 's/\\/\\\\/g; s/"/\\"/g; :a;N;$!ba;s/\n/\\n/g')
    printf '{"systemMessage":"%s"}\n' "$escaped"
}

collect_changed_contracts() {
    {
        git diff --name-only --diff-filter=ACMR -- .agents/skills .codex/agents .codex/config.toml .codex/hooks.json scripts/sync_codex_metadata.py scripts/validate_codex_native.py 2>/dev/null
        git diff --cached --name-only --diff-filter=ACMR -- .agents/skills .codex/agents .codex/config.toml .codex/hooks.json scripts/sync_codex_metadata.py scripts/validate_codex_native.py 2>/dev/null
        git ls-files --others --exclude-standard -- .agents/skills .codex/agents .codex/config.toml .codex/hooks.json scripts/sync_codex_metadata.py scripts/validate_codex_native.py 2>/dev/null
    } | sed '/^$/d' | sort -u
}

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    exit 0
fi

cd "$REPO_ROOT" || exit 0

CHANGED_CONTRACTS=$(collect_changed_contracts)
if [ -z "$CHANGED_CONTRACTS" ]; then
    exit 0
fi

PYTHON_CMD=$(find_python || true)
if [ -z "$PYTHON_CMD" ]; then
    emit_system_message "Codex-native contract files changed, but no Python runtime was found for scripts/validate_codex_native.py."
    exit 0
fi

OUTPUT=$("$PYTHON_CMD" scripts/validate_codex_native.py 2>&1)
STATUS=$?

if [ "$STATUS" -eq 0 ]; then
    exit 0
fi

SYNC_HINT=""
if echo "$CHANGED_CONTRACTS" | grep -qE '^\.agents/skills/'; then
    SYNC_HINT="\nRun: python3 scripts/sync_codex_metadata.py"
fi

MESSAGE="Codex-native validation is failing for the current worktree.\n$OUTPUT$SYNC_HINT\nRun: python3 scripts/validate_codex_native.py"
emit_system_message "$MESSAGE"

exit 0
