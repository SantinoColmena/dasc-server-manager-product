#!/usr/bin/env bash
set -euo pipefail

APP_USER="${APP_USER:-dasc}"
APP_GROUP="${APP_GROUP:-$APP_USER}"
APP_HOME="/home/${APP_USER}"
BACKUP_DIR="${BACKUP_DIR:-${APP_HOME}/backups}"

DB_HOST="${DB_HOST:-}"
DB_NAME="${DB_NAME:-employees}"
DB_BACKUP_USER="${DB_BACKUP_USER:-dasc_backup}"
DB_BACKUP_PASS="${DB_BACKUP_PASS:-}"
DB_RESTORE_USER="${DB_RESTORE_USER:-dasc_restore}"
DB_RESTORE_PASS="${DB_RESTORE_PASS:-}"

INSTALL_BACKUP_SCRIPT="/usr/local/bin/backups_api.sh"
INSTALL_SERVICES_SCRIPT="/usr/local/bin/servicios_api.sh"
INSTALL_EXTERNAL_SYNC_SCRIPT="/usr/local/bin/sync_external_backup.sh"
INSTALL_RESTORE_SCRIPT="/usr/local/bin/restore_api.sh"
INSTALL_RESTORE_DRILL_SCRIPT="/usr/local/bin/restore_drill_api.sh"
SUDOERS_FILE="/etc/sudoers.d/dasc-servicios"
SSHD_CONFIG="/etc/ssh/sshd_config"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$SCRIPT_DIR/package"
OPTIONAL_API_PUBKEY="$SCRIPT_DIR/api_panel.pub"

prompt_required_var() {
  local var_name="$1"
  local prompt_text="$2"
  local current_value="${!var_name:-}"

  if [[ -z "$current_value" ]]; then
    read -rp "$prompt_text: " current_value
  fi

  if [[ -z "$current_value" ]]; then
    echo "ERROR: ${var_name} no puede estar vacío."
    exit 1
  fi

  printf -v "$var_name" '%s' "$current_value"
}
if [[ "$EUID" -ne 0 ]]; then
  echo "ERROR: ejecuta este script con sudo."
  exit 1
fi

if [[ ! -d "$PACKAGE_DIR" ]]; then
  echo "ERROR: no existe la carpeta package/"
  exit 1
fi

if [[ ! -f "$PACKAGE_DIR/backups_api.sh" ]]; then
  echo "ERROR: falta backups_api.sh en package/"
  exit 1
fi

if [[ ! -f "$PACKAGE_DIR/servicios_api.sh" ]]; then
  echo "ERROR: falta servicios_api.sh en package/"
  exit 1
fi

if [[ ! -f "$PACKAGE_DIR/sync_external_backup.sh" ]]; then
  echo "ERROR: falta sync_external_backup.sh en package/"
  exit 1
fi

if [[ ! -f "$PACKAGE_DIR/restore_api.sh" ]]; then
  echo "ERROR: falta restore_api.sh en package/"
  exit 1
fi

if [[ ! -f "$PACKAGE_DIR/restore_drill_api.sh" ]]; then
  echo "ERROR: falta restore_drill_api.sh en package/"
  exit 1
fi

echo "==> Instalando paquetes necesarios"
# =====================
# R-051F - PERFIL Y SECRETOS BACKUP-SERVICES
# =====================

is_empty_or_placeholder() {
  local value="${1:-}"

  [[ -z "$value" ||
     "$value" == CAMBIAR_* ||
     "$value" == "NO_GUARDAR_EN_GIT" ||
     "$value" == "dasc_backup_2026" ||
     "$value" == "dasc_restore_2026" ||
     "$value" == "<IP_SERVIDOR_DB>" ||
     "$value" == "<IP_SERVIDOR_BACKUPS>" ||
     "$value" == "<IP_SERVIDOR_DB_BACKUPS>" ]]
}

prompt_secret_var() {
  local key="$1"
  local label="$2"
  local value="${!key:-}"
  local input=""
  local confirm=""

  if ! is_empty_or_placeholder "$value"; then
    echo "==> ${key} definido externamente (no se muestra)"
    return 0
  fi

  read -rsp "${label}: " input
  echo
  read -rsp "Repite ${label}: " confirm
  echo

  if [[ "$input" != "$confirm" ]]; then
    echo "ERROR: los valores de ${key} no coinciden."
    exit 1
  fi

  if is_empty_or_placeholder "$input"; then
    echo "ERROR: ${key} no puede quedar vacío ni usar valores de laboratorio."
    exit 1
  fi

  printf -v "$key" "%s" "$input"
  echo "==> ${key} configurado manualmente (no se muestra)"
}

