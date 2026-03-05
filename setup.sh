#!/usr/bin/env bash
set -euo pipefail

VENV_DIR=".venv"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Error: '$PYTHON_BIN' not found. Install Python 3 or set PYTHON_BIN." >&2
  return 1 2>/dev/null || exit 1
fi

if [[ ! -d "$VENV_DIR" ]]; then
  echo "Creating virtual environment in $VENV_DIR..."
  "$PYTHON_BIN" -m venv "$VENV_DIR"
else
  echo "Virtual environment already exists at $VENV_DIR."
fi

echo "Installing dependencies from requirements.txt..."
"$VENV_DIR/bin/python" -m pip install --upgrade pip
"$VENV_DIR/bin/python" -m pip install -r requirements.txt

if [[ "${BASH_SOURCE[0]}" != "$0" ]]; then
  # Script is sourced: activate in current shell session.
  # shellcheck disable=SC1091
  source "$VENV_DIR/bin/activate"
  echo "Setup complete. Virtual environment is active."
else
  echo "Setup complete. To activate, run: source $VENV_DIR/bin/activate"
fi
