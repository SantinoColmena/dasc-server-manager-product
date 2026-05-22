#!/usr/bin/env bash
set -euo pipefail

TYPE="${1:-}"
DB="${2:-employees}"
DEST="${3:-/home/dasc/backups}"
NAME="${4:-}"
COMPRESS="${5:-gzip}"
RETENTION="${6:-30}"
BASE_REF="${7:-manual}"
NOTES="${8:-manual}"

HISTORY_DIR="${DEST}/.dasc"
HISTORY_FILE="${HISTORY_DIR}/history.tsv"
CHECKSUM_FILE="${HISTORY_DIR}/checksums.sha256"
COUNTER_FILE="${HISTORY_DIR}/next_id"

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

if [[ "$DEST" != /home/dasc/backups* ]]; then
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

mysqldump --defaults-extra-file="/home/dasc/.my.cnf" \
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

BASE_ID=""
if [[ "$TYPE" != "full" ]]; then
  BASE_ID="$(awk -F '\t' 'NR>1 && $3=="full" && $7=="OK" {id=$1} END{print id}' "$HISTORY_FILE")"
fi

TIMESTAMP="$(date -Iseconds)"
echo -e "${ID}\t${TIMESTAMP}\t${TYPE}\t${DB}\t${FINAL_FILE}\t${BASE_ID}\tOK\t${NOTES};sha256=${SHA256};size=${SIZE_BYTES}" >> "$HISTORY_FILE"

if [[ "$RETENTION" != "0" ]]; then
  find "$DEST" -maxdepth 1 -type f -name "*.sql*" -mtime +"$RETENTION" -delete || true
fi

echo "OK: Backup ${TYPE} creado en ${FINAL_FILE}"
echo "ID: ${ID}"
echo "SHA256: ${SHA256}"
echo "SIZE_BYTES: ${SIZE_BYTES}"