DASC_PROFILE_VALUE="${DASC_PROFILE:-custom}"
DASC_PROFILE_VALUE="$(echo "$DASC_PROFILE_VALUE" | tr '[:upper:]' '[:lower:]')"

case "$DASC_PROFILE_VALUE" in
  lite|standard|pro|custom)
    ;;
  *)
    echo "ERROR: DASC_PROFILE debe ser lite, standard, pro o custom."
    exit 1
    ;;
esac

echo "==> Perfil DASC backup-services seleccionado: ${DASC_PROFILE_VALUE}"

DB_SECRETS_FILE="${DB_SECRETS_FILE:-/root/dasc-db-install-secrets.env}"

if [[ -f "$DB_SECRETS_FILE" ]]; then
  echo "==> Cargando secretos DB desde ${DB_SECRETS_FILE}"

  set -a
  # shellcheck disable=SC1090
  . "$DB_SECRETS_FILE"
  set +a

  # Mapear nombres generados por install_db.sh a nombres usados por backup-services.
  if is_empty_or_placeholder "$DB_BACKUP_USER" && [[ -n "${BACKUP_USER:-}" ]]; then
    DB_BACKUP_USER="$BACKUP_USER"
  fi

  if is_empty_or_placeholder "$DB_BACKUP_PASS" && [[ -n "${BACKUP_PASS:-}" ]]; then
    DB_BACKUP_PASS="$BACKUP_PASS"
  fi

  if is_empty_or_placeholder "$DB_RESTORE_USER" && [[ -n "${RESTORE_USER:-}" ]]; then
    DB_RESTORE_USER="$RESTORE_USER"
  fi

  if is_empty_or_placeholder "$DB_RESTORE_PASS" && [[ -n "${RESTORE_PASS:-}" ]]; then
    DB_RESTORE_PASS="$RESTORE_PASS"
  fi

  if is_empty_or_placeholder "$DB_NAME" && [[ -n "${DB_NAME:-}" ]]; then
    DB_NAME="$DB_NAME"
  fi
else
  echo "==> No se encontró ${DB_SECRETS_FILE}. Se usarán variables de entorno o entrada manual."
fi

case "$DASC_PROFILE_VALUE" in
  lite)
    if is_empty_or_placeholder "$DB_HOST"; then
      DB_HOST="127.0.0.1"
      echo "==> DB_HOST asignado por perfil Lite: ${DB_HOST}"
    fi
    ;;

  standard|pro|custom)
    echo "==> DB_HOST se validará/pedirá para perfil ${DASC_PROFILE_VALUE}"
    ;;
esac

prompt_secret_var "DB_BACKUP_PASS" "Introduce la contraseña del usuario DB de backup"
prompt_secret_var "DB_RESTORE_PASS" "Introduce la contraseña del usuario DB de restauración"

prompt_required_var "DB_HOST" "Introduce la IP o hostname del servidor DB"

echo "==> Parámetros backup-services"
echo "DB_HOST=${DB_HOST}"
apt update

echo "==> Instalando dependencias base"
DEBIAN_FRONTEND=noninteractive apt install -y \
  python3 \
  openssh-server \
  sudo \
  cron \
  gzip \
  rsync \
  openssh-client

echo "==> Instalando cliente de base de datos"
# R-053A/B1: preferimos mariadb-client. Convive con mariadb-server (caso Lite en
# un unico host) y aporta mariadb-dump/mariadb-binlog para los alias mysql*.
# default-mysql-client (MySQL 8.0) entra en conflicto con MariaDB y en single-host
# desinstalaria mariadb-server. Solo como ultimo recurso si mariadb-client falta.
if ! DEBIAN_FRONTEND=noninteractive apt install -y mariadb-client; then
  echo "AVISO: no se pudo instalar mariadb-client. Probando default-mysql-client."
  DEBIAN_FRONTEND=noninteractive apt install -y default-mysql-client
fi

