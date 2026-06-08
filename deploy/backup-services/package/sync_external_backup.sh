#!/usr/bin/env bash
set -euo pipefail

# ==================================================
# Vigex
# R-028 / R-029 - Sincronización externa de backups
# Soporta:
#   - local / nas: destino montado en el sistema
#   - sftp: sincronización por rsync sobre SSH
#   - cifrado opcional con GPG simétrico
# ==================================================

SOURCE_DIR="${1:-${BACKUP_DIR:-/home/vigex/backups}}"
CONFIG_FILE="${2:-}"

if [[ -n "${CONFIG_FILE}" && -f "${CONFIG_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${CONFIG_FILE}"
fi

EXTERNAL_BACKUP_ENABLED="${EXTERNAL_BACKUP_ENABLED:-no}"
EXTERNAL_BACKUP_TYPE="${EXTERNAL_BACKUP_TYPE:-none}"
EXTERNAL_BACKUP_PATH="${EXTERNAL_BACKUP_PATH:-/mnt/vigex-external}"
EXTERNAL_BACKUP_ENCRYPTION="${EXTERNAL_BACKUP_ENCRYPTION:-none}"
EXTERNAL_SYNC_DELETE="${EXTERNAL_SYNC_DELETE:-no}"

EXTERNAL_SFTP_HOST="${EXTERNAL_SFTP_HOST:-}"
EXTERNAL_SFTP_PORT="${EXTERNAL_SFTP_PORT:-22}"
EXTERNAL_SFTP_USER="${EXTERNAL_SFTP_USER:-}"
EXTERNAL_SFTP_REMOTE_PATH="${EXTERNAL_SFTP_REMOTE_PATH:-}"

EXTERNAL_GPG_PASSPHRASE="${EXTERNAL_GPG_PASSPHRASE:-}"

log() {
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*"
}

fail() {
  echo "ERROR: $*" >&2
  exit 1
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "Falta el comando requerido: $1"
}

if [[ "${EXTERNAL_BACKUP_ENABLED}" != "yes" ]]; then
  log "Copia externa desactivada. EXTERNAL_BACKUP_ENABLED=${EXTERNAL_BACKUP_ENABLED}"
  exit 0
fi

if [[ ! -d "${SOURCE_DIR}" ]]; then
  fail "No existe el directorio origen de backups: ${SOURCE_DIR}"
fi

if [[ "${EXTERNAL_BACKUP_TYPE}" == "none" ]]; then
  fail "EXTERNAL_BACKUP_TYPE=none pero EXTERNAL_BACKUP_ENABLED=yes"
fi

require_cmd rsync

SYNC_SOURCE="${SOURCE_DIR}"
TMP_DIR=""

cleanup() {
  if [[ -n "${TMP_DIR}" && -d "${TMP_DIR}" ]]; then
    rm -rf "${TMP_DIR}"
  fi
}
trap cleanup EXIT

if [[ "${EXTERNAL_BACKUP_ENCRYPTION}" == "gpg" || "${EXTERNAL_BACKUP_ENCRYPTION}" == "gpg-symmetric" ]]; then
  require_cmd gpg

  if [[ -z "${EXTERNAL_GPG_PASSPHRASE}" ]]; then
    fail "Cifrado GPG activado pero EXTERNAL_GPG_PASSPHRASE está vacío"
  fi

  TMP_DIR="$(mktemp -d)"
  log "Cifrado activado. Preparando copias cifradas en ${TMP_DIR}"

  while IFS= read -r -d '' file; do
    rel="${file#${SOURCE_DIR}/}"
    out_dir="${TMP_DIR}/$(dirname "${rel}")"
    mkdir -p "${out_dir}"

    gpg --batch --yes --pinentry-mode loopback \
      --passphrase "${EXTERNAL_GPG_PASSPHRASE}" \
      -c \
      -o "${TMP_DIR}/${rel}.gpg" \
      "${file}"
  done < <(find "${SOURCE_DIR}" -type f -print0)

  SYNC_SOURCE="${TMP_DIR}"
elif [[ "${EXTERNAL_BACKUP_ENCRYPTION}" != "none" ]]; then
  fail "Tipo de cifrado no soportado: ${EXTERNAL_BACKUP_ENCRYPTION}"
fi

RSYNC_DELETE_OPT=""
if [[ "${EXTERNAL_SYNC_DELETE}" == "yes" ]]; then
  RSYNC_DELETE_OPT="--delete"
fi

case "${EXTERNAL_BACKUP_TYPE}" in
  local|nas)
    mkdir -p "${EXTERNAL_BACKUP_PATH}"
    log "Sincronizando backups hacia destino ${EXTERNAL_BACKUP_TYPE}: ${EXTERNAL_BACKUP_PATH}"
    rsync -av ${RSYNC_DELETE_OPT} "${SYNC_SOURCE}/" "${EXTERNAL_BACKUP_PATH}/"
    ;;

  sftp)
    if [[ -z "${EXTERNAL_SFTP_HOST}" || -z "${EXTERNAL_SFTP_USER}" || -z "${EXTERNAL_SFTP_REMOTE_PATH}" ]]; then
      fail "Para sftp hacen falta EXTERNAL_SFTP_HOST, EXTERNAL_SFTP_USER y EXTERNAL_SFTP_REMOTE_PATH"
    fi

    log "Sincronizando backups por SFTP/SSH hacia ${EXTERNAL_SFTP_USER}@${EXTERNAL_SFTP_HOST}:${EXTERNAL_SFTP_REMOTE_PATH}"
    rsync -av ${RSYNC_DELETE_OPT} \
      -e "ssh -p ${EXTERNAL_SFTP_PORT} -o StrictHostKeyChecking=accept-new" \
      "${SYNC_SOURCE}/" \
      "${EXTERNAL_SFTP_USER}@${EXTERNAL_SFTP_HOST}:${EXTERNAL_SFTP_REMOTE_PATH}/"
    ;;

  *)
    fail "EXTERNAL_BACKUP_TYPE no soportado: ${EXTERNAL_BACKUP_TYPE}"
    ;;
esac

log "OK: sincronización externa completada correctamente"