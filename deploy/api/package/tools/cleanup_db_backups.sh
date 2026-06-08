#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/vigex/api}"
PYTHON_BIN="${APP_DIR}/venv/bin/python"
CLEANUP_SCRIPT="${APP_DIR}/tools/cleanup_db_backups.py"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  echo "ERROR: no existe el Python del entorno virtual en ${PYTHON_BIN}"
  exit 1
fi

if [[ ! -f "${CLEANUP_SCRIPT}" ]]; then
  echo "ERROR: no existe el script de limpieza en ${CLEANUP_SCRIPT}"
  exit 1
fi

cd "${APP_DIR}"

"${PYTHON_BIN}" "${CLEANUP_SCRIPT}" --root "${APP_DIR}" "$@"
