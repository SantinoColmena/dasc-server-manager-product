#!/usr/bin/env bash
set -euo pipefail

APP_NAME="DASC Server Manager"
SERVICE_NAME="dasc-api"
APP_USER="${SUDO_USER:-$USER}"
APP_GROUP="$APP_USER"
PADRE_DIR="/opt/dasc"
INSTALL_DIR="/opt/dasc/api"
VENV_DIR="$INSTALL_DIR/venv"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$SCRIPT_DIR/package"

CONFIG_FILE="$INSTALL_DIR/config.env"
CONFIG_EXAMPLE_FILE="$INSTALL_DIR/config.env.example"

if [[ "$EUID" -ne 0 ]]; then
  echo "ERROR: ejecuta este script con sudo."
  exit 1
fi

echo "==> Instalando ${APP_NAME}"
echo "==> Usuario de ejecución: ${APP_USER}"
echo "==> Ruta destino: ${INSTALL_DIR}"

if [[ ! -d "$PACKAGE_DIR" ]]; then
  echo "ERROR: no existe la carpeta package/"
  exit 1
fi

for required in main.py requirements.txt config.env.example templates static; do
  if [[ ! -e "$PACKAGE_DIR/$required" ]]; then
    echo "ERROR: falta $required dentro de package/"
    exit 1
  fi
done

echo "==> Instalando dependencias del sistema"
apt update
apt install -y python3 python3-venv python3-pip openssh-client curl sshpass

echo "==> Creando estructura destino"
mkdir -p "$PADRE_DIR"
mkdir -p "$INSTALL_DIR"

echo "==> Copiando archivos del proyecto"
cp -r "$PACKAGE_DIR"/. "$INSTALL_DIR"

echo "==> Preparando config.env seguro"
if [[ ! -f "$CONFIG_FILE" ]]; then
  cp "$CONFIG_EXAMPLE_FILE" "$CONFIG_FILE"
  echo "==> config.env creado desde config.env.example"
else
  echo "==> config.env existente detectado. Se conserva."
fi

generate_secret_key() {
  python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(48))
PY
}

read_env_value() {
  local key="$1"
  local file="$2"
  awk -F= -v k="$key" '$1 == k {print substr($0, index($0, "=") + 1)}' "$file" | tail -n1
}

write_env_value() {
  local key="$1"
  local value="$2"

  python3 - "$CONFIG_FILE" "$key" "$value" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
key = sys.argv[2]
value = sys.argv[3]

lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
out = []
found = False

for line in lines:
    if line.startswith(key + "="):
        out.append(f"{key}={value}")
        found = True
    else:
        out.append(line)

if not found:
    out.append(f"{key}={value}")

path.write_text("\n".join(out) + "\n", encoding="utf-8")
PY
}

CURRENT_SECRET_KEY="$(read_env_value "SECRET_KEY" "$CONFIG_FILE" || true)"
if [[ -z "$CURRENT_SECRET_KEY" || "$CURRENT_SECRET_KEY" == CAMBIAR_* || "$CURRENT_SECRET_KEY" == "cambia-esta-clave-por-una-segura" ]]; then
  NEW_SECRET_KEY="$(generate_secret_key)"
  write_env_value "SECRET_KEY" "$NEW_SECRET_KEY"
  echo "==> SECRET_KEY generada automáticamente"
else
  echo "==> SECRET_KEY existente conservada"
fi

CURRENT_ADMIN_PASSWORD="$(read_env_value "ADMIN_PASSWORD" "$CONFIG_FILE" || true)"
NEED_ADMIN_PASSWORD="no"

if [[ -z "$CURRENT_ADMIN_PASSWORD" || "$CURRENT_ADMIN_PASSWORD" == CAMBIAR_* || "$CURRENT_ADMIN_PASSWORD" == "admin123" ]]; then
  NEED_ADMIN_PASSWORD="yes"
fi

if [[ "$NEED_ADMIN_PASSWORD" == "yes" ]]; then
  if [[ -z "${ADMIN_PASSWORD_INPUT:-}" ]]; then
    echo
    read -rsp "Introduce la nueva contraseña del administrador del panel: " ADMIN_PASSWORD_INPUT
    echo
    read -rsp "Repite la contraseña del administrador del panel: " ADMIN_PASSWORD_CONFIRM
    echo

    if [[ "$ADMIN_PASSWORD_INPUT" != "$ADMIN_PASSWORD_CONFIRM" ]]; then
      echo "ERROR: las contraseñas del administrador no coinciden."
      exit 1
    fi
  fi

  if [[ -z "$ADMIN_PASSWORD_INPUT" ]]; then
    echo "ERROR: la contraseña del administrador no puede estar vacía."
    exit 1
  fi
else
  echo "==> ADMIN_PASSWORD existente conservada"
fi

echo "==> Ajustando permisos iniciales"
chown -R "$APP_USER:$APP_GROUP" /opt/dasc
chmod 750 "$PADRE_DIR"
chmod 750 "$INSTALL_DIR"
chmod 640 "$CONFIG_FILE"

