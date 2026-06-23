#!/usr/bin/env bash
# Crimson OS — local intranet bootstrap (Linux/macOS)
# Usage: ./scripts/startup.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -d Agent_Bridge ]]; then
  echo "ERROR: Agent_Bridge not found at $ROOT/Agent_Bridge" >&2
  exit 1
fi

if docker ps -a --format '{{.Names}}' | grep -qx crimson-intranet; then
  echo "Removing existing crimson-intranet container..."
  docker rm -f crimson-intranet >/dev/null 2>&1 || true
fi

echo "Starting Agent_Bridge intranet on http://127.0.0.1:8092 ..."
echo "Starting Q cockpit on http://127.0.0.1:8093 ..."
docker compose up -d intranet cockpit

echo "OK: Intranet + cockpit live."
echo "Health: ./scripts/health_check.sh"
echo "First Ping: http://127.0.0.1:8092/"
