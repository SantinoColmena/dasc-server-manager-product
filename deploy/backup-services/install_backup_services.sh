#!/usr/bin/env bash
set -euo pipefail

APP_USER="${APP_USER:-dasc}"
APP_GROUP="${APP_GROUP:-$APP_USER}"
APP_HOME="/home/${APP_USER}"
BACKUP_DIR="${BACKUP_DIR:-${APP_HOME}/backups}"

DB_HOST="${DB_HOST:-}"
DB_NAME="${DB_NAME:-employees}"
DB_BACKUP_USER="${DB_BACKUP_USER:-dasc_backup}"
DB_BACKUP_PASS="${DB_BACKUP_PASS:-dasc_backup_2026}"
DB_RESTORE_USER="${DB_RESTORE_USER:-dasc_restore}"
DB_RESTORE_PASS="${DB_RESTORE_PASS:-dasc_restore_2026}"

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
apt update

# En Ubuntu 22.04/Isard, mysqlbinlog suele venir en mysql-server-core-8.0.
# Usamos cliente MySQL para asegurar mysql, mysqldump y mysqlbinlog.
DEBIAN_FRONTEND=noninteractive apt install -y python3 \
  openssh-server \
  sudo \
  cron \
  mariadb-client \
  mariadb-client-8.0 \
  mariadb-client-core-8.0 \
  mysql-server-core-8.0

echo "==> Habilitando SSH"
systemctl enable --now ssh

echo "==> Habilitando CRON"
systemctl enable --now cron

if [[ -f "$SSHD_CONFIG" ]]; then
  echo "==> Asegurando autenticaciÃ³n por contraseÃ±a y clave pÃºblica en SSH"
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

  systemctl restart ssh
fi

echo "==> Creando usuario de servicio ${APP_USER}"
if ! id "${APP_USER}" >/dev/null 2>&1; then
  useradd -m -s /bin/bash "${APP_USER}"
fi

if [[ -z "${APP_PASSWORD:-}" ]]; then
  echo
  read -rsp "Introduce la contraseÃ±a para ${APP_USER}: " APP_PASSWORD
  echo
  read -rsp "Repite la contraseÃ±a para ${APP_USER}: " APP_PASSWORD_CONFIRM
  echo

  if [[ "$APP_PASSWORD" != "$APP_PASSWORD_CONFIRM" ]]; then
    echo "ERROR: las contraseÃ±as no coinciden."
    exit 1
  fi
fi

if [[ -z "$APP_PASSWORD" ]]; then
  echo "ERROR: la contraseÃ±a de ${APP_USER} no puede estar vacÃ­a."
  exit 1
fi

echo "${APP_USER}:${APP_PASSWORD}" | chpasswd
echo "==> ContraseÃ±a de ${APP_USER} configurada"

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

echo "==> Configurando sudoers para controlar servicios sin contraseÃ±a"
cat > "${SUDOERS_FILE}" <<EOF2
${APP_USER} ALL=(ALL) NOPASSWD: /usr/bin/systemctl start *, /usr/bin/systemctl stop *, /usr/bin/systemctl restart *, /usr/bin/systemctl status *, /usr/bin/systemctl is-active *
EOF2
chmod 440 "${SUDOERS_FILE}"
visudo -cf "${SUDOERS_FILE}"

if [[ -f "${OPTIONAL_API_PUBKEY}" ]]; then
  echo "==> Instalando clave pÃºblica opcional desde api_panel.pub"
  touch "${APP_HOME}/.ssh/authorized_keys"
  chown "${APP_USER}:${APP_GROUP}" "${APP_HOME}/.ssh/authorized_keys"
  chmod 600 "${APP_HOME}/.ssh/authorized_keys"
  grep -qxF "$(cat "${OPTIONAL_API_PUBKEY}")" "${APP_HOME}/.ssh/authorized_keys" || \
    cat "${OPTIONAL_API_PUBKEY}" >> "${APP_HOME}/.ssh/authorized_keys"
else
  echo "==> No se encontrÃ³ api_panel.pub. La API podrÃ¡ copiar su clave automÃ¡ticamente con sshpass."
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

echo "==> Comprobando usuario de restauraciÃ³n"
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
    echo "AVISO: mysqlbinlog devolviÃ³ avisos/error de versiÃ³n, pero puede funcionar igualmente con MariaDB."
  fi
else
  echo "AVISO: no se han detectado binlogs. Revisa log_bin en la mÃ¡quina DB."
fi

echo
echo "============================================"
echo "Servidor de Backups + Servicios instalado"
echo "APP_USER=${APP_USER}"
echo "DB_HOST=${DB_HOST}"
echo "DB_NAME=${DB_NAME}"
echo "Backups en: ${BACKUP_DIR}"
echo "Scripts: ${INSTALL_BACKUP_SCRIPT}, ${INSTALL_RESTORE_SCRIPT}, ${INSTALL_RESTORE_DRILL_SCRIPT} y ${INSTALL_SERVICES_SCRIPT}"
echo "SSH listo para autenticaciÃ³n por contraseÃ±a y clave pÃºblica"
echo "============================================"
