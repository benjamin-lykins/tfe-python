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

echo "Creating teams..."
$PY teams.py create --name "python-contributor" --visibility secret
$PY teams.py create --name "python-reader" --visibility secret
$PY teams.py create --name "python-cicd" --visibility secret

echo "Creating projects..."
$PY projects.py create --name "python-alpha-project-nprd" --description "Non-prod project for python alpha"
$PY projects.py create --name "python-alpha-project-prod" --description "Prod project for python alpha"

echo "Creating variable sets and attaching to projects..."
$PY varset.py create --name "python-alpha-project-nprd-varset" --description "Variables for python-alpha-project-nprd"
$PY varset.py add-projects --varset-name "python-alpha-project-nprd-varset" --project-names "python-alpha-project-nprd"

$PY varset.py create --name "python-alpha-project-prod-varset" --description "Variables for python-alpha-project-prod"
$PY varset.py add-projects --varset-name "python-alpha-project-prod-varset" --project-names "python-alpha-project-prod"

echo "Done."