echo "==> Creando entorno virtual"
if [[ ! -d "$VENV_DIR" ]]; then
  sudo -u "$APP_USER" python3 -m venv "$VENV_DIR"
else
  echo "==> Entorno virtual existente detectado. Se reutiliza."
fi

echo "==> Instalando dependencias Python"
sudo -u "$APP_USER" "$VENV_DIR/bin/pip" install --upgrade pip
sudo -u "$APP_USER" "$VENV_DIR/bin/pip" install -r "$INSTALL_DIR/requirements.txt"

if [[ "$NEED_ADMIN_PASSWORD" == "yes" ]]; then
  echo "==> Generando hash bcrypt para ADMIN_PASSWORD"
  ADMIN_PASSWORD_HASH="$(sudo -u "$APP_USER" "$VENV_DIR/bin/python" - "$ADMIN_PASSWORD_INPUT" <<'PY'
import sys
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print(pwd_context.hash(sys.argv[1]))
PY
)"
  write_env_value "ADMIN_PASSWORD" "$ADMIN_PASSWORD_HASH"
  chmod 640 "$CONFIG_FILE"
  chown "$APP_USER:$APP_GROUP" "$CONFIG_FILE"
  echo "==> ADMIN_PASSWORD guardada como hash bcrypt"
fi

echo "==> Creando servicio systemd"
cat > "$SERVICE_FILE" <<EOF2
[Unit]
Description=DASC Panel + API (FastAPI/Uvicorn)
After=network-online.target
Wants=network-online.target

[Service]
User=${APP_USER}
Group=${APP_GROUP}
WorkingDirectory=${INSTALL_DIR}
EnvironmentFile=${INSTALL_DIR}/config.env
ExecStart=${VENV_DIR}/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF2
chmod 644 "$SERVICE_FILE"

echo "==> Recargando systemd"
systemctl daemon-reload

echo "==> Activando servicio al arranque"
systemctl enable "$SERVICE_NAME"

echo "==> Reiniciando servicio"
systemctl restart "$SERVICE_NAME"

echo "==> Preparando clave SSH para la API"
APP_HOME="$(eval echo "~${APP_USER}")"
sudo -u "$APP_USER" mkdir -p "${APP_HOME}/.ssh"
sudo -u "$APP_USER" chmod 700 "${APP_HOME}/.ssh"

if [[ ! -f "${APP_HOME}/.ssh/id_rsa" ]]; then
  sudo -u "$APP_USER" ssh-keygen -t rsa -b 4096 -N "" -f "${APP_HOME}/.ssh/id_rsa"
  echo "==> Clave SSH generada"
else
  echo "==> La clave SSH ya existe, se reutiliza"
fi

cp "${APP_HOME}/.ssh/id_rsa.pub" "${INSTALL_DIR}/api_panel.pub"
chown "$APP_USER:$APP_GROUP" "${INSTALL_DIR}/api_panel.pub"
chmod 644 "${INSTALL_DIR}/api_panel.pub"
echo "==> Clave pública exportada a ${INSTALL_DIR}/api_panel.pub"

BACKUP_HOST="$(read_env_value "BACKUPS_HOST" "$CONFIG_FILE" || true)"
if [[ -z "$BACKUP_HOST" || "$BACKUP_HOST" == CAMBIAR_* ]]; then
  echo "ERROR: BACKUPS_HOST no está configurado correctamente en config.env"
  exit 1
fi

echo "==> Configurando acceso SSH automático al servidor de backups (${BACKUP_HOST})"
if [[ -z "${DASC_PASS:-}" ]]; then
  echo
  read -rsp "Introduce la contraseña actual del usuario dasc en ${BACKUP_HOST}: " DASC_PASS
  echo
fi

if [[ -z "$DASC_PASS" ]]; then
  echo "ERROR: la contraseña de dasc no puede estar vacía."
  exit 1
fi

sudo -u "$APP_USER" sshpass -p "$DASC_PASS" ssh-copy-id -o StrictHostKeyChecking=no "dasc@${BACKUP_HOST}" || {
  echo "ERROR: no se pudo copiar la clave automáticamente a dasc@${BACKUP_HOST}."
  exit 1
}

echo "==> Verificando acceso SSH sin contraseña"
sudo -u "$APP_USER" ssh -o BatchMode=yes -o StrictHostKeyChecking=no "dasc@${BACKUP_HOST}" "hostname >/dev/null" || {
  echo "ERROR: la verificación SSH sin contraseña ha fallado."
  exit 1
}

echo "==> Comprobando estado"
systemctl --no-pager --full status "$SERVICE_NAME" || true
sleep 2
curl -I http://127.0.0.1:8000 || true

echo
echo "============================================"
echo "Instalación completada"
echo "Panel instalado en: $INSTALL_DIR"
echo "Servicio: $SERVICE_NAME"
echo "config.env protegido en: $CONFIG_FILE"
echo "SSH automático configurado contra: $BACKUP_HOST"
echo "URL local: http://127.0.0.1:8000"
echo "URL red:   http://<IP_DEL_SERVIDOR>:8000"
echo "============================================"
