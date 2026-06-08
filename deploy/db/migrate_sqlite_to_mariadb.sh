#!/usr/bin/env bash
# =============================================================================
# migrate_sqlite_to_mariadb.sh — Vigex Central
# R-087 / Ruta 12.4
#
# Migra la base de datos SQLite de Vigex Central a MariaDB.
# Solo necesario cuando la base de clientes crezca y SQLite no sea suficiente.
# Umbral orientativo: > 50 clientes activos o > 100.000 tickets.
#
# Uso:
#   sudo bash deploy/db/migrate_sqlite_to_mariadb.sh
#
# Requisitos:
#   - MariaDB/MySQL instalado y accesible
#   - python3, sqlite3 disponibles
#   - Ejecutar con acceso al fichero SQLite de Central Support
#   - Hacer un backup de central_support.db ANTES de ejecutar
# =============================================================================
set -euo pipefail

SQLITE_DB="${Vigex_SQLITE_PATH:-/opt/vigex/central-support/data/central_support.db}"
MARIADB_HOST="${Vigex_MARIADB_HOST:-127.0.0.1}"
MARIADB_PORT="${Vigex_MARIADB_PORT:-3306}"
MARIADB_USER="${Vigex_MARIADB_USER:-vigex_central}"
MARIADB_PASS="${Vigex_MARIADB_PASS:-}"
MARIADB_DB="${Vigex_MARIADB_DB:-vigex_central}"

RESET="\033[0m"; BOLD="\033[1m"; GREEN="\033[32m"; BLUE="\033[34m"
YELLOW="\033[33m"; RED="\033[31m"
info()    { echo -e "${BLUE}[INFO]${RESET}  $*"; }
ok()      { echo -e "${GREEN}[OK]${RESET}    $*"; }
warn()    { echo -e "${YELLOW}[AVISO]${RESET} $*"; }
error()   { echo -e "${RED}[ERROR]${RESET} $*"; }

echo ""
echo "  Vigex Central — Migración SQLite → MariaDB"
echo "  R-087 / Ruta 12.4"
echo ""

# ── Verificaciones previas ──────────────────────────────────────────────────

if [[ ! -f "${SQLITE_DB}" ]]; then
    error "No se encuentra la base de datos SQLite en: ${SQLITE_DB}"
    error "Ajusta Vigex_SQLITE_PATH si la ruta es diferente."
    exit 1
fi

if ! command -v python3 &>/dev/null; then
    error "python3 no está disponible."
    exit 1
fi

if ! command -v mysql &>/dev/null; then
    error "El cliente mysql no está disponible. Instálalo con: apt install mysql-client"
    exit 1
fi

if [[ -z "${MARIADB_PASS:-}" ]]; then
    read -rsp "Contraseña de MariaDB para usuario ${MARIADB_USER}: " MARIADB_PASS
    echo ""
fi

info "Base de datos origen:  ${SQLITE_DB}"
info "Base de datos destino: ${MARIADB_USER}@${MARIADB_HOST}:${MARIADB_PORT}/${MARIADB_DB}"
echo ""
warn "Esto es una operación IRREVERSIBLE en la BD destino."
warn "¿Has hecho un backup de ${SQLITE_DB}? (Se recomienda encarecidamente)"
echo ""
read -rp "Continuar [s/N]: " CONFIRMAR
if [[ "${CONFIRMAR,,}" != "s" ]]; then
    info "Operación cancelada."
    exit 0
fi

# ── Crear estructura en MariaDB ─────────────────────────────────────────────

info "Creando schema en MariaDB..."

mysql -h "${MARIADB_HOST}" -P "${MARIADB_PORT}" \
      -u "${MARIADB_USER}" -p"${MARIADB_PASS}" \
      "${MARIADB_DB}" << 'SQL'
