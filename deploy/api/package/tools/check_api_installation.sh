#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/vigex/api}"
SERVICE_NAME="${SERVICE_NAME:-vigex-api}"
CLIENT="${1:-Vigex validacion}"
PERIOD="${2:-$(date +%Y-%m)}"

REPORT_DIR="${APP_DIR}/reports"
TS="$(date +%Y%m%d-%H%M%S)"
REPORT_FILE="${REPORT_DIR}/validacion_instalacion_api_${TS}.md"

OK_COUNT=0
FAIL_COUNT=0

mkdir -p "${REPORT_DIR}" 2>/dev/null || true

add_line() {
  echo "$1" >> "${REPORT_FILE}"
}

check_ok() {
  OK_COUNT=$((OK_COUNT + 1))
  add_line "| OK | $1 | $2 |"
}

check_fail() {
  FAIL_COUNT=$((FAIL_COUNT + 1))
  add_line "| FALTA | $1 | $2 |"
}

check_path() {
  local name="$1"
  local path="$2"

  if [[ -e "${path}" ]]; then
    check_ok "${name}" "${path}"
  else
    check_fail "${name}" "${path}"
  fi
}

check_executable() {
  local name="$1"
  local path="$2"

  if [[ -x "${path}" ]]; then
    check_ok "${name}" "${path}"
  else
    check_fail "${name}" "${path}"
  fi
}

check_command() {
  local name="$1"
  local command="$2"

  if bash -c "${command}" >/tmp/vigex_validation_check.out 2>/tmp/vigex_validation_check.err; then
    check_ok "${name}" "Comando correcto: ${command}"
  else
    local err
    err="$(cat /tmp/vigex_validation_check.err 2>/dev/null | head -n 3 | tr '\n' ' ')"
    check_fail "${name}" "Comando fallido: ${command}. ${err}"
  fi
}

cat > "${REPORT_FILE}" <<EOF
# Validación post-instalación API Vigex

## Datos generales

| Campo | Valor |
|---|---|
| Fecha | $(date '+%Y-%m-%d %H:%M:%S') |
| APP_DIR | ${APP_DIR} |
| Servicio | ${SERVICE_NAME} |
| Cliente / entorno | ${CLIENT} |
| Periodo | ${PERIOD} |

## Comprobaciones

| Estado | Comprobación | Detalle |
|---|---|---|
EOF

check_path "Directorio de instalación" "${APP_DIR}"
check_path "main.py" "${APP_DIR}/main.py"
check_path "requirements.txt" "${APP_DIR}/requirements.txt"
check_path "config.env" "${APP_DIR}/config.env"
check_path "config.env.example" "${APP_DIR}/config.env.example"
check_path "Directorio data" "${APP_DIR}/data"
check_path "Directorio reports" "${APP_DIR}/reports"
check_path "Directorio tools" "${APP_DIR}/tools"
check_path "Entorno virtual" "${APP_DIR}/venv"
check_executable "Python del entorno virtual" "${APP_DIR}/venv/bin/python"

check_path "Generador informe operativo Python" "${APP_DIR}/tools/generate_operational_report.py"
check_executable "Wrapper informe operativo" "${APP_DIR}/tools/generate_operational_report.sh"
check_executable "Validador post-instalación" "${APP_DIR}/tools/check_api_installation.sh"

check_command "Servicio systemd existe" "systemctl status ${SERVICE_NAME} --no-pager"
check_command "Servicio systemd activo" "systemctl is-active --quiet ${SERVICE_NAME}"
check_command "Puerto local API responde" "curl -fsSI http://127.0.0.1:8000"

if [[ -x "${APP_DIR}/tools/generate_operational_report.sh" ]]; then
  check_command "Generar informe operativo" "APP_DIR='${APP_DIR}' '${APP_DIR}/tools/generate_operational_report.sh' '${CLIENT}' '${PERIOD}'"
else
  check_fail "Generar informe operativo" "No se puede ejecutar porque falta el wrapper."
fi

add_line ""
add_line "## Resumen"
add_line ""
add_line "| Campo | Valor |"
add_line "|---|---|"
add_line "| Correctas | ${OK_COUNT} |"
add_line "| Fallidas | ${FAIL_COUNT} |"
add_line ""

if [[ "${FAIL_COUNT}" -eq 0 ]]; then
  add_line "## Resultado"
  add_line ""
  add_line "Resultado: OK."
  add_line ""
  add_line "La instalación API supera las comprobaciones mínimas post-instalación."
else
  add_line "## Resultado"
  add_line ""
  add_line "Resultado: REVISAR."
  add_line ""
  add_line "La instalación API requiere correcciones antes de considerarse preparada."
fi

echo "Validación generada en: ${REPORT_FILE}"

if [[ "${FAIL_COUNT}" -gt 0 ]]; then
  exit 1
fi
