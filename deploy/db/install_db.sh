#!/usr/bin/env bash
set -euo pipefail

DB_BIND_ADDRESS="${DB_BIND_ADDRESS:-0.0.0.0}"
DB_NAME="${DB_NAME:-employees}"
TEST_TABLE="${TEST_TABLE:-empleados_demo}"

BACKUP_USER="${BACKUP_USER:-vigex_backup}"
BACKUP_PASS="${BACKUP_PASS:-}"
BACKUP_ALLOWED_HOST="${BACKUP_ALLOWED_HOST:-}"
RESTORE_USER="${RESTORE_USER:-vigex_restore}"
RESTORE_PASS="${RESTORE_PASS:-}"
LOGS_DB_NAME="${LOGS_DB_NAME:-vigex_logs}"
LOGS_DB_USER="${LOGS_DB_USER:-vigex_logs}"
LOGS_DB_PASS="${LOGS_DB_PASS:-}"
LOGS_ALLOWED_HOST="${LOGS_ALLOWED_HOST:-}"

MARIADB_CNF="/etc/mysql/mariadb.conf.d/50-server.cnf"

# Usuario SSH usado por la API/Terminal para entrar en esta máquina DB
APP_USER="${APP_USER:-vigex}"
APP_GROUP="${APP_GROUP:-$APP_USER}"
APP_HOME="/home/${APP_USER}"
SSHD_CONFIG="/etc/ssh/sshd_config"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPTIONAL_API_PUBKEY="$SCRIPT_DIR/api_panel.pub"

DB_SERVER_ID="${DB_SERVER_ID:-}"
BINLOG_BASENAME="${BINLOG_BASENAME:-/var/log/mysql/vigex-bin}"
BINLOG_FORMAT="${BINLOG_FORMAT:-ROW}"
BINLOG_EXPIRE_DAYS="${BINLOG_EXPIRE_DAYS:-14}"
BINLOG_MAX_SIZE="${BINLOG_MAX_SIZE:-100M}"

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

# =====================
# R-051E - PERFIL Y SECRETOS DB
# =====================

is_empty_or_placeholder() {
  local value="${1:-}"

  [[ -z "$value" ||
     "$value" == CAMBIAR_* ||
     "$value" == "NO_GUARDAR_EN_GIT" ||
     "$value" == "vigex_backup_2026" ||
     "$value" == "vigex_restore_2026" ||
     "$value" == "vigex_logs_2026" ||
     "$value" == "<IP_SERVIDOR_API>" ||
     "$value" == "<IP_SERVIDOR_DB>" ||
     "$value" == "<IP_SERVIDOR_BACKUPS>" ||
     "$value" == "<IP_SERVIDOR_DB_BACKUPS>" ]]
}

generate_db_secret() {
  python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(32))
PY
}

resolve_secret_var() {
  local key="$1"
  local value="${!key:-}"

  if is_empty_or_placeholder "$value"; then
    printf -v "$key" "%s" "$(generate_db_secret)"
    echo "==> ${key} generado automaticamente (no se muestra)"
  else
    echo "==> ${key} definido externamente (no se muestra)"
  fi
}

VIGEX_PROFILE_VALUE="${VIGEX_PROFILE:-custom}"
VIGEX_PROFILE_VALUE="$(echo "$VIGEX_PROFILE_VALUE" | tr '[:upper:]' '[:lower:]')"

case "$VIGEX_PROFILE_VALUE" in
  lite|standard|pro|custom)
    ;;
  *)
    echo "ERROR: VIGEX_PROFILE debe ser lite, standard, pro o custom."
    exit 1
    ;;
esac

echo "==> Perfil Vigex DB seleccionado: ${VIGEX_PROFILE_VALUE}"

