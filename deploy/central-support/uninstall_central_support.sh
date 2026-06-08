#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="vigex-central"
INSTALL_DIR="${INSTALL_DIR:-/opt/vigex/central-support}"

echo "==> Desinstalando Vigex Central"

if [ "$(id -u)" -ne 0 ]; then
  echo "ERROR: ejecuta este desinstalador con sudo."
  exit 1
fi

echo "==> Parando servicio si existe"
systemctl stop "${SERVICE_NAME}" >/dev/null 2>&1 || true
systemctl disable "${SERVICE_NAME}" >/dev/null 2>&1 || true

echo "==> Eliminando unidad systemd"
rm -f "/etc/systemd/system/${SERVICE_NAME}.service"

systemctl daemon-reload
systemctl reset-failed "${SERVICE_NAME}" >/dev/null 2>&1 || true

echo "==> Eliminando instalación"
rm -rf "${INSTALL_DIR}"

echo "OK: Vigex Central desinstalado."
