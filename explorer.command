#!/bin/bash
# Trajectory Explorer — doble click para regenerar y abrir el visor de corridas
cd "$(dirname "$0")"
PY=.venv/bin/python; [ -x "$PY" ] || PY=python3
"$PY" scripts/explorer.py
