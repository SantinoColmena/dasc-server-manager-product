#!/usr/bin/env bash
set -euo pipefail
shopt -s extglob

BACKUP_ID="${1:-}"
BACKUP_ROOT="${2:-/home/dasc/backups}"

HISTORY_FILE="${BACKUP_ROOT}/.dasc/history.tsv"
CHECKSUM_FILE="${BACKUP_ROOT}/.dasc/checksums.sha256"
AUDIT_LOG="${BACKUP_ROOT}/.dasc/audit.log"
DRILL_LOG="${BACKUP_ROOT}/.dasc/restore_drill.log"

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

fail() {
  local msg="$1"
  echo "ERROR: $msg"
  audit_log "backup.restore_drill" "ERROR" "id=${BACKUP_ID}" "reason=${msg}"
  echo "[$(date -Iseconds)] ERROR id=${BACKUP_ID} reason=${msg}" >> "$DRILL_LOG"
  exit 1
}

if [[ -z "$BACKUP_ID" ]]; then
  fail "ID de backup obligatorio"
fi

if [[ "$BACKUP_ID" != +([0-9]) ]]; then
  fail "ID de backup no válido"
fi

if [[ "$BACKUP_ROOT" != /home/dasc/backups* ]]; then
  fail "directorio de backups no permitido"
fi

mkdir -p "$(dirname "$DRILL_LOG")"

if [[ ! -f "$HISTORY_FILE" ]]; then
  fail "no existe history.tsv"
fi

if [[ ! -f "$CHECKSUM_FILE" ]]; then
  fail "no existe checksums.sha256"
fi

line="$(awk -F '\t' -v id="$BACKUP_ID" 'NR>1 && $1 == id {print $0}' "$HISTORY_FILE" | tail -n1)"

if [[ -z "$line" ]]; then
  fail "no existe backup con ese ID"
fi

id="$(awk -F '\t' '{print $1}' <<< "$line")"
timestamp="$(awk -F '\t' '{print $2}' <<< "$line")"
type="$(awk -F '\t' '{print $3}' <<< "$line")"
db="$(awk -F '\t' '{print $4}' <<< "$line")"
path="$(awk -F '\t' '{print $5}' <<< "$line")"
base_id="$(awk -F '\t' '{print $6}' <<< "$line")"
status="$(awk -F '\t' '{print $7}' <<< "$line")"
notes="$(awk -F '\t' '{print $8}' <<< "$line")"

if [[ "$status" != "OK" ]]; then
  fail "el backup no está en estado OK"
fi

if [[ -z "$path" ]]; then
  fail "el backup no tiene ruta asociada"
fi

normalized="$(readlink -m "$path")"
allowed_root="$(readlink -m "$BACKUP_ROOT")"

case "$normalized" in
  "$allowed_root"/*) ;;
  *)
    fail "ruta fuera del directorio permitido"
    ;;
esac

if [[ ! -f "$normalized" ]]; then
  fail "no existe el fichero físico"
fi

if [[ ! -s "$normalized" ]]; then
  fail "el fichero existe pero está vacío"
fi

expected_sha=""
while read -r hash file_path; do
  if [[ "${file_path:-}" == "$normalized" ]]; then
    expected_sha="$hash"
  fi
done < "$CHECKSUM_FILE"

if [[ -z "$expected_sha" ]]; then
  fail "no hay checksum registrado"
fi

actual_sha="$(sha256sum "$normalized" | awk '{print $1}')"

if [[ "$actual_sha" != "$expected_sha" ]]; then
  fail "sha256 no coincide"
fi

if [[ "$normalized" == *.gz ]]; then
  gzip -t "$normalized" || fail "gzip -t falló"
  if ! gzip -dc "$normalized" | head -n 20 >/dev/null; then
    fail "no se puede leer el SQL comprimido"
  fi
else
  if ! head -n 20 "$normalized" >/dev/null; then
    fail "no se puede leer el SQL"
  fi
fi

audit_log "backup.restore_drill" "OK" "id=${BACKUP_ID}" "db=${db}" "type=${type}" "file=${normalized}" "sha256=${actual_sha}"
echo "[$(date -Iseconds)] OK id=${BACKUP_ID} db=${db} type=${type} file=${normalized}" >> "$DRILL_LOG"

echo "OK: Simulacro de recuperación validado"
echo "ID: ${BACKUP_ID}"
echo "BD: ${db}"
echo "Tipo: ${type}"
echo "Archivo: ${normalized}"
echo "SHA256: ${actual_sha}"