if is_empty_or_placeholder "$DB_SERVER_ID"; then
  case "$VIGEX_PROFILE_VALUE" in
    lite)
      DB_SERVER_ID="10"
      ;;
    standard)
      DB_SERVER_ID="20"
      ;;
    pro)
      DB_SERVER_ID="30"
      ;;
    custom)
      DB_SERVER_ID="20"
      ;;
  esac

  echo "==> DB_SERVER_ID asignado por perfil: ${DB_SERVER_ID}"
else
  echo "==> DB_SERVER_ID definido externamente: ${DB_SERVER_ID}"
fi

resolve_secret_var "BACKUP_PASS"
resolve_secret_var "RESTORE_PASS"
resolve_secret_var "LOGS_DB_PASS"

prompt_required_var "BACKUP_ALLOWED_HOST" "Introduce la IP o hostname permitido para backups/restauración"
prompt_required_var "LOGS_ALLOWED_HOST" "Introduce la IP o hostname permitido para logs/API"

echo "==> Parámetros de acceso remoto DB"
echo "BACKUP_ALLOWED_HOST=${BACKUP_ALLOWED_HOST}"
echo "LOGS_ALLOWED_HOST=${LOGS_ALLOWED_HOST}"
echo "==> Instalando MariaDB, SSH y sudo"
apt update
DEBIAN_FRONTEND=noninteractive apt install -y mariadb-server mariadb-client openssh-server sudo

echo "==> Preparando SSH para la terminal remota de Vigex"
systemctl enable --now ssh

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
  # que sshd_config, gana (SSH usa el primer valor). Escribimos un drop-in 00-vigex
  # que se lee el primero para garantizar la auth por contrasena del bootstrap.
  SSHD_DROPIN_DIR="/etc/ssh/sshd_config.d"
  if [[ -d "$SSHD_DROPIN_DIR" ]]; then
    cat > "${SSHD_DROPIN_DIR}/00-vigex-ssh.conf" <<'SSHDROP'
PasswordAuthentication yes
PubkeyAuthentication yes
SSHDROP
    chmod 644 "${SSHD_DROPIN_DIR}/00-vigex-ssh.conf"
  fi

  systemctl restart ssh
fi

echo "==> Creando usuario SSH de servicio ${APP_USER}"
if ! id "${APP_USER}" >/dev/null 2>&1; then
  useradd -m -s /bin/bash "${APP_USER}"
fi

if [[ -z "${APP_PASSWORD:-}" ]]; then
  echo
  read -rsp "Introduce la contraseña para el usuario ${APP_USER} en esta máquina DB: " APP_PASSWORD
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
touch "${APP_HOME}/.ssh/authorized_keys"
chown -R "${APP_USER}:${APP_GROUP}" "${APP_HOME}"
chmod 755 "${APP_HOME}"
chmod 700 "${APP_HOME}/.ssh"
chmod 600 "${APP_HOME}/.ssh/authorized_keys"

if [[ -f "${OPTIONAL_API_PUBKEY}" ]]; then
  echo "==> Instalando clave pública opcional desde api_panel.pub"
  grep -qxF "$(cat "${OPTIONAL_API_PUBKEY}")" "${APP_HOME}/.ssh/authorized_keys" || \
    cat "${OPTIONAL_API_PUBKEY}" >> "${APP_HOME}/.ssh/authorized_keys"
  chown "${APP_USER}:${APP_GROUP}" "${APP_HOME}/.ssh/authorized_keys"
  chmod 600 "${APP_HOME}/.ssh/authorized_keys"
else
  echo "==> No se encontró api_panel.pub junto al instalador DB."
  echo "==> La API podrá copiar su clave automáticamente con sshpass durante install_vigex_api.sh."
fi

echo "==> Configurando bind-address y binary logs en ${MARIADB_CNF}"
if [[ ! -f "$MARIADB_CNF" ]]; then
  echo "ERROR: no existe ${MARIADB_CNF}"
  exit 1
fi

cp -n "$MARIADB_CNF" "${MARIADB_CNF}.bak" || true

