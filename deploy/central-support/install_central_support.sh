#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="dasc-central-support"
INSTALL_DIR="${INSTALL_DIR:-/opt/dasc/central-support}"
INSTALL_PARENT="${INSTALL_PARENT:-$(dirname "${INSTALL_DIR}")}"
APP_USER="${APP_USER:-dasc}"
APP_GROUP="${APP_GROUP:-dasc}"
APP_HOST="${APP_HOST:-0.0.0.0}"
APP_PORT="${APP_PORT:-8010}"
SOURCE_DIR="${SOURCE_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/package" && pwd)}"
ENV_FILE="${INSTALL_DIR}/config.env"

echo "==> Instalando DASC Central Support"

if [ "$(id -u)" -ne 0 ]; then
  echo "ERROR: ejecuta este instalador con sudo."
  exit 1
fi

echo "==> Instalando dependencias del sistema"
apt-get update
apt-get install -y python3 python3-venv python3-pip rsync curl

echo "==> Preparando usuario ${APP_USER}"
if ! id "${APP_USER}" >/dev/null 2>&1; then
  useradd --system --home /opt/dasc --shell /usr/sbin/nologin "${APP_USER}"
fi

echo "==> Creando directorios"
mkdir -p "${INSTALL_PARENT}"
chmod 755 "${INSTALL_PARENT}"
mkdir -p "${INSTALL_DIR}"
mkdir -p "${INSTALL_DIR}/data"

echo "==> Copiando aplicación desde ${SOURCE_DIR}"
rsync -a --delete \
  --exclude "venv" \
  --exclude "__pycache__" \
  --exclude "*.pyc" \
  --exclude "*.log" \
  --exclude "data/*.db" \
  "${SOURCE_DIR}/" "${INSTALL_DIR}/"

echo "==> Creando entorno virtual"
python3 -m venv "${INSTALL_DIR}/venv"
"${INSTALL_DIR}/venv/bin/python" -m pip install --upgrade pip
"${INSTALL_DIR}/venv/bin/pip" install -r "${INSTALL_DIR}/requirements.txt"

echo "==> Preparando config.env"
if [ ! -f "${ENV_FILE}" ]; then
  CENTRAL_SECRET="$(python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(48))
PY
)"

  cat > "${ENV_FILE}" <<EOF
# DASC Central Support
DASC_CENTRAL_AUTH_ENABLED=true
DASC_CENTRAL_SECRET_KEY=${CENTRAL_SECRET}

# Usuarios de laboratorio. Cambiar en despliegue real.
DASC_CENTRAL_ADMIN_USER=admin
DASC_CENTRAL_ADMIN_PASSWORD=admin
DASC_CENTRAL_TECH_USER=tecnico
DASC_CENTRAL_TECH_PASSWORD=tecnico

# Cliente demo para integración local-central
DASC_CENTRAL_DEMO_CLIENT_ID=cliente-demo-a
DASC_CENTRAL_DEMO_CLIENT_NAME=Cliente Demo A
DASC_CENTRAL_DEMO_TOKEN=dasc-central-demo-token-lab
EOF

  chmod 600 "${ENV_FILE}"
else
  echo "==> config.env ya existe, se conserva"
fi

echo "==> Ajustando permisos"
chown -R "${APP_USER}:${APP_GROUP}" "${INSTALL_DIR}"
chmod 750 "${INSTALL_DIR}"
chmod 750 "${INSTALL_DIR}/data"
chmod 600 "${ENV_FILE}"

echo "==> Creando servicio systemd"
cat > "/etc/systemd/system/${SERVICE_NAME}.service" <<EOF
[Unit]
Description=DASC Central Support (FastAPI/Uvicorn)
After=network.target

[Service]
Type=simple
User=${APP_USER}
Group=${APP_GROUP}
WorkingDirectory=${INSTALL_DIR}
EnvironmentFile=${ENV_FILE}
ExecStart=${INSTALL_DIR}/venv/bin/python -m uvicorn main:app --host ${APP_HOST} --port ${APP_PORT}
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

echo "==> Activando servicio"
systemctl daemon-reload
systemctl enable "${SERVICE_NAME}"
systemctl restart "${SERVICE_NAME}"

sleep 3

echo "==> Estado del servicio"
systemctl --no-pager --full status "${SERVICE_NAME}" || true

echo
echo "==> Probando health local"
curl -s "http://127.0.0.1:${APP_PORT}/health" || true
echo

echo
echo "OK: DASC Central Support instalado."
echo "URL local: http://127.0.0.1:${APP_PORT}"
echo "Servicio: ${SERVICE_NAME}"
echo "Directorio: ${INSTALL_DIR}"
