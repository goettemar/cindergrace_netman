#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

# Setup venv if needed
if [[ ! -d "$VENV_DIR" ]]; then
  python3 -m venv "$VENV_DIR"
fi

# Install/update dependencies (as normal user)
"$VENV_DIR/bin/pip" install --upgrade pip -q
"$VENV_DIR/bin/pip" install -e "$ROOT_DIR" -q

echo "NetMan requires root privileges for traffic shaping."
echo "Starting UI with sudo..."
echo ""

# Start UI with sudo (keeps venv python path)
exec sudo "$VENV_DIR/bin/cindergrace-netman" ui
