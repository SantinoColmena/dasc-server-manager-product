#!/usr/bin/env bash
set -euo pipefail

APP_NAME="Vigex"
SERVICE_NAME="vigex-api"
APP_USER="${SUDO_USER:-$USER}"
APP_GROUP="$APP_USER"
PADRE_DIR="/opt/vigex"
INSTALL_DIR="/opt/vigex/api"
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


echo "==> Verificando cliente MariaDB para backups"
if ! command -v mysqldump >/dev/null 2>&1 && ! command -v mariadb-dump >/dev/null 2>&1; then
  apt-get update
  DEBIAN_FRONTEND=noninteractive apt-get install -y mariadb-client
fi
echo "==> Creando estructura destino"
mkdir -p "$PADRE_DIR"
mkdir -p "$INSTALL_DIR"

echo "==> Copiando archivos del proyecto"
cp -r "$PACKAGE_DIR"/. "$INSTALL_DIR"

if [[ ! -f "$INSTALL_DIR/config.env" ]]; then
  cp "$INSTALL_DIR/config.env.example" "$INSTALL_DIR/config.env"
fi

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

# =====================
# R-051D - PERFIL DE DESPLIEGUE API/PANEL LOCAL
# =====================

is_empty_or_placeholder() {
  local value="${1:-}"

  # R-053A/B2: se reconocen los placeholders con y sin corchetes (config.env.example
  # usa la forma sin corchetes) y las contrasenas de laboratorio, para que el
  # autorelleno por perfil (Lite=127.0.0.1) y los prompts (Standard/Pro) funcionen.
  [[ -z "$value" ||
     "$value" == CAMBIAR_* ||
     "$value" == "NO_GUARDAR_EN_GIT" ||
     "$value" == "<IP_SERVIDOR_API>" ||
     "$value" == "<IP_SERVIDOR_DB>" ||
     "$value" == "<IP_SERVIDOR_BACKUPS>" ||
     "$value" == "<IP_SERVIDOR_DB_BACKUPS>" ||
     "$value" == "IP_SERVIDOR_API" ||
     "$value" == "IP_SERVIDOR_DB" ||
     "$value" == "IP_SERVIDOR_BACKUPS" ||
     "$value" == "IP_SERVIDOR_DB_BACKUPS" ||
     "$value" == "IP_SERVIDOR_SERVICIOS_O_BACKUPS" ||
     "$value" == "vigex_backup_2026" ||
     "$value" == "vigex_restore_2026" ||
     "$value" == "vigex_logs_2026" ]]
}

write_config_if_env_set() {
  local key="$1"
  local value="${!key:-}"

  if ! is_empty_or_placeholder "$value"; then
    write_env_value "$key" "$value"
    echo "==> ${key} configurado desde variable de entorno"
  fi
}

write_config_if_empty() {
  local key="$1"
  local value="$2"
  local current

  current="$(read_env_value "$key" "$CONFIG_FILE" || true)"

  if is_empty_or_placeholder "$current"; then
    write_env_value "$key" "$value"
    echo "==> ${key} configurado automáticamente: ${value}"
  else
    echo "==> ${key} existente conservado"
  fi
}

prompt_config_key() {
  local key="$1"
  local label="$2"
  local default_value="${3:-}"
  local current
  local env_value
  local input

  current="$(read_env_value "$key" "$CONFIG_FILE" || true)"

  if ! is_empty_or_placeholder "$current"; then
    echo "==> ${key} existente conservado"
    return 0
  fi

  env_value="${!key:-}"

  if ! is_empty_or_placeholder "$env_value"; then
    write_env_value "$key" "$env_value"
    echo "==> ${key} configurado desde variable de entorno"
    return 0
  fi

  if [[ -n "$default_value" ]]; then
    read -rp "${label} [${default_value}]: " input
    input="${input:-$default_value}"
  else
    read -rp "${label}: " input
  fi

  if is_empty_or_placeholder "$input"; then
    echo "ERROR: ${key} no puede quedar vacío."
    exit 1
  fi

  write_env_value "$key" "$input"
  echo "==> ${key} configurado"
}

VIGEX_PROFILE_VALUE="${VIGEX_PROFILE:-$(read_env_value "VIGEX_PROFILE" "$CONFIG_FILE" || true)}"
VIGEX_PROFILE_VALUE="${VIGEX_PROFILE_VALUE:-custom}"
VIGEX_PROFILE_VALUE="$(echo "$VIGEX_PROFILE_VALUE" | tr '[:upper:]' '[:lower:]')"

