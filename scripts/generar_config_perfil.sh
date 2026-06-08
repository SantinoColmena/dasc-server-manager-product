#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROFILES_DIR="${ROOT_DIR}/config/perfiles"
DEST_CONFIG="${DEST_CONFIG:-${ROOT_DIR}/config.env}"

print_menu() {
  echo "============================================"
  echo "Vigex - Asistente de perfil"
  echo "============================================"
  echo
  echo "Selecciona el perfil de despliegue:"
  echo
  echo "1) single      - Vigex Lite / 1 servidor"
  echo "2) dual        - Vigex PyME / 2 servidores"
  echo "3) distributed - Vigex Pro / 3 servidores"
  echo
}

normalize_profile() {
  case "$1" in
    1|single|lite|Lite|SINGLE)
      echo "single"
      ;;
    2|dual|pyme|PyME|PYME|DUAL)
      echo "dual"
      ;;
    3|distributed|pro|Pro|DISTRIBUTED)
      echo "distributed"
      ;;
    *)
      echo ""
      ;;
  esac
}

PROFILE_INPUT="${1:-}"

if [[ -z "${PROFILE_INPUT}" ]]; then
  print_menu
  echo
  read -rp "Opción: " PROFILE_INPUT
fi

PROFILE="$(normalize_profile "${PROFILE_INPUT}")"

if [[ -z "${PROFILE}" ]]; then
  echo "ERROR: perfil no válido."
  echo "Usa: single, dual o distributed."
  exit 1
fi

SOURCE_CONFIG="${PROFILES_DIR}/config.${PROFILE}.env.example"

if [[ ! -f "${SOURCE_CONFIG}" ]]; then
  echo "ERROR: no existe la plantilla ${SOURCE_CONFIG}"
  exit 1
fi

echo
echo "Perfil seleccionado: ${PROFILE}"
echo "Plantilla origen: ${SOURCE_CONFIG}"
echo "Archivo destino: ${DEST_CONFIG}"
echo

if [[ -f "${DEST_CONFIG}" ]]; then
  BACKUP_FILE="${DEST_CONFIG}.bak.$(date +'%Y%m%d-%H%M%S')"
  cp "${DEST_CONFIG}" "${BACKUP_FILE}"
  echo "Se ha creado copia de seguridad del config.env anterior:"
  echo "${BACKUP_FILE}"
fi

cp "${SOURCE_CONFIG}" "${DEST_CONFIG}"
chmod 600 "${DEST_CONFIG}" 2>/dev/null || true

echo
echo "config.env generado correctamente."

case "${PROFILE}" in
  single)
    echo
    echo "AVISO IMPORTANTE:"
    echo "El perfil single/Lite requiere copia externa obligatoria."
    echo "Revisa EXTERNAL_BACKUP_REQUIRED y EXTERNAL_BACKUP_ENABLED."
    ;;
  dual)
    echo
    echo "Perfil recomendado para PyMEs."
    echo "Revisa las IPs de DB_HOST, BACKUPS_HOST y LOGS_DB_HOST."
    ;;
  distributed)
    echo
    echo "Perfil Pro/distribuido."
    echo "Revisa la separación entre API, DB y Backups."
    ;;
esac

echo
echo "Siguiente paso:"
echo "Edita ${DEST_CONFIG} y cambia contraseñas, IPs y rutas antes de instalar."
echo "============================================"
