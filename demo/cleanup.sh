#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$ROOT/.venv/bin/python"

if [[ ! -x "$PY" ]]; then
  echo "Python venv not found at $PY"
  echo "Run: python -m venv .venv && .venv/bin/python -m pip install -r requirements.txt"
  exit 1
fi

cd "$ROOT"

echo "Removing variable set project attachments..."
$PY varset.py remove-projects --varset-name "python-alpha-project-nprd-varset" --project-names "python-alpha-project-nprd" || true
$PY varset.py remove-projects --varset-name "python-alpha-project-prod-varset" --project-names "python-alpha-project-prod" || true

echo "Deleting variable sets..."
$PY varset.py delete --name "python-alpha-project-nprd-varset" || true
$PY varset.py delete --name "python-alpha-project-prod-varset" || true

echo "Deleting projects..."
$PY projects.py delete --name "python-alpha-project-nprd" || true
$PY projects.py delete --name "python-alpha-project-prod" || true

echo "Deleting teams..."
$PY teams.py delete --name "python-contributor" || true
$PY teams.py delete --name "python-reader" || true
$PY teams.py delete --name "python-cicd" || true

echo "Cleanup complete."
