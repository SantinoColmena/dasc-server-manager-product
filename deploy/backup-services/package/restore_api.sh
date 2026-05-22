#!/usr/bin/env bash
set -euo pipefail
shopt -s extglob

BACKUP_ID="${1:-}"
BACKUP_ROOT="${2:-/home/dasc/backups}"
CONFIRM="${3:-}"

HISTORY_FILE="${BACKUP_ROOT}/.dasc/history.tsv"
RESTORE_LOG="${BACKUP_ROOT}/.dasc/restore.log"
RESTORE_CNF="/home/dasc/.my_restore.cnf"

if [[ -z "$BACKUP_ID" ]]; then
  echo "ERROR: ID de backup obligatorio"
  exit 1
fi

if [[ "$CONFIRM" != "SI" ]]; then
  echo "ERROR: restauración cancelada. Confirmación requerida: SI"
  exit 1
fi

if [[ "$BACKUP_ID" != +([0-9]) ]]; then
  echo "ERROR: ID de backup no válido"
  exit 1
fi

if [[ "$BACKUP_ROOT" != /home/dasc/backups* ]]; then
  echo "ERROR: directorio de backups no permitido"
  exit 1
fi

if [[ ! -f "$HISTORY_FILE" ]]; then
  echo "ERROR: no existe historial de backups: $HISTORY_FILE"
  exit 1
fi

if [[ ! -f "$RESTORE_CNF" ]]; then
  echo "ERROR: no existe fichero de credenciales restore: $RESTORE_CNF"
  exit 1
fi

line="$(awk -F '\t' -v id="$BACKUP_ID" 'NR>1 && $1 == id {print $0}' "$HISTORY_FILE" | tail -n1)"

if [[ -z "$line" ]]; then
  echo "ERROR: no existe backup con ID=${BACKUP_ID}"
  exit 1
fi

IFS=$'\t' read -r id timestamp type db path base_id status notes <<< "$line"

if [[ "$status" != "OK" ]]; then
  echo "ERROR: el backup ID=${BACKUP_ID} no tiene estado OK"
  exit 1
fi

if [[ -z "$path" ]]; then
  echo "ERROR: el backup ID=${BACKUP_ID} no tiene ruta asociada"
  exit 1
fi

normalized="$(readlink -m "$path")"
allowed_root="$(readlink -m "$BACKUP_ROOT")"

case "$normalized" in
  "$allowed_root"/*) ;;
  *)
    echo "ERROR: ruta de backup fuera del directorio permitido"
    exit 1
    ;;
esac

if [[ ! -f "$normalized" ]]; then
  echo "ERROR: no existe el fichero de backup: $normalized"
  exit 1
fi

mkdir -p "$(dirname "$RESTORE_LOG")"

echo "[$(date -Iseconds)] INICIO restore id=${BACKUP_ID} db=${db} file=${normalized}" >> "$RESTORE_LOG"

if [[ "$normalized" == *.gz ]]; then
  gzip -dc "$normalized" | mysql --defaults-extra-file="$RESTORE_CNF" --protocol=tcp
else
  mysql --defaults-extra-file="$RESTORE_CNF" --protocol=tcp < "$normalized"
fi

echo "[$(date -Iseconds)] OK restore id=${BACKUP_ID} db=${db} file=${normalized}" >> "$RESTORE_LOG"

echo "OK: Restauración completada"
echo "ID: ${BACKUP_ID}"
echo "BD: ${db}"
echo "Archivo: ${normalized}"