ensure_cmd_alias() {
  local expected="$1"
  local fallback="$2"

  if command -v "$expected" >/dev/null 2>&1; then
    return 0
  fi

  if command -v "$fallback" >/dev/null 2>&1; then
    local fallback_path
    fallback_path="$(command -v "$fallback")"

    cat > "/usr/local/bin/${expected}" <<EOF
#!/usr/bin/env bash
exec "${fallback_path}" "\$@"
EOF
    chmod 755 "/usr/local/bin/${expected}"
    return 0
  fi

  return 1
}

ensure_cmd_alias "mysql" "mariadb" || true
ensure_cmd_alias "mysqldump" "mariadb-dump" || true
ensure_cmd_alias "mysqlbinlog" "mariadb-binlog" || true

for required_cmd in mysql mysqldump mysqlbinlog gzip rsync ssh; do
  if ! command -v "$required_cmd" >/dev/null 2>&1; then
    echo "ERROR: falta comando requerido: $required_cmd"
    exit 1
  fi
done

echo "==> Habilitando SSH"
systemctl enable --now ssh

echo "==> Habilitando CRON"
systemctl enable --now cron

if [[ -f "$SSHD_CONFIG" ]]; then
  echo "==> Asegurando autenticación por contraseña y clave pública en SSH"
  if grep -qE '^[#[:space:]]*PasswordAuthentication' "$SSHD_CONFIG"; then
    sed -i -E 's|^[#[:space:]]*PasswordAuthentication[[:space:]]+.*|PasswordAuthentication yes|g' "$SSHD_CONFIG"
  else
    echo 'PasswordAuthentication yes' >> "$SSHD_CONFIG"
  fi

  if grep -qE '^[#[:space:]]*PubkeyAuthentication' "$SSHD_CONFIG"; then
    sed -i -E 's|^[#[:space:]]*PubkeyAuthentication[[:space:]]+.*|PubkeyAuthentication yes|g' "$SSHD_CONFIG"
  else
    echo 'PubkeyAuthentication yes' >> "$SSHD_CONFIG"
  fi

  # R-053A/B3: las imagenes cloud de Ubuntu traen un drop-in
  # (60-cloudimg-settings.conf) con PasswordAuthentication no que, al leerse antes
  # que sshd_config, gana (SSH usa el primer valor). Escribimos un drop-in 00-dasc
  # que se lee el primero para garantizar la auth por contrasena del bootstrap.
  SSHD_DROPIN_DIR="/etc/ssh/sshd_config.d"
  if [[ -d "$SSHD_DROPIN_DIR" ]]; then
    cat > "${SSHD_DROPIN_DIR}/00-dasc-ssh.conf" <<'SSHDROP'
PasswordAuthentication yes
PubkeyAuthentication yes
SSHDROP
    chmod 644 "${SSHD_DROPIN_DIR}/00-dasc-ssh.conf"
  fi

  systemctl restart ssh
fi

echo "==> Creando usuario de servicio ${APP_USER}"
if ! id "${APP_USER}" >/dev/null 2>&1; then
  useradd -m -s /bin/bash "${APP_USER}"
fi

if [[ -z "${APP_PASSWORD:-}" ]]; then
  echo
  read -rsp "Introduce la contraseña para ${APP_USER}: " APP_PASSWORD
  echo
  read -rsp "Repite la contraseña para ${APP_USER}: " APP_PASSWORD_CONFIRM
  echo

  if [[ "$APP_PASSWORD" != "$APP_PASSWORD_CONFIRM" ]]; then
    echo "ERROR: las contraseñas no coinciden."
    exit 1
  fi
fi

if [[ -z "$APP_PASSWORD" ]]; then
  echo "ERROR: la contraseña de ${APP_USER} no puede estar vacía."
  exit 1
fi

echo "${APP_USER}:${APP_PASSWORD}" | chpasswd
echo "==> Contraseña de ${APP_USER} configurada"

mkdir -p "${APP_HOME}/.ssh"
mkdir -p "${BACKUP_DIR}"
chown -R "${APP_USER}:${APP_GROUP}" "${APP_HOME}"
chmod 700 "${APP_HOME}/.ssh"
chmod 755 "${BACKUP_DIR}"
chmod 755 "${APP_HOME}"

echo "==> Instalando scripts administrativos"
normalize_script_file() {
  local file="$1"

  python3 - "$file" <<'PY'
from pathlib import Path
import sys

p = Path(sys.argv[1])
data = p.read_bytes()

if data.startswith(b"\xef\xbb\xbf"):
    data = data[3:]

data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")

p.write_bytes(data)
PY
}