case "$VIGEX_PROFILE_VALUE" in
  lite|standard|pro|custom)
    ;;
  *)
    echo "ERROR: VIGEX_PROFILE debe ser lite, standard, pro o custom."
    exit 1
    ;;
esac

write_env_value "VIGEX_PROFILE" "$VIGEX_PROFILE_VALUE"
echo "==> Perfil Vigex API seleccionado: ${VIGEX_PROFILE_VALUE}"

# R-053A/F8 - Importar credenciales de la BD de logs generadas por install_db.sh.
# En Lite (un host) o en multi-host con el fichero de secretos copiado a este
# servidor, el panel necesita la contrasena real de LOGS_DB para conectarse.
DB_SECRETS_FILE="${DB_SECRETS_FILE:-/root/vigex-db-install-secrets.env}"
if [[ -f "$DB_SECRETS_FILE" ]]; then
  echo "==> Importando credenciales de logs desde ${DB_SECRETS_FILE}"
  SECRET_LOGS_DB_NAME="$(read_env_value "LOGS_DB_NAME" "$DB_SECRETS_FILE" || true)"
  SECRET_LOGS_DB_USER="$(read_env_value "LOGS_DB_USER" "$DB_SECRETS_FILE" || true)"
  SECRET_LOGS_DB_PASS="$(read_env_value "LOGS_DB_PASS" "$DB_SECRETS_FILE" || true)"

  if [[ -n "$SECRET_LOGS_DB_NAME" ]]; then write_config_if_empty "LOGS_DB_NAME" "$SECRET_LOGS_DB_NAME"; fi
  if [[ -n "$SECRET_LOGS_DB_USER" ]]; then write_config_if_empty "LOGS_DB_USER" "$SECRET_LOGS_DB_USER"; fi
  if [[ -n "$SECRET_LOGS_DB_PASS" ]]; then write_config_if_empty "LOGS_DB_PASS" "$SECRET_LOGS_DB_PASS"; fi
else
  echo "==> Sin fichero de secretos DB (${DB_SECRETS_FILE}); LOGS_DB_* se conserva tal cual"
fi

# Variables opcionales que se pueden pasar desde plantilla/perfil.
write_config_if_env_set "CENTRAL_SUPPORT_ENABLED"
write_config_if_env_set "CENTRAL_SUPPORT_URL"
write_config_if_env_set "CENTRAL_SUPPORT_CLIENT_ID"
write_config_if_env_set "CENTRAL_SUPPORT_CLIENT_NAME"
write_config_if_env_set "CENTRAL_SUPPORT_TOKEN"
write_config_if_env_set "VIGEX_LOCAL_INTERNAL_SUPPORT_ENABLED"

# Alias cómodos de plantilla.
if [[ -n "${CLIENT_ID:-}" && -z "${CENTRAL_SUPPORT_CLIENT_ID:-}" ]]; then
  write_env_value "CENTRAL_SUPPORT_CLIENT_ID" "$CLIENT_ID"
  echo "==> CENTRAL_SUPPORT_CLIENT_ID configurado desde CLIENT_ID"
fi

if [[ -n "${CLIENT_NAME:-}" && -z "${CENTRAL_SUPPORT_CLIENT_NAME:-}" ]]; then
  write_env_value "CENTRAL_SUPPORT_CLIENT_NAME" "$CLIENT_NAME"
  echo "==> CENTRAL_SUPPORT_CLIENT_NAME configurado desde CLIENT_NAME"
fi

