#!/bin/bash
# SessionStart hook for Claude Code on the web.
# Installs Python (backend, via uv) and Node (frontend) dependencies so the
# app, linters and tests work in fresh remote containers. Synchronous.
set -euo pipefail

# Only run in remote (Claude Code on the web) sessions.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"

# Backend dependencies are managed with uv.
if ! command -v uv >/dev/null 2>&1; then
  echo "[session-start] Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

echo "[session-start] Syncing Python backend dependencies (uv sync)..."
uv sync

echo "[session-start] Installing frontend dependencies (npm install)..."
(cd frontend && npm install)

echo "[session-start] Done."
