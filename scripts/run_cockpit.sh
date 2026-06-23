#!/usr/bin/env bash
# Run Q cockpit locally (without Docker)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export COCKPIT_HOST="${COCKPIT_HOST:-127.0.0.1}"
export COCKPIT_PORT="${COCKPIT_PORT:-8093}"
export BUILD_LOG_PATH="${BUILD_LOG_PATH:-$ROOT/data/build_log.jsonl}"
pip install -q pydantic 2>/dev/null || true
exec python3 Code/Node_1_Q_Frontend_Orchestrator/cockpit_server.py