if grep -qE '^[#[:space:]]*bind-address' "$MARIADB_CNF"; then
  sed -i -E "s|^[#[:space:]]*bind-address[[:space:]]*=.*|bind-address = ${DB_BIND_ADDRESS}|g" "$MARIADB_CNF"
else
  cat >> "$MARIADB_CNF" <<EOF

# Vigex NETWORK START
[mysqld]
bind-address = ${DB_BIND_ADDRESS}
# Vigex NETWORK END
EOF
fi

echo "==> Preparando directorio de binlogs"
mkdir -p /var/log/mysql
chown mysql:adm /var/log/mysql
chmod 750 /var/log/mysql

# Evita duplicados si el instalador se ejecuta varias veces
sed -i '/# Vigex BINLOG START/,/# Vigex BINLOG END/d' "$MARIADB_CNF"

cat >> "$MARIADB_CNF" <<EOF

# Vigex BINLOG START
server_id = ${DB_SERVER_ID}
log_bin = ${BINLOG_BASENAME}
binlog_format = ${BINLOG_FORMAT}
expire_logs_days = ${BINLOG_EXPIRE_DAYS}
max_binlog_size = ${BINLOG_MAX_SIZE}
# Vigex BINLOG END
EOF

echo "==> Habilitando y reiniciando MariaDB"
systemctl enable --now mariadb
systemctl restart mariadb

