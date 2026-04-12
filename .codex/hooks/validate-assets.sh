#!/bin/bash
# Codex CLI Stop hook: validate changed asset files in the worktree.
# This replaces the old Write/Edit matcher pattern because current Codex
# PostToolUse only emits Bash tool names.
#
# Exit behavior:
#   exit 0 = success or advisory warnings only
#
# Output:
#   Emits a JSON systemMessage on stdout when changed assets need attention.

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

collect_changed_assets() {
    {
        git diff --name-only --diff-filter=ACMR -- assets 2>/dev/null
        git diff --cached --name-only --diff-filter=ACMR -- assets 2>/dev/null
        git ls-files --others --exclude-standard -- assets 2>/dev/null
    } | sed '/^$/d' | sort -u
}

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    exit 0
fi

cd "$REPO_ROOT" || exit 0

CHANGED_ASSETS=$(collect_changed_assets)
if [ -z "$CHANGED_ASSETS" ]; then
    exit 0
fi

PYTHON_CMD=$(find_python || true)
WARNINGS=""
ERRORS=""

while IFS= read -r file; do
    [ -z "$file" ] && continue

    FILE_PATH=$(echo "$file" | sed 's|\\|/|g')
    if [ ! -e "$FILE_PATH" ]; then
        continue
    fi

    FILENAME=$(basename "$FILE_PATH")

    if echo "$FILENAME" | grep -qE '[A-Z[:space:]-]'; then
        WARNINGS="$WARNINGS\n- $FILE_PATH should use lowercase_with_underscores naming"
    fi

    if echo "$FILE_PATH" | grep -qE '^assets/data/.*\.json$'; then
        if [ -n "$PYTHON_CMD" ]; then
            if ! "$PYTHON_CMD" -m json.tool "$FILE_PATH" >/dev/null 2>&1; then
                ERRORS="$ERRORS\n- $FILE_PATH is not valid JSON"
            fi
        else
            WARNINGS="$WARNINGS\n- $FILE_PATH could not be JSON-validated because no Python runtime was found"
        fi
    fi
done <<< "$CHANGED_ASSETS"

if [ -z "$WARNINGS$ERRORS" ]; then
    exit 0
fi

MESSAGE="Asset checks found issues in changed worktree files."
if [ -n "$ERRORS" ]; then
    MESSAGE="$MESSAGE\nBlocking-on-commit issues:$ERRORS"
fi
if [ -n "$WARNINGS" ]; then
    MESSAGE="$MESSAGE\nWarnings:$WARNINGS"
fi
MESSAGE="$MESSAGE\nThe git commit hook will re-check these files before commit."

emit_system_message "$MESSAGE"

exit 0