case "$VIGEX_PROFILE_VALUE" in
  lite)
    write_config_if_empty "BACKUPS_HOST" "127.0.0.1"
    write_config_if_empty "SERVICIOS_HOST" "127.0.0.1"
    write_config_if_empty "LOGS_DB_HOST" "127.0.0.1"
    write_config_if_empty "TERMINAL_DATABASE_HOST" "127.0.0.1"
    ;;

  standard)
    prompt_config_key "BACKUPS_HOST" "Introduce IP/hostname del servidor DB+Backups+Logs"
    STANDARD_SHARED_HOST="$(read_env_value "BACKUPS_HOST" "$CONFIG_FILE" || true)"

    prompt_config_key "SERVICIOS_HOST" "Introduce IP/hostname del servidor de servicios" "$STANDARD_SHARED_HOST"
    prompt_config_key "LOGS_DB_HOST" "Introduce IP/hostname del servidor de logs/DB" "$STANDARD_SHARED_HOST"
    prompt_config_key "TERMINAL_DATABASE_HOST" "Introduce IP/hostname del servidor DB para terminal" "$STANDARD_SHARED_HOST"
    ;;

  pro)
    prompt_config_key "BACKUPS_HOST" "Introduce IP/hostname del servidor Backups"
    prompt_config_key "SERVICIOS_HOST" "Introduce IP/hostname del servidor Servicios" "$(read_env_value "BACKUPS_HOST" "$CONFIG_FILE" || true)"
    prompt_config_key "LOGS_DB_HOST" "Introduce IP/hostname del servidor DB/Logs"
    prompt_config_key "TERMINAL_DATABASE_HOST" "Introduce IP/hostname del servidor DB para terminal" "$(read_env_value "LOGS_DB_HOST" "$CONFIG_FILE" || true)"
    ;;

  custom)
    prompt_config_key "BACKUPS_HOST" "Introduce IP/hostname del servidor Backups"
    prompt_config_key "SERVICIOS_HOST" "Introduce IP/hostname del servidor Servicios" "$(read_env_value "BACKUPS_HOST" "$CONFIG_FILE" || true)"
    prompt_config_key "LOGS_DB_HOST" "Introduce IP/hostname del servidor Logs/DB" "$(read_env_value "BACKUPS_HOST" "$CONFIG_FILE" || true)"
    prompt_config_key "TERMINAL_DATABASE_HOST" "Introduce IP/hostname del servidor DB para terminal" "$(read_env_value "LOGS_DB_HOST" "$CONFIG_FILE" || true)"
    ;;
esac

# Valor limpio por defecto para cliente real si no está definido.
write_config_if_empty "VIGEX_LOCAL_INTERNAL_SUPPORT_ENABLED" "false"

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


dedupe_config_csv_key() {
  local config_file="${CONFIG_FILE:-${INSTALL_DIR}/config.env}"
  local key="$1"

  if [[ ! -f "$config_file" ]]; then
    return 0
  fi

  python3 - "$config_file" "$key" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
key = sys.argv[2]

lines = path.read_text(encoding="utf-8").splitlines()
out = []

for line in lines:
    if line.startswith(key + "="):
        raw = line.split("=", 1)[1]
        seen = []
        for item in raw.split(","):
            item = item.strip()
            if item and item not in seen:
                seen.append(item)
        out.append(f"{key}={','.join(seen)}")
    else:
        out.append(line)

path.write_text("\n".join(out) + "\n", encoding="utf-8")
PY
}

dedupe_config_csv_key "VIGEX_SSH_ALLOWED_HOSTS"

echo "==> Ajustando permisos iniciales"
echo "==> Preparando directorios runtime"
mkdir -p "$INSTALL_DIR/data"
mkdir -p "$INSTALL_DIR/reports"
mkdir -p "$INSTALL_DIR/tools"
chown -R "$APP_USER:$APP_GROUP" /opt/vigex
chmod 750 "$PADRE_DIR"
chmod 750 "$INSTALL_DIR"
if [[ -f "$INSTALL_DIR/tools/generate_operational_report.sh" ]]; then
  chmod 755 "$INSTALL_DIR/tools/generate_operational_report.sh"
fi

if [[ -f "$INSTALL_DIR/tools/generate_operational_report.py" ]]; then
  chmod 755 "$INSTALL_DIR/tools/generate_operational_report.py"
fi

if [[ -f "$INSTALL_DIR/tools/run_full_db_backup.sh" ]]; then
  chmod 755 "$INSTALL_DIR/tools/run_full_db_backup.sh"
fi

if [[ -f "$INSTALL_DIR/tools/run_full_db_backup.py" ]]; then
  chmod 755 "$INSTALL_DIR/tools/run_full_db_backup.py"
fi

if [[ -f "$INSTALL_DIR/tools/cleanup_db_backups.sh" ]]; then
  chmod 755 "$INSTALL_DIR/tools/cleanup_db_backups.sh"
fi

if [[ -f "$INSTALL_DIR/tools/cleanup_db_backups.py" ]]; then
  chmod 755 "$INSTALL_DIR/tools/cleanup_db_backups.py"
fi

if [[ -f "$INSTALL_DIR/tools/restore_db_backup.sh" ]]; then
  chmod 755 "$INSTALL_DIR/tools/restore_db_backup.sh"
fi