echo "==> Creando base de datos, tabla demo y usuarios de backup/restauración"
mariadb <<SQL
CREATE DATABASE IF NOT EXISTS \`${DB_NAME}\`;

CREATE TABLE IF NOT EXISTS \`${DB_NAME}\`.\`${TEST_TABLE}\` (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL,
  fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO \`${DB_NAME}\`.\`${TEST_TABLE}\` (nombre)
SELECT 'registro-inicial'
WHERE NOT EXISTS (
  SELECT 1 FROM \`${DB_NAME}\`.\`${TEST_TABLE}\` WHERE nombre='registro-inicial'
);

CREATE USER IF NOT EXISTS '${BACKUP_USER}'@'${BACKUP_ALLOWED_HOST}' IDENTIFIED BY '${BACKUP_PASS}';
ALTER USER '${BACKUP_USER}'@'${BACKUP_ALLOWED_HOST}' IDENTIFIED BY '${BACKUP_PASS}';

GRANT SELECT, SHOW VIEW, TRIGGER, EVENT, LOCK TABLES
ON \`${DB_NAME}\`.* TO '${BACKUP_USER}'@'${BACKUP_ALLOWED_HOST}';

GRANT RELOAD, REPLICATION CLIENT, REPLICATION SLAVE
ON *.* TO '${BACKUP_USER}'@'${BACKUP_ALLOWED_HOST}';

CREATE USER IF NOT EXISTS '${RESTORE_USER}'@'${BACKUP_ALLOWED_HOST}' IDENTIFIED BY '${RESTORE_PASS}';
ALTER USER '${RESTORE_USER}'@'${BACKUP_ALLOWED_HOST}' IDENTIFIED BY '${RESTORE_PASS}';

GRANT ALL PRIVILEGES
ON \`${DB_NAME}\`.* TO '${RESTORE_USER}'@'${BACKUP_ALLOWED_HOST}';


CREATE DATABASE IF NOT EXISTS \`${LOGS_DB_NAME}\`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS '${LOGS_DB_USER}'@'${LOGS_ALLOWED_HOST}'
  IDENTIFIED BY '${LOGS_DB_PASS}';

ALTER USER '${LOGS_DB_USER}'@'${LOGS_ALLOWED_HOST}'
  IDENTIFIED BY '${LOGS_DB_PASS}';

GRANT ALL PRIVILEGES ON \`${LOGS_DB_NAME}\`.* TO '${LOGS_DB_USER}'@'${LOGS_ALLOWED_HOST}';

CREATE TABLE IF NOT EXISTS \`${LOGS_DB_NAME}\`.\`eventos\` (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  origen VARCHAR(100) NOT NULL DEFAULT 'vigex-api',
  tipo VARCHAR(100) NOT NULL,
  usuario VARCHAR(100) NULL,
  ip_origen VARCHAR(45) NULL,
  recurso VARCHAR(255) NULL,
  resultado VARCHAR(50) NOT NULL,
  detalle TEXT NULL,
  PRIMARY KEY (id),
  KEY idx_fecha (fecha),
  KEY idx_tipo (tipo),
  KEY idx_usuario (usuario),
  KEY idx_resultado (resultado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

FLUSH PRIVILEGES;
SQL

echo "==> Validaciones"
systemctl --no-pager --full status ssh || true
systemctl --no-pager --full status mariadb || true
id "${APP_USER}" || true
ls -ld "${APP_HOME}" "${APP_HOME}/.ssh" || true
ss -lntp | grep -E '(:22|:3306)' || true
mariadb -e "SELECT User, Host FROM mysql.user WHERE User='${BACKUP_USER}';"
mariadb -e "SHOW DATABASES LIKE '${DB_NAME}';"
mariadb -e "SHOW GRANTS FOR '${BACKUP_USER}'@'${BACKUP_ALLOWED_HOST}';" || true
mariadb -e "SHOW GRANTS FOR '${RESTORE_USER}'@'${BACKUP_ALLOWED_HOST}';" || true
mariadb -e "SHOW VARIABLES LIKE 'log_bin';"
mariadb -e "SELECT User, Host FROM mysql.user WHERE User='${LOGS_DB_USER}';"
mariadb -e "USE ${LOGS_DB_NAME}; SHOW TABLES;"
mariadb -e "SHOW MASTER STATUS;"
mariadb -e "SHOW BINARY LOGS;"

echo
echo "============================================"
echo "Base de datos instalada correctamente"
# =====================
# R-051E - EXPORTAR SECRETOS DB PARA SIGUIENTE INSTALADOR
# =====================

DB_SECRETS_FILE="${DB_SECRETS_FILE:-/root/vigex-db-install-secrets.env}"

cat > "$DB_SECRETS_FILE" <<EOF
# Vigex DB install secrets
# No copiar este archivo al repositorio.
DB_NAME=${DB_NAME}
DB_SERVER_ID=${DB_SERVER_ID}
BACKUP_ALLOWED_HOST=${BACKUP_ALLOWED_HOST}
LOGS_ALLOWED_HOST=${LOGS_ALLOWED_HOST}
BACKUP_USER=${BACKUP_USER}
BACKUP_PASS=${BACKUP_PASS}
RESTORE_USER=${RESTORE_USER}
RESTORE_PASS=${RESTORE_PASS}
LOGS_DB_NAME=${LOGS_DB_NAME}
LOGS_DB_USER=${LOGS_DB_USER}
LOGS_DB_PASS=${LOGS_DB_PASS}
EOF

chown root:root "$DB_SECRETS_FILE"
chmod 600 "$DB_SECRETS_FILE"

echo "Secretos DB guardados en: ${DB_SECRETS_FILE}"
echo "Usar este fichero solo para preparar backup-services. No subirlo a Git."

echo "DB_NAME=${DB_NAME}"
echo "TEST_TABLE=${TEST_TABLE}"
echo "BACKUP_USER=${BACKUP_USER}"
echo "RESTORE_USER=${RESTORE_USER}"
echo "LOGS_DB_NAME=${LOGS_DB_NAME}"
echo "LOGS_DB_USER=${LOGS_DB_USER}"
echo "LOGS_ALLOWED_HOST=${LOGS_ALLOWED_HOST}"
echo "BACKUP_ALLOWED_HOST=${BACKUP_ALLOWED_HOST}"
echo "Binary logs: ${BINLOG_BASENAME}"
echo "Puerto SSH esperado: 22"
echo "Puerto MariaDB esperado: 3306"
echo "Usuario SSH para terminal: ${APP_USER}"
echo "============================================"
