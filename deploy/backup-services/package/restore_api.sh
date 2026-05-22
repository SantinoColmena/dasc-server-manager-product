#!/usr/bin/env bash
set -euo pipefail
shopt -s extglob

BACKUP_ID="${1:-}"
BACKUP_ROOT="${2:-/home/dasc/backups}"
CONFIRM="${3:-}"

HISTORY_FILE="${BACKUP_ROOT}/.dasc/history.tsv"
CHECKSUM_FILE="${BACKUP_ROOT}/.dasc/checksums.sha256"
RESTORE_LOG="${BACKUP_ROOT}/.dasc/restore.log"
AUDIT_LOG="${BACKUP_ROOT}/.dasc/audit.log"
RESTORE_CNF="/home/dasc/.my_restore.cnf"


audit_log() {
  local action="$1"
  local result="$2"
  shift 2 || true

  mkdir -p "$(dirname "$AUDIT_LOG")"

  {
    printf 'timestamp=%s action=%s result=%s' "$(date -Iseconds)" "$action" "$result"

    local item
    for item in "$@"; do
      item="${item//$'\n'/ }"
      item="${item//$'\r'/ }"
      printf ' %s' "$item"
    done

    printf '\n'
  } >> "$AUDIT_LOG"
}

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

if [[ ! -f "$CHECKSUM_FILE" ]]; then
  echo "ERROR: no existe manifiesto de integridad: $CHECKSUM_FILE"
  exit 1
fi

expected_sha=""
while read -r hash file_path; do
  if [[ "${file_path:-}" == "$normalized" ]]; then
    expected_sha="$hash"
  fi
done < "$CHECKSUM_FILE"

if [[ -z "$expected_sha" ]]; then
  echo "ERROR: el backup no tiene checksum registrado"
  exit 1
fi

actual_sha="$(sha256sum "$normalized" | awk '{print $1}')"

if [[ "$actual_sha" != "$expected_sha" ]]; then
  echo "ERROR: integridad fallida. SHA256 esperado=${expected_sha} actual=${actual_sha}"
  echo "[$(date -Iseconds)] ERROR integridad id=${BACKUP_ID} file=${normalized}" >> "$RESTORE_LOG"
  audit_log "backup.integrity" "ERROR" "id=${BACKUP_ID}" "file=${normalized}" "expected_sha=${expected_sha}" "actual_sha=${actual_sha}"
  exit 1
fi

if [[ "$normalized" == *.gz ]]; then
  gzip -t "$normalized" || {
    echo "ERROR: el fichero comprimido no supera gzip -t"
    echo "[$(date -Iseconds)] ERROR gzip id=${BACKUP_ID} file=${normalized}" >> "$RESTORE_LOG"
    audit_log "backup.integrity" "ERROR" "id=${BACKUP_ID}" "file=${normalized}" "reason=gzip_test_failed"
    exit 1
  }
fi

echo "[$(date -Iseconds)] INTEGRIDAD OK id=${BACKUP_ID} sha256=${actual_sha} file=${normalized}" >> "$RESTORE_LOG"
audit_log "backup.integrity" "OK" "id=${BACKUP_ID}" "sha256=${actual_sha}" "file=${normalized}"


echo "[$(date -Iseconds)] INICIO restore id=${BACKUP_ID} db=${db} file=${normalized}" >> "$RESTORE_LOG"
audit_log "backup.restore.start" "OK" "id=${BACKUP_ID}" "db=${db}" "file=${normalized}"

if [[ "$normalized" == *.gz ]]; then
  if ! gzip -dc "$normalized" | mysql --defaults-extra-file="$RESTORE_CNF" --protocol=tcp; then
    echo "[$(date -Iseconds)] ERROR restore id=${BACKUP_ID} db=${db} file=${normalized}" >> "$RESTORE_LOG"
    audit_log "backup.restore" "ERROR" "id=${BACKUP_ID}" "db=${db}" "file=${normalized}"
    exit 1
  fi
else
  if ! mysql --defaults-extra-file="$RESTORE_CNF" --protocol=tcp < "$normalized"; then
    echo "[$(date -Iseconds)] ERROR restore id=${BACKUP_ID} db=${db} file=${normalized}" >> "$RESTORE_LOG"
    audit_log "backup.restore" "ERROR" "id=${BACKUP_ID}" "db=${db}" "file=${normalized}"
    exit 1
  fi
fi

echo "[$(date -Iseconds)] OK restore id=${BACKUP_ID} db=${db} file=${normalized}" >> "$RESTORE_LOG"
audit_log "backup.restore" "OK" "id=${BACKUP_ID}" "db=${db}" "file=${normalized}"

echo "OK: Restauración completada"
echo "ID: ${BACKUP_ID}"
echo "BD: ${db}"
echo "Archivo: ${normalized}"
