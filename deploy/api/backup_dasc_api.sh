#!/usr/bin/env bash
# backup_dasc_api.sh — Copia de seguridad de la propia instalación DASC
# R-066 / Ruta 8.4
# Uso: sudo bash backup_dasc_api.sh [directorio_destino]
#
# Incluye: config.env · data/ (BD, usuarios) · .ssh/ (claves) · code/
# Excluye: venv/ (regenerable con pip install)

set -euo pipefail

INSTALL_DIR="/opt/dasc/api"
DEFAULT_BACKUP_DIR="/opt/dasc/backups_panel"
BACKUP_DIR="${1:-$DEFAULT_BACKUP_DIR}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
ARCHIVE="${BACKUP_DIR}/dasc_panel_backup_${TIMESTAMP}.tar.gz"
MAX_BACKUPS=10

# ── Verificaciones ───────────────────────────────────────────────────────────

if [[ "$EUID" -ne 0 ]]; then
  echo "ERROR: ejecuta este script con sudo."
  exit 1
fi

if [[ ! -d "$INSTALL_DIR" ]]; then
  echo "ERROR: DASC no está instalado en ${INSTALL_DIR}."
  exit 1
fi

mkdir -p "$BACKUP_DIR"
chmod 700 "$BACKUP_DIR"

echo "==================================================================="
echo " DASC — Copia de seguridad del panel"
echo "==================================================================="
echo "  Origen : ${INSTALL_DIR}"
echo "  Destino: ${ARCHIVE}"
echo "==================================================================="

# ── Crear archivo comprimido ─────────────────────────────────────────────────
# Excluimos el venv (grande, regenerable) y los backups de actualización

echo "==> Creando archivo de copia de seguridad"
tar -czf "$ARCHIVE" \
  --exclude="api/venv" \
  --exclude="api/actualizacion_backup_*" \
  -C "$(dirname "$INSTALL_DIR")" \
  "$(basename "$INSTALL_DIR")" \
  2>/dev/null

SIZE="$(du -sh "$ARCHIVE" 2>/dev/null | cut -f1)"
echo "==> Archivo creado: ${ARCHIVE} (${SIZE})"

# ── Limpieza automática (mantener las N más recientes) ───────────────────────

BACKUP_COUNT="$(ls -1 "${BACKUP_DIR}"/dasc_panel_backup_*.tar.gz 2>/dev/null | wc -l)"
if [[ "$BACKUP_COUNT" -gt "$MAX_BACKUPS" ]]; then
  REMOVED="$(( BACKUP_COUNT - MAX_BACKUPS ))"
  ls -1t "${BACKUP_DIR}"/dasc_panel_backup_*.tar.gz | tail -n "+$(( MAX_BACKUPS + 1 ))" | xargs rm -f
  echo "==> ${REMOVED} copia(s) antigua(s) eliminada(s) (se mantienen las ${MAX_BACKUPS} más recientes)"
fi

# ── Instrucciones de restauración ────────────────────────────────────────────

echo
echo "==================================================================="
echo " Copia completada: ${ARCHIVE}"
echo
echo " Para restaurar:"
echo "   1. sudo systemctl stop dasc-api"
echo "   2. sudo tar -xzf ${ARCHIVE} -C $(dirname "$INSTALL_DIR")"
echo "   3. cd ${INSTALL_DIR} && sudo -u \$(stat -c '%U' ${INSTALL_DIR}) \\"
echo "        ./venv/bin/pip install -r requirements.txt  # si el venv no existe"
echo "   4. sudo systemctl start dasc-api"
echo "==================================================================="