normalize_script_file "$PACKAGE_DIR/backups_api.sh"
normalize_script_file "$PACKAGE_DIR/servicios_api.sh"
normalize_script_file "$PACKAGE_DIR/restore_api.sh"
normalize_script_file "$PACKAGE_DIR/restore_drill_api.sh"

cp "$PACKAGE_DIR/backups_api.sh" "$INSTALL_BACKUP_SCRIPT"
cp "$PACKAGE_DIR/servicios_api.sh" "$INSTALL_SERVICES_SCRIPT"
cp "$PACKAGE_DIR/sync_external_backup.sh" "$INSTALL_EXTERNAL_SYNC_SCRIPT"
cp "$PACKAGE_DIR/restore_api.sh" "$INSTALL_RESTORE_SCRIPT"
cp "$PACKAGE_DIR/restore_drill_api.sh" "$INSTALL_RESTORE_DRILL_SCRIPT"

chown root:root "$INSTALL_BACKUP_SCRIPT" "$INSTALL_SERVICES_SCRIPT" "$INSTALL_EXTERNAL_SYNC_SCRIPT" "$INSTALL_RESTORE_SCRIPT" "$INSTALL_RESTORE_DRILL_SCRIPT"
chmod 755 "$INSTALL_BACKUP_SCRIPT" "$INSTALL_SERVICES_SCRIPT" "$INSTALL_EXTERNAL_SYNC_SCRIPT" "$INSTALL_RESTORE_SCRIPT" "$INSTALL_RESTORE_DRILL_SCRIPT"

echo "==> Validando sintaxis de scripts"
bash -n "$INSTALL_BACKUP_SCRIPT"
bash -n "$INSTALL_SERVICES_SCRIPT"
bash -n "$INSTALL_RESTORE_SCRIPT"
bash -n "$INSTALL_RESTORE_DRILL_SCRIPT"

echo "==> Creando ${APP_HOME}/.my.cnf"
cat > "${APP_HOME}/.my.cnf" <<EOF2
[client]
user=${DB_BACKUP_USER}
password=${DB_BACKUP_PASS}
host=${DB_HOST}
EOF2
chown "${APP_USER}:${APP_GROUP}" "${APP_HOME}/.my.cnf"
chmod 600 "${APP_HOME}/.my.cnf"


echo "==> Creando ${APP_HOME}/.my_restore.cnf"
cat > "${APP_HOME}/.my_restore.cnf" <<EOF2
[client]
user=${DB_RESTORE_USER}
password=${DB_RESTORE_PASS}
host=${DB_HOST}
EOF2
chown "${APP_USER}:${APP_GROUP}" "${APP_HOME}/.my_restore.cnf"
chmod 600 "${APP_HOME}/.my_restore.cnf"

echo "==> Configurando sudoers para controlar servicios sin contraseña"
cat > "${SUDOERS_FILE}" <<EOF2
${APP_USER} ALL=(ALL) NOPASSWD: /usr/bin/systemctl start *, /usr/bin/systemctl stop *, /usr/bin/systemctl restart *, /usr/bin/systemctl status *, /usr/bin/systemctl is-active *
EOF2
chmod 440 "${SUDOERS_FILE}"
visudo -cf "${SUDOERS_FILE}"

if [[ -f "${OPTIONAL_API_PUBKEY}" ]]; then
  echo "==> Instalando clave pública opcional desde api_panel.pub"
  touch "${APP_HOME}/.ssh/authorized_keys"
  chown "${APP_USER}:${APP_GROUP}" "${APP_HOME}/.ssh/authorized_keys"
  chmod 600 "${APP_HOME}/.ssh/authorized_keys"
  grep -qxF "$(cat "${OPTIONAL_API_PUBKEY}")" "${APP_HOME}/.ssh/authorized_keys" || \
    cat "${OPTIONAL_API_PUBKEY}" >> "${APP_HOME}/.ssh/authorized_keys"
else
  echo "==> No se encontró api_panel.pub. La API podrá copiar su clave automáticamente con sshpass."
fi

echo "==> Validando herramientas de base de datos"
command -v mysql >/dev/null || { echo "ERROR: falta mysql"; exit 1; }
command -v mysqldump >/dev/null || { echo "ERROR: falta mysqldump"; exit 1; }
command -v mysqlbinlog >/dev/null || { echo "ERROR: falta mysqlbinlog"; exit 1; }
command -v crontab >/dev/null || { echo "ERROR: falta crontab"; exit 1; }