CREATE TABLE IF NOT EXISTS central_clients (
    id VARCHAR(64) NOT NULL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    token VARCHAR(128) NOT NULL,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    fecha_alta DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS central_tickets (
    id VARCHAR(32) NOT NULL PRIMARY KEY,
    fecha_recepcion DATETIME NOT NULL,
    fecha_actualizacion DATETIME NOT NULL,
    cliente_id VARCHAR(64) NOT NULL,
    nombre_cliente VARCHAR(200) NOT NULL,
    ticket_local_id VARCHAR(64),
    tipo VARCHAR(50) NOT NULL,
    prioridad VARCHAR(20) NOT NULL,
    servicio VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    evidencia TEXT,
    contacto VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL,
    fecha_origen VARCHAR(50),
    version_panel VARCHAR(20),
    origen VARCHAR(50),
    estado VARCHAR(30) NOT NULL DEFAULT 'Nuevo',
    INDEX idx_cliente (cliente_id),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS central_ticket_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id VARCHAR(32) NOT NULL,
    fecha DATETIME NOT NULL,
    usuario VARCHAR(100) NOT NULL,
    accion VARCHAR(100) NOT NULL,
    valor_anterior VARCHAR(200),
    valor_nuevo VARCHAR(200),
    detalle TEXT,
    INDEX idx_ticket (ticket_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS central_heartbeats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id VARCHAR(64) NOT NULL,
    nombre_cliente VARCHAR(200) NOT NULL,
    fecha DATETIME NOT NULL,
    version_panel VARCHAR(20),
    disco_pct SMALLINT,
    backups_ok TINYINT,
    ultimo_backup VARCHAR(50),
    alertas_activas SMALLINT,
    servicios_activos SMALLINT,
    uptime_segundos INT,
    datos_extra TEXT,
    INDEX idx_cliente (cliente_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS central_audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME NOT NULL,
    usuario VARCHAR(100) NOT NULL,
    accion VARCHAR(100) NOT NULL,
    detalle TEXT,
    INDEX idx_usuario (usuario)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
SQL

ok "Schema creado en MariaDB."

# ── Exportar datos de SQLite a CSV y cargar en MariaDB ──────────────────────

TMPDIR_MIG="$(mktemp -d /tmp/vigex_migration_XXXXXX)"
trap "rm -rf ${TMPDIR_MIG}" EXIT

info "Exportando datos de SQLite..."

python3 << PYEOF
import sqlite3, csv, os

db_path = "${SQLITE_DB}"
tmpdir = "${TMPDIR_MIG}"

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row

tablas = [
    "central_clients",
    "central_tickets",
    "central_ticket_history",
    "central_heartbeats",
    "central_audit_log",
]

for tabla in tablas:
    try:
        rows = conn.execute(f"SELECT * FROM {tabla}").fetchall()
        if not rows:
            print(f"  {tabla}: vacía, se omite")
            continue
        out = os.path.join(tmpdir, f"{tabla}.csv")
        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow([d[0] for d in conn.execute(f"PRAGMA table_info({tabla})").fetchall()][1:])
            for row in rows:
                w.writerow(list(row)[1:] if tabla != "central_clients" else list(row))
        print(f"  {tabla}: {len(rows)} filas exportadas → {out}")
    except Exception as e:
        print(f"  {tabla}: no existe o error ({e}), se omite")

conn.close()
print("Exportación completada.")
PYEOF

ok "Exportación completada."

# Cargar cada CSV en MariaDB
for tabla in central_clients central_tickets central_ticket_history central_heartbeats central_audit_log; do
    CSV_FILE="${TMPDIR_MIG}/${tabla}.csv"
    if [[ ! -f "${CSV_FILE}" ]]; then
        info "  ${tabla}: sin datos, se omite"
        continue
    fi
    info "  Cargando ${tabla}..."
    mysql -h "${MARIADB_HOST}" -P "${MARIADB_PORT}" \
          -u "${MARIADB_USER}" -p"${MARIADB_PASS}" \
          --local-infile=1 \
          "${MARIADB_DB}" -e \
        "LOAD DATA LOCAL INFILE '${CSV_FILE}'
         INTO TABLE ${tabla}
         FIELDS TERMINATED BY ','
         OPTIONALLY ENCLOSED BY '\"'
         LINES TERMINATED BY '\n'
         IGNORE 1 ROWS;" 2>/dev/null || \
    warn "  ${tabla}: LOAD DATA LOCAL no disponible. Importa manualmente: ${CSV_FILE}"
done

ok "Migración completada."

# ── Verificación básica ─────────────────────────────────────────────────────

info "Verificación de recuentos..."

mysql -h "${MARIADB_HOST}" -P "${MARIADB_PORT}" \
      -u "${MARIADB_USER}" -p"${MARIADB_PASS}" \
      "${MARIADB_DB}" -e \
    "SELECT 'central_clients' AS tabla, COUNT(*) AS filas FROM central_clients
     UNION SELECT 'central_tickets', COUNT(*) FROM central_tickets
     UNION SELECT 'central_heartbeats', COUNT(*) FROM central_heartbeats
     UNION SELECT 'central_audit_log', COUNT(*) FROM central_audit_log;"

echo ""
ok "Migración SQLite → MariaDB completada."
echo ""
warn "SIGUIENTE PASO: Actualizar central-support para usar MariaDB en lugar de SQLite."
warn "Esto requiere reemplazar sqlite3 por pymysql en main.py (Fase 12)."
warn "Los CSVs de exportación están en: ${TMPDIR_MIG} (se eliminarán al salir)"
