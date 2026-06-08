#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="vigex-central-retry"
TIMER_NAME="vigex-central-retry"
APP_DIR="${APP_DIR:-/opt/vigex/api}"
INSTALLED_SCRIPT="${APP_DIR}/scripts/retry_central_pending.py"

echo "==> Desinstalando timer de reintento central Vigex"

if [ "$(id -u)" -ne 0 ]; then
  echo "ERROR: ejecuta este desinstalador con sudo."
  exit 1
fi

systemctl stop "${TIMER_NAME}.timer" >/dev/null 2>&1 || true
systemctl disable "${TIMER_NAME}.timer" >/dev/null 2>&1 || true
systemctl stop "${SERVICE_NAME}.service" >/dev/null 2>&1 || true

rm -f "/etc/systemd/system/${TIMER_NAME}.timer"
rm -f "/etc/systemd/system/${SERVICE_NAME}.service"
rm -f "${INSTALLED_SCRIPT}"

systemctl daemon-reload
systemctl reset-failed "${SERVICE_NAME}.service" >/dev/null 2>&1 || true
systemctl reset-failed "${TIMER_NAME}.timer" >/dev/null 2>&1 || true

echo "OK: timer de reintento central desinstalado."
