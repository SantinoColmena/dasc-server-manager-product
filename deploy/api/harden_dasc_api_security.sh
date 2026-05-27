#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/dasc/api}"
SERVICE_NAME="${SERVICE_NAME:-dasc-api}"
SERVICE_FILE="${SERVICE_FILE:-/etc/systemd/system/${SERVICE_NAME}.service}"
APP_USER="${APP_USER:-dasc-api}"
APP_GROUP="${APP_GROUP:-dasc-api}"
TEST_USER="${TEST_USER:-santino}"

CONFIG_FILE="${APP_DIR}/config.env"
DATA_DIR="${APP_DIR}/data"
SSH_DIR="${APP_DIR}/.ssh"
REPORTS_DIR="${APP_DIR}/reports"

if [ "$(id -u)" -ne 0 ]; then
  echo "ERROR: ejecuta este script con sudo."
  exit 1
fi

echo "==> R-052E - Endureciendo DASC API local"

if [ ! -d "$APP_DIR" ]; then
  echo "ERROR: no existe $APP_DIR"
  exit 1
fi

if [ ! -f "$SERVICE_FILE" ]; then
  echo "ERROR: no existe $SERVICE_FILE"
  exit 1
fi

if [ ! -f "$CONFIG_FILE" ]; then
  echo "ERROR: no existe $CONFIG_FILE"
  exit 1
fi

echo "==> Creando grupo/usuario técnico si no existe"

if ! getent group "$APP_GROUP" >/dev/null 2>&1; then
  groupadd --system "$APP_GROUP"
fi

if ! id -u "$APP_USER" >/dev/null 2>&1; then
  useradd \
    --system \
    --gid "$APP_GROUP" \
    --home-dir "$APP_DIR" \
    --no-create-home \
    --shell /usr/sbin/nologin \
    "$APP_USER"
fi

echo "==> Parando servicio ${SERVICE_NAME}"
systemctl stop "$SERVICE_NAME"

STAMP="$(date +%Y%m%d-%H%M%S)"

echo "==> Creando backup de unidad systemd"
cp -a "$SERVICE_FILE" "/root/${SERVICE_NAME}.service.bak.R-052E-${STAMP}"

echo "==> Ajustando unidad systemd"

ensure_service_key() {
  local key="$1"
  local value="$2"

  if grep -qE "^${key}=" "$SERVICE_FILE"; then
    sed -i -E "s|^${key}=.*|${key}=${value}|g" "$SERVICE_FILE"
  else
    sed -i "/^\[Service\]/a ${key}=${value}" "$SERVICE_FILE"
  fi
}

ensure_service_key "User" "$APP_USER"
ensure_service_key "Group" "$APP_GROUP"

sed -i -E 's|--host[[:space:]]+[^[:space:]]+|--host 127.0.0.1|g' "$SERVICE_FILE"

echo "==> Ajustando propietario general"
chown -R "$APP_USER:$APP_GROUP" "$APP_DIR"

echo "==> Endureciendo directorio principal"
chmod 750 "$APP_DIR"

echo "==> Protegiendo config.env y backups de config"
find "$APP_DIR" -maxdepth 1 -type f -name 'config.env*' -exec chown root:"$APP_GROUP" {} \;
find "$APP_DIR" -maxdepth 1 -type f -name 'config.env*' -exec chmod 640 {} \;

echo "==> Protegiendo data/"
if [ -d "$DATA_DIR" ]; then
  chown -R "$APP_USER:$APP_GROUP" "$DATA_DIR"
  find "$DATA_DIR" -type d -exec chmod 750 {} \;
  find "$DATA_DIR" -type f -exec chmod 640 {} \;
fi

echo "==> Protegiendo .ssh/"
if [ -d "$SSH_DIR" ]; then
  chown -R "$APP_USER:$APP_GROUP" "$SSH_DIR"
  chmod 700 "$SSH_DIR"
  find "$SSH_DIR" -type f -name 'id_rsa*' ! -name '*.pub' -exec chmod 600 {} \;
  find "$SSH_DIR" -type f -name '*.pub' -exec chmod 644 {} \;
  find "$SSH_DIR" -type f -name 'known_hosts*' -exec chmod 644 {} \;
fi

echo "==> Ajustando reports/"
if [ -d "$REPORTS_DIR" ]; then
  chown -R "$APP_USER:$APP_GROUP" "$REPORTS_DIR"
  find "$REPORTS_DIR" -type d -exec chmod 750 {} \;
  find "$REPORTS_DIR" -type f -exec chmod 640 {} \;
fi

echo "==> Asegurando scripts ejecutables"
if [ -d "$APP_DIR/scripts" ]; then
  chown -R "$APP_USER:$APP_GROUP" "$APP_DIR/scripts"
  find "$APP_DIR/scripts" -type d -exec chmod 750 {} \;
  find "$APP_DIR/scripts" -type f -name '*.py' -exec chmod 750 {} \;
fi

if [ -d "$APP_DIR/tools" ]; then
  chown -R "$APP_USER:$APP_GROUP" "$APP_DIR/tools"
  find "$APP_DIR/tools" -type d -exec chmod 750 {} \;
  find "$APP_DIR/tools" -type f -name '*.sh' -exec chmod 750 {} \;
  find "$APP_DIR/tools" -type f -name '*.py' -exec chmod 750 {} \;
fi

echo "==> Recargando systemd"
systemctl daemon-reload

echo "==> Arrancando ${SERVICE_NAME}"
systemctl start "$SERVICE_NAME"
systemctl enable "$SERVICE_NAME" >/dev/null

echo
echo "==> Estado servicio"
systemctl --no-pager --full status "$SERVICE_NAME" || true

echo
echo "==> Validación local"
curl -i -s http://127.0.0.1:8000/ | head -n 10

echo
echo "==> Validación permisos config.env"
ls -l "$CONFIG_FILE"

if id -u "$TEST_USER" >/dev/null 2>&1; then
  if sudo -u "$TEST_USER" cat "$CONFIG_FILE" >/tmp/dasc-api-config-read-test.txt 2>/tmp/dasc-api-config-read-test.err; then
    echo "AVISO: ${TEST_USER} todavía puede leer ${CONFIG_FILE}"
  else
    echo "OK: ${TEST_USER} no puede leer ${CONFIG_FILE}"
  fi
else
  echo "AVISO: usuario de prueba ${TEST_USER} no existe"
fi

echo
echo "==> Puertos"
ss -lntp | grep -E ':80|:8080|:8000|:8010|:22' || true

echo
echo "OK: hardening R-052E aplicado."
echo "Acceso recomendado al panel local: Nginx."
