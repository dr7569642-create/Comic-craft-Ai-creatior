#!/usr/bin/env bash
# Localhost startup script for ComicCraft (Linux / macOS / Unix)
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH="$DIR/backend:$PYTHONPATH"
export HOST="127.0.0.1"
export PORT="8000"
export ENVIRONMENT="development"

echo "=========================================="
echo "  Starting ComicCraft AI Studio on Localhost  "
echo "=========================================="

if [ -f "$DIR/.venv/bin/python" ]; then
    PYTHON_CMD="$DIR/.venv/bin/python"
elif [ -f "$DIR/venv/bin/python" ]; then
    PYTHON_CMD="$DIR/venv/bin/python"
else
    PYTHON_CMD="python3"
fi

echo "Running backend on http://127.0.0.1:8000 ..."
exec $PYTHON_CMD -m uvicorn app.main:app --app-dir "$DIR/backend" --host 127.0.0.1 --port 8000 --reload
