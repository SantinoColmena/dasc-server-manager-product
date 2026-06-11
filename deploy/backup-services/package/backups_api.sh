#!/usr/bin/env bash
set -euo pipefail

TYPE="${1:-}"
DB="${2:-employees}"
DEST="${3:-/home/vigex/backups}"
NAME="${4:-}"
COMPRESS="${5:-gzip}"
RETENTION="${6:-30}"
BASE_REF="${7:-manual}"
NOTES="${8:-manual}"

HISTORY_DIR="${DEST}/.vigex"
HISTORY_FILE="${HISTORY_DIR}/history.tsv"
CHECKSUM_FILE="${HISTORY_DIR}/checksums.sha256"
AUDIT_LOG="${HISTORY_DIR}/audit.log"
COUNTER_FILE="${HISTORY_DIR}/next_id"



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

safe_retention_cleanup() {
  local dest="$1"
  local retention_days="$2"
  local history_file="$3"
  local checksum_file="$4"

  if [[ "$retention_days" == "0" ]]; then
    echo "INFO: Retención desactivada"
    return 0
  fi

  if [[ "$dest" != /home/vigex/backups* ]]; then
    echo "ERROR: retención cancelada, destino no permitido: $dest"
    return 1
  fi

  if [[ ! "$retention_days" =~ ^[0-9]+$ ]]; then
    echo "ERROR: retención no válida: $retention_days"
    return 1
  fi

  if [[ ! -f "$history_file" ]]; then
    echo "INFO: no existe historial, no se aplica retención"
    return 0
  fi

  local now_epoch
  now_epoch="$(date +%s)"
  local cutoff_epoch
  cutoff_epoch="$((now_epoch - retention_days * 86400))"

  local tmp_history
  tmp_history="${history_file}.tmp"
  local pruned_ids
  pruned_ids="$(mktemp)"

  awk -F '\t' -v cutoff="$cutoff_epoch" -v pruned_ids="$pruned_ids" '
    BEGIN { OFS = FS }

    NR == 1 {
      print $0
      next
    }

    {
      id=$1
      timestamp=$2
      type=$3
      db=$4
      path=$5
      base_id=$6
      status=$7
      notes=$8

      cmd = "date -d \"" timestamp "\" +%s 2>/dev/null"
      cmd | getline ts_epoch
      close(cmd)

      old = 0
      if (ts_epoch != "" && ts_epoch < cutoff) {
        old = 1
      }

      if (status == "OK" && old == 1) {
        candidate[id] = 1
        rows[id] = $0
        paths[id] = path
        next
      }

      if (status == "OK" && base_id != "") {
        referenced[base_id] = 1
      }

      print $0
    }

    END {
      for (id in candidate) {
        if (referenced[id]) {
          print rows[id]
        } else {
          split(rows[id], cols, FS)
          cols[7] = "PRUNED"
          cols[8] = cols[8] ";pruned_at=" strftime("%Y-%m-%dT%H:%M:%S%z")
          print cols[1], cols[2], cols[3], cols[4], cols[5], cols[6], cols[7], cols[8]
          print id "\t" paths[id] >> pruned_ids
        }
      }
    }
  ' "$history_file" > "$tmp_history"

  mv "$tmp_history" "$history_file"

  while IFS=$'\t' read -r id file_path; do
    [[ -z "${file_path:-}" ]] && continue

    local normalized
    normalized="$(readlink -m "$file_path")"
    local allowed_root
    allowed_root="$(readlink -m "$dest")"

    case "$normalized" in
      "$allowed_root"/*)
        if [[ -f "$normalized" ]]; then
          rm -f "$normalized"
          echo "INFO: backup purgado por retención segura: ID=${id} PATH=${normalized}"
          audit_log "backup.prune" "OK" "id=${id}" "file=${normalized}" "retention_days=${retention_days}"
        fi

        if [[ -f "$checksum_file" ]]; then
          local tmp_checksum
          tmp_checksum="${checksum_file}.tmp"
          grep -vF "  ${normalized}" "$checksum_file" > "$tmp_checksum" || true
          mv "$tmp_checksum" "$checksum_file"
        fi
        ;;
      *)
        echo "AVISO: no se elimina ruta fuera del directorio permitido: $normalized"
        audit_log "backup.prune" "WARNING" "file=${normalized}" "reason=outside_allowed_root"
        ;;
    esac
  done < "$pruned_ids"

  rm -f "$pruned_ids"
}

if [[ -z "$TYPE" ]]; then
  echo "ERROR: tipo de backup obligatorio"
  exit 1
fi

case "$TYPE" in
  full|incremental|differential) ;;
  *)
    echo "ERROR: tipo de backup no permitido: $TYPE"
    exit 1
    ;;
esac

# Seguridad (auditoría 2026-06-11): un nombre de BD que empiece por '-' podría
# interpretarse como una opción de mysqldump. Lo rechazamos explícitamente.
if [[ "$DB" == -* ]]; then
  echo "ERROR: nombre de base de datos no permitido"
  exit 1
fi

if [[ "$DEST" != /home/vigex/backups* ]]; then
  echo "ERROR: destino no permitido"
  exit 1
fi

if [[ -z "$NAME" ]]; then
  NAME="${DB}-${TYPE}-$(date +'%Y%m%d-%H%M%S').sql"
fi

SAFE_NAME="$(basename "$NAME")"
SAFE_NAME="${SAFE_NAME// /_}"
SAFE_NAME="${SAFE_NAME//;/_}"
SAFE_NAME="${SAFE_NAME//|/_}"
SAFE_NAME="${SAFE_NAME//&/_}"

DATE_STAMP="$(date +'%Y%m%d')"
TIME_STAMP="$(date +'%H%M')"
TIME_STAMP_SECONDS="$(date +'%H%M%S')"
FULL_TIMESTAMP="$(date +'%Y%m%d-%H%M%S')"

SAFE_NAME="${SAFE_NAME//YYYYMMDD/$DATE_STAMP}"
SAFE_NAME="${SAFE_NAME//HHMMSS/$TIME_STAMP_SECONDS}"
SAFE_NAME="${SAFE_NAME//HHMM/$TIME_STAMP}"
SAFE_NAME="${SAFE_NAME//TIMESTAMP/$FULL_TIMESTAMP}"

mkdir -p "$DEST" "$HISTORY_DIR"

if [[ ! -f "$COUNTER_FILE" ]]; then
  echo "1" > "$COUNTER_FILE"
fi

ID="$(cat "$COUNTER_FILE")"
NEXT_ID="$((ID + 1))"
echo "$NEXT_ID" > "$COUNTER_FILE"

if [[ ! -f "$HISTORY_FILE" ]]; then
  echo -e "id\ttimestamp\ttype\tdb\tpath\tbase_id\tstatus\tnotes" > "$HISTORY_FILE"
fi

OUTFILE="${DEST}/${SAFE_NAME}"

if [[ "$OUTFILE" != *.sql && "$OUTFILE" != *.sql.gz ]]; then
  OUTFILE="${OUTFILE}.sql"
fi

TMP_SQL="$OUTFILE"
if [[ "$TMP_SQL" == *.gz ]]; then
  TMP_SQL="${TMP_SQL%.gz}"
fi

mysqldump --defaults-extra-file="/home/vigex/.my.cnf" \
  --protocol=tcp \
  --single-transaction \
  --routines \
  --events \
  --triggers \
  --databases "$DB" > "$TMP_SQL"

FINAL_FILE="$TMP_SQL"
if [[ "$COMPRESS" == "gzip" ]]; then
  gzip -f "$TMP_SQL"
  FINAL_FILE="${TMP_SQL}.gz"
elif [[ "$COMPRESS" == "none" ]]; then
  FINAL_FILE="$TMP_SQL"
else
  echo "ERROR: compresión no permitida"
  rm -f "$TMP_SQL"
  exit 1
fi

if [[ ! -s "$FINAL_FILE" ]]; then
  echo "ERROR: el fichero de backup no existe o está vacío"
  rm -f "$FINAL_FILE"
  exit 1
fi

if [[ "$FINAL_FILE" == *.gz ]]; then
  gzip -t "$FINAL_FILE" || {
    echo "ERROR: el backup comprimido no supera gzip -t"
    exit 1
  }
fi

SHA256="$(sha256sum "$FINAL_FILE" | awk '{print $1}')"
SIZE_BYTES="$(wc -c < "$FINAL_FILE" | tr -d '[:space:]')"

touch "$CHECKSUM_FILE"
TMP_MANIFEST="${CHECKSUM_FILE}.tmp"
grep -vF "  ${FINAL_FILE}" "$CHECKSUM_FILE" > "$TMP_MANIFEST" || true
mv "$TMP_MANIFEST" "$CHECKSUM_FILE"
echo "${SHA256}  ${FINAL_FILE}" >> "$CHECKSUM_FILE"
audit_log "backup.integrity" "OK" "id=${ID}" "sha256=${SHA256}" "size=${SIZE_BYTES}" "file=${FINAL_FILE}"

BASE_ID=""
if [[ "$TYPE" != "full" ]]; then
  BASE_ID="$(awk -F '\t' 'NR>1 && $3=="full" && $7=="OK" {id=$1} END{print id}' "$HISTORY_FILE")"
fi

TIMESTAMP="$(date -Iseconds)"
# Saneado (auditoría 2026-06-11, FINDING-3): DB y NOTES pueden originarse en el
# panel; un salto de línea o tabulador corrompería el TSV de historial (y, vía
# 'echo -e', un backslash se interpretaría). Neutralizamos esos caracteres a
# espacios y escribimos con printf para tratar el contenido de forma literal.
DB_SAFE="${DB//$'\n'/ }";       DB_SAFE="${DB_SAFE//$'\r'/ }";       DB_SAFE="${DB_SAFE//$'\t'/ }"
NOTES_SAFE="${NOTES//$'\n'/ }"; NOTES_SAFE="${NOTES_SAFE//$'\r'/ }"; NOTES_SAFE="${NOTES_SAFE//$'\t'/ }"
printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
  "${ID}" "${TIMESTAMP}" "${TYPE}" "${DB_SAFE}" "${FINAL_FILE}" "${BASE_ID}" "OK" \
  "${NOTES_SAFE};sha256=${SHA256};size=${SIZE_BYTES}" >> "$HISTORY_FILE"
audit_log "backup.create" "OK" "id=${ID}" "type=${TYPE}" "db=${DB}" "file=${FINAL_FILE}" "sha256=${SHA256}" "size=${SIZE_BYTES}"

safe_retention_cleanup "$DEST" "$RETENTION" "$HISTORY_FILE" "$CHECKSUM_FILE"

echo "OK: Backup ${TYPE} creado en ${FINAL_FILE}"
echo "ID: ${ID}"
echo "SHA256: ${SHA256}"
echo "SIZE_BYTES: ${SIZE_BYTES}"