echo "==> Validaciones"
systemctl --no-pager --full status ssh || true
systemctl --no-pager --full status cron || true
ls -l "${INSTALL_BACKUP_SCRIPT}"
ls -l "${INSTALL_SERVICES_SCRIPT}"
ls -l "${INSTALL_EXTERNAL_SYNC_SCRIPT}"
ls -l "${INSTALL_RESTORE_SCRIPT}"
ls -l "${INSTALL_RESTORE_DRILL_SCRIPT}"
ls -ld "${BACKUP_DIR}"
sudo -u "${APP_USER}" test -f "${APP_HOME}/.my.cnf" && echo ".my.cnf OK"
sudo -u "${APP_USER}" test -f "${APP_HOME}/.my_restore.cnf" && echo ".my_restore.cnf OK"

echo "==> Comprobando acceso a MariaDB remota"
if sudo -u "${APP_USER}" mysql --defaults-extra-file="${APP_HOME}/.my.cnf" --protocol=tcp -h "${DB_HOST}" -e "SHOW DATABASES;" >/dev/null; then
  echo "Prueba mysql OK"
else
  echo "AVISO: la prueba mysql ha fallado. Revisa DB_HOST, usuario o permisos."
fi

echo "==> Comprobando usuario de restauración"
if sudo -u "${APP_USER}" mysql --defaults-extra-file="${APP_HOME}/.my_restore.cnf" --protocol=tcp -h "${DB_HOST}" -e "SHOW DATABASES;" >/dev/null; then
  echo "Prueba usuario restore OK"
else
  echo "AVISO: la prueba del usuario restore ha fallado. Revisa DB_HOST, usuario o permisos."
fi

echo "==> Comprobando mysqldump"
if sudo -u "${APP_USER}" mysqldump --defaults-extra-file="${APP_HOME}/.my.cnf" --protocol=tcp --single-transaction --databases "${DB_NAME}" >/dev/null; then
  echo "Prueba mysqldump OK"
else
  echo "AVISO: la prueba mysqldump ha fallado. Revisa DB_HOST, usuario o permisos."
fi

echo "==> Comprobando binlogs remotos"
FIRST_BINLOG="$(sudo -u "${APP_USER}" mysql --defaults-extra-file="${APP_HOME}/.my.cnf" --protocol=tcp -h "${DB_HOST}" --batch --skip-column-names -e "SHOW BINARY LOGS;" 2>/dev/null | awk 'NR==1 {print $1}' || true)"
if [[ -n "$FIRST_BINLOG" ]]; then
  if sudo -u "${APP_USER}" mysqlbinlog --defaults-extra-file="${APP_HOME}/.my.cnf" --read-from-remote-server --host="${DB_HOST}" --port=3306 "$FIRST_BINLOG" >/dev/null 2>&1; then
    echo "Prueba mysqlbinlog OK"
  else
    echo "AVISO: mysqlbinlog devolvió avisos/error de versión, pero puede funcionar igualmente con MariaDB."
  fi
else
  echo "AVISO: no se han detectado binlogs. Revisa log_bin en la máquina DB."
fi

echo
echo "============================================"
# =====================
# R-051F - RESUMEN DE SECRETOS BACKUP-SERVICES
# =====================

echo "Credenciales DB configuradas en ficheros locales:"
echo "- ${APP_HOME}/.my.cnf"
echo "- ${APP_HOME}/.my_restore.cnf"
echo "Permisos esperados: 600 y propietario ${APP_USER}:${APP_GROUP}"
echo "Los valores de contraseña no se muestran por pantalla."

echo "Servidor de Backups + Servicios instalado"
echo "APP_USER=${APP_USER}"
echo "DB_HOST=${DB_HOST}"
echo "DB_NAME=${DB_NAME}"
echo "Backups en: ${BACKUP_DIR}"
echo "Scripts: ${INSTALL_BACKUP_SCRIPT}, ${INSTALL_RESTORE_SCRIPT}, ${INSTALL_RESTORE_DRILL_SCRIPT} y ${INSTALL_SERVICES_SCRIPT}"
echo "SSH listo para autenticación por contraseña y clave pública"
echo "============================================"
