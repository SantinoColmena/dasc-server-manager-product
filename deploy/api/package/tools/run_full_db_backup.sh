#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/dasc/api}"
PYTHON_BIN="${APP_DIR}/venv/bin/python"
BACKUP_SCRIPT="${APP_DIR}/tools/run_full_db_backup.py"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  echo "ERROR: no existe el Python del entorno virtual en ${PYTHON_BIN}"
  exit 1
fi

if [[ ! -f "${BACKUP_SCRIPT}" ]]; then
  echo "ERROR: no existe el script de backup en ${BACKUP_SCRIPT}"
  exit 1
fi

cd "${APP_DIR}"

"${PYTHON_BIN}" "${BACKUP_SCRIPT}" --root "${APP_DIR}" "$@"