if [[ -f "$INSTALL_DIR/tools/restore_db_backup.py" ]]; then
  chmod 755 "$INSTALL_DIR/tools/restore_db_backup.py"
fi
chmod 640 "$CONFIG_FILE"
if [[ -f "$INSTALL_DIR/tools/check_api_installation.sh" ]]; then
  chmod 755 "$INSTALL_DIR/tools/check_api_installation.sh"
fi

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
if [[ -f "$INSTALL_DIR/tools/check_api_installation.sh" ]]; then
  chmod 755 "$INSTALL_DIR/tools/check_api_installation.sh"
fi
  chown "$APP_USER:$APP_GROUP" "$CONFIG_FILE"
  echo "==> ADMIN_PASSWORD guardada como hash bcrypt"
fi

echo "==> Creando servicio systemd"
cat > "$SERVICE_FILE" <<EOF2
[Unit]
Description=Panel Vigex + API (FastAPI/Uvicorn)
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

echo "==> Preparando clave SSH dedicada para la API"
SSH_DIR="${INSTALL_DIR}/.ssh"
SSH_KEY_FILE="${SSH_DIR}/id_rsa_vigex"
SSH_KNOWN_HOSTS_FILE="${SSH_DIR}/known_hosts_vigex"

mkdir -p "$SSH_DIR"
chown "$APP_USER:$APP_GROUP" "$SSH_DIR"
chmod 700 "$SSH_DIR"

if [[ ! -f "$SSH_KEY_FILE" ]]; then
  sudo -u "$APP_USER" ssh-keygen -t ed25519 -N "" -f "$SSH_KEY_FILE"
  echo "==> Clave SSH dedicada generada en ${SSH_KEY_FILE}"
else
  echo "==> Clave SSH dedicada existente detectada. Se reutiliza."
fi

chown "$APP_USER:$APP_GROUP" "$SSH_KEY_FILE" "$SSH_KEY_FILE.pub"
chmod 600 "$SSH_KEY_FILE"
chmod 644 "$SSH_KEY_FILE.pub"

cp "$SSH_KEY_FILE.pub" "${INSTALL_DIR}/api_panel.pub"
chown "$APP_USER:$APP_GROUP" "${INSTALL_DIR}/api_panel.pub"
chmod 644 "${INSTALL_DIR}/api_panel.pub"
echo "==> Clave pública exportada a ${INSTALL_DIR}/api_panel.pub"

BACKUP_HOST="$(read_env_value "BACKUPS_HOST" "$CONFIG_FILE" || true)"
SERVICES_HOST="$(read_env_value "SERVICIOS_HOST" "$CONFIG_FILE" || true)"

if [[ -z "$BACKUP_HOST" || "$BACKUP_HOST" == CAMBIAR_* ]]; then
  echo "ERROR: BACKUPS_HOST no está configurado correctamente en config.env"
  exit 1
fi

if [[ -z "$SERVICES_HOST" || "$SERVICES_HOST" == CAMBIAR_* ]]; then
  SERVICES_HOST="$BACKUP_HOST"
fi

write_env_value "VIGEX_SSH_KEY" "$SSH_KEY_FILE"
write_env_value "VIGEX_SSH_KNOWN_HOSTS" "$SSH_KNOWN_HOSTS_FILE"
write_env_value "VIGEX_SSH_TIMEOUT" "30"
write_env_value "VIGEX_SSH_CONNECT_TIMEOUT" "10"
DATABASE_HOST="$(read_env_value "TERMINAL_DATABASE_HOST" "$CONFIG_FILE" || true)"

if [[ -z "$DATABASE_HOST" || "$DATABASE_HOST" == CAMBIAR_* ]]; then
  DATABASE_HOST="$(read_env_value "LOGS_DB_HOST" "$CONFIG_FILE" || true)"
fi

if [[ -z "$DATABASE_HOST" || "$DATABASE_HOST" == CAMBIAR_* ]]; then
  DATABASE_HOST="$BACKUP_HOST"
fi

build_unique_csv() {
  local result=""
  local item=""

  for item in "$@"; do
    if [[ -z "$item" ]]; then
      continue
    fi

    case ",${result}," in
      *,"${item}",*)
        ;;
      *)
        if [[ -z "$result" ]]; then
          result="$item"
        else
          result="${result},${item}"
        fi
        ;;
    esac
  done

  printf '%s\n' "$result"
}
VIGEX_ALLOWED_HOSTS="$(build_unique_csv "127.0.0.1" "localhost" "${BACKUP_HOST}" "${SERVICES_HOST}" "${DATABASE_HOST}")"
write_env_value "VIGEX_SSH_ALLOWED_HOSTS" "${VIGEX_ALLOWED_HOSTS}"

