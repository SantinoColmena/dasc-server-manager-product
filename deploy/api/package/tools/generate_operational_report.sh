#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/dasc/api}"
CLIENT="${1:-DASC interno}"
PERIOD="${2:-$(date +%Y-%m)}"

PYTHON_BIN="${APP_DIR}/venv/bin/python"
REPORT_SCRIPT="${APP_DIR}/tools/generate_operational_report.py"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  echo "ERROR: no existe el Python del entorno virtual en ${PYTHON_BIN}"
  exit 1
fi

if [[ ! -f "${REPORT_SCRIPT}" ]]; then
  echo "ERROR: no existe el generador de informe en ${REPORT_SCRIPT}"
  exit 1
fi

cd "${APP_DIR}"

"${PYTHON_BIN}" "${REPORT_SCRIPT}" \
  --root "${APP_DIR}" \
  --client "${CLIENT}" \
  --period "${PERIOD}"
