#!/bin/bash
# Codex CLI Stop hook: append a lightweight per-turn audit entry.
# Current Codex runtime fires Stop at turn scope, so keep this concise.

INPUT=$(cat)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SESSION_LOG_DIR="production/session-logs"
STATE_FILE="production/session-state/active.md"

mkdir -p "$SESSION_LOG_DIR" 2>/dev/null

if command -v jq >/dev/null 2>&1; then
    TURN_ID=$(echo "$INPUT" | jq -r '.turn_id // empty')
else
    TURN_ID=$(echo "$INPUT" | grep -oE '"turn_id"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/"turn_id"[[:space:]]*:[[:space:]]*"//;s/"$//')
fi

CURRENT_HEAD=$(git rev-parse --short HEAD 2>/dev/null)
MODIFIED_FILES=$(git status --short 2>/dev/null)

if [ -z "$TURN_ID" ] && [ -z "$CURRENT_HEAD" ] && [ -z "$MODIFIED_FILES" ] && [ ! -f "$STATE_FILE" ]; then
    exit 0
fi

{
    echo "## Turn Stop: $TIMESTAMP"
    if [ -n "$TURN_ID" ]; then
        echo "Turn: $TURN_ID"
    fi
    if [ -n "$CURRENT_HEAD" ]; then
        echo "Head: $CURRENT_HEAD"
    fi
    if [ -f "$STATE_FILE" ]; then
        echo "Session state file present: $STATE_FILE"
    fi
    if [ -n "$MODIFIED_FILES" ]; then
        echo "### Working Tree"
        echo "$MODIFIED_FILES"
    fi
    echo "---"
    echo ""
} >> "$SESSION_LOG_DIR/session-log.md" 2>/dev/null

exit 0