touch "$SSH_KNOWN_HOSTS_FILE"
chown "$APP_USER:$APP_GROUP" "$SSH_KNOWN_HOSTS_FILE"
chmod 644 "$SSH_KNOWN_HOSTS_FILE"

TARGET_HOSTS=("$BACKUP_HOST")
if [[ "$SERVICES_HOST" != "$BACKUP_HOST" ]]; then
  TARGET_HOSTS+=("$SERVICES_HOST")
fi

if [[ "$DATABASE_HOST" != "$BACKUP_HOST" && "$DATABASE_HOST" != "$SERVICES_HOST" ]]; then
  TARGET_HOSTS+=("$DATABASE_HOST")
fi

for TARGET_HOST in "${TARGET_HOSTS[@]}"; do
  echo "==> Registrando host SSH en known_hosts_vigex: ${TARGET_HOST}"
  ssh-keygen -R "$TARGET_HOST" -f "$SSH_KNOWN_HOSTS_FILE" >/dev/null 2>&1 || true
  if ssh-keyscan -H "$TARGET_HOST" >> "$SSH_KNOWN_HOSTS_FILE" 2>/dev/null; then
    echo "==> Huella SSH registrada correctamente para ${TARGET_HOST}"
  else
    echo "AVISO: no se pudo obtener la huella SSH de ${TARGET_HOST}"
    echo "AVISO: se omite la preparación SSH de ${TARGET_HOST}. La conexión con backups se validará en una puerta posterior."
    continue
  fi

  APP_USER_HOME="$(getent passwd "$APP_USER" | cut -d: -f6)"
mkdir -p "${APP_USER_HOME}/.ssh"
chown "$APP_USER:$APP_GROUP" "${APP_USER_HOME}/.ssh"
chmod 700 "${APP_USER_HOME}/.ssh"

echo "==> Configurando acceso SSH automático al servidor ${TARGET_HOST}"
  if [[ -z "${VIGEX_PASS:-}" ]]; then
    echo
    read -rsp "Introduce la contraseña actual del usuario vigex en ${TARGET_HOST}: " VIGEX_PASS
    echo
  fi

  if [[ -z "$VIGEX_PASS" ]]; then
    echo "ERROR: la contraseña de vigex no puede estar vacía."
    exit 1
  fi

  sudo -u "$APP_USER" sshpass -p "$VIGEX_PASS" ssh-copy-id \
    -i "$SSH_KEY_FILE.pub" \
    -o StrictHostKeyChecking=yes \
    -o UserKnownHostsFile="$SSH_KNOWN_HOSTS_FILE" \
    "vigex@${TARGET_HOST}" || {
      echo "ERROR: no se pudo copiar la clave automáticamente a vigex@${TARGET_HOST}."
      exit 1
    }

  echo "==> Verificando acceso SSH sin contraseña contra ${TARGET_HOST}"
  sudo -u "$APP_USER" ssh \
    -i "$SSH_KEY_FILE" \
    -o BatchMode=yes \
    -o StrictHostKeyChecking=yes \
    -o UserKnownHostsFile="$SSH_KNOWN_HOSTS_FILE" \
    "vigex@${TARGET_HOST}" "hostname >/dev/null" || {
      echo "ERROR: la verificación SSH sin contraseña ha fallado contra ${TARGET_HOST}."
      exit 1
    }

done
# R-053B/B5: unset VIGEX_PASS fuera del bucle para que la contraseña persista
# en despliegues multi-host (Standard/Pro). Dentro del bucle, el unset borraba
# la variable antes de la segunda iteración; read desde stdin=/dev/null devuelve
# exit 1, que set -euo pipefail convierte en salida silenciosa del instalador.
unset VIGEX_PASS

chmod 640 "$CONFIG_FILE"
if [[ -f "$INSTALL_DIR/tools/check_api_installation.sh" ]]; then
  chmod 755 "$INSTALL_DIR/tools/check_api_installation.sh"
fi
chown "$APP_USER:$APP_GROUP" "$CONFIG_FILE"

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
echo "SSH remoto: modo no bloqueante. Validacion completa en puerta posterior."
echo "URL local: http://127.0.0.1:8000"
echo "URL red:   http://<IP_DEL_SERVIDOR>:8000"
echo "============================================"


