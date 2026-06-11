#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="vigex-central-retry"
TIMER_NAME="vigex-central-retry"
APP_DIR="${APP_DIR:-/opt/vigex/api}"
SOURCE_SCRIPT="${SOURCE_SCRIPT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/package/scripts" && pwd)/retry_central_pending.py}"
INSTALLED_SCRIPT="${APP_DIR}/scripts/retry_central_pending.py"
INTERVAL="${INTERVAL:-5min}"

echo "==> Instalando timer de reintento central Vigex"

if [ "$(id -u)" -ne 0 ]; then
  echo "ERROR: ejecuta este instalador con sudo."
  exit 1
fi

if [ ! -d "${APP_DIR}" ]; then
  echo "ERROR: no existe ${APP_DIR}. Instala primero vigex-api."
  exit 1
fi

if [ ! -x "${APP_DIR}/venv/bin/python" ]; then
  echo "ERROR: no existe ${APP_DIR}/venv/bin/python."
  exit 1
fi

if [ ! -f "${APP_DIR}/main.py" ]; then
  echo "ERROR: no existe ${APP_DIR}/main.py."
  exit 1
fi

if [ ! -f "${SOURCE_SCRIPT}" ]; then
  echo "ERROR: no existe script fuente ${SOURCE_SCRIPT}."
  exit 1
fi

echo "==> Copiando script"
mkdir -p "${APP_DIR}/scripts"
cp "${SOURCE_SCRIPT}" "${INSTALLED_SCRIPT}"
chmod 750 "${INSTALLED_SCRIPT}"
chown --reference="${APP_DIR}/main.py" "${INSTALLED_SCRIPT}" || true
chown --reference="${APP_DIR}/main.py" "${APP_DIR}/scripts" || true

API_USER="$(systemctl cat vigex-api 2>/dev/null | awk -F= '/^User=/{print $2; exit}' || true)"
API_GROUP="$(systemctl cat vigex-api 2>/dev/null | awk -F= '/^Group=/{print $2; exit}' || true)"

USER_LINE=""
GROUP_LINE=""

if [ -n "${API_USER}" ]; then
  USER_LINE="User=${API_USER}"
fi

if [ -n "${API_GROUP}" ]; then
  GROUP_LINE="Group=${API_GROUP}"
fi

echo "==> Creando servicio oneshot"
cat > "/etc/systemd/system/${SERVICE_NAME}.service" <<EOF
[Unit]
Description=Vigex automatic retry for central support pending tickets
After=network-online.target vigex-api.service
Wants=network-online.target

[Service]
Type=oneshot
${USER_LINE}
${GROUP_LINE}
WorkingDirectory=${APP_DIR}
EnvironmentFile=${APP_DIR}/config.env
Environment=VIGEX_CENTRAL_RETRY_LIMIT=50
ExecStart=${APP_DIR}/venv/bin/python ${INSTALLED_SCRIPT}
EOF

echo "==> Creando timer"
cat > "/etc/systemd/system/${TIMER_NAME}.timer" <<EOF
[Unit]
Description=Run Vigex central support retry periodically

[Timer]
OnBootSec=2min
OnUnitActiveSec=${INTERVAL}
Unit=${SERVICE_NAME}.service
Persistent=true

[Install]
WantedBy=timers.target
EOF

echo "==> Activando timer"
systemctl daemon-reload
systemctl enable "${TIMER_NAME}.timer"
systemctl restart "${TIMER_NAME}.timer"

echo
echo "==> Estado timer"
systemctl --no-pager --full status "${TIMER_NAME}.timer" || true

echo
echo "==> Proxima ejecucion"
systemctl list-timers "${TIMER_NAME}.timer" --no-pager || true

echo
echo "OK: timer de reintento central instalado."
echo "Servicio: ${SERVICE_NAME}.service"
echo "Timer: ${TIMER_NAME}.timer"
echo "Intervalo: ${INTERVAL}"
