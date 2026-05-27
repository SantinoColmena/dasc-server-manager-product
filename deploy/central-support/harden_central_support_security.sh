#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="${SERVICE_NAME:-dasc-central-support}"
SERVICE_FILE="${SERVICE_FILE:-/etc/systemd/system/${SERVICE_NAME}.service}"
APP_DIR="${APP_DIR:-/opt/dasc/central-support}"
CONFIG_FILE="${CONFIG_FILE:-${APP_DIR}/config.env}"

if [ "$(id -u)" -ne 0 ]; then
  echo "ERROR: ejecuta este script con sudo."
  exit 1
fi

echo "==> R-052F - Endureciendo DASC Central Support"

if [ ! -f "$SERVICE_FILE" ]; then
  echo "ERROR: no existe $SERVICE_FILE"
  exit 1
fi

if [ ! -d "$APP_DIR" ]; then
  echo "ERROR: no existe $APP_DIR"
  exit 1
fi

if [ ! -f "$CONFIG_FILE" ]; then
  echo "ERROR: no existe $CONFIG_FILE"
  exit 1
fi

STAMP="$(date +%Y%m%d-%H%M%S)"

echo "==> Backup unidad systemd"
cp -a "$SERVICE_FILE" "/root/${SERVICE_NAME}.service.bak.R-052F-${STAMP}"

echo "==> Parando ${SERVICE_NAME}"
systemctl stop "$SERVICE_NAME"

echo "==> Ajustando central-support para escuchar solo en 127.0.0.1"
sed -i -E 's|--host[[:space:]]+[^[:space:]]+|--host 127.0.0.1|g' "$SERVICE_FILE"

echo "==> Validando permisos config.env central"
chown root:root "$CONFIG_FILE"
chmod 600 "$CONFIG_FILE"

echo "==> Recargando systemd"
systemctl daemon-reload

echo "==> Arrancando ${SERVICE_NAME}"
systemctl start "$SERVICE_NAME"
systemctl enable "$SERVICE_NAME" >/dev/null

echo
echo "==> Estado servicio"
systemctl --no-pager --full status "$SERVICE_NAME" || true

echo
echo "==> Health local central"
curl -s http://127.0.0.1:8010/health | python3 -m json.tool

echo
echo "==> Panel central por Nginx"
curl -i -s http://127.0.0.1/ | head -n 12

echo
echo "==> Puertos"
ss -lntp | grep -E ':80|:8080|:8000|:8010|:22' || true

echo
echo "OK: hardening central-support aplicado."
echo "El backend central debe quedar interno en 127.0.0.1:8010."
