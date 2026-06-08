#!/usr/bin/env bash
# update_vigex_api.sh — Actualiza Panel Vigex a una nueva versión sin perder datos
# R-065 / Rutas 8.1 + 8.3
# Uso: sudo bash update_vigex_api.sh
#
# Reemplaza : main.py · requirements.txt · templates/ · static/ · tools/ · config.env.example
# Preserva  : config.env · .ssh/ · data/ · reports/

set -euo pipefail

SERVICE_NAME="vigex-api"
INSTALL_DIR="/opt/vigex/api"
VENV_DIR="${INSTALL_DIR}/venv"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="${SCRIPT_DIR}/package"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
CODE_BACKUP_DIR="/opt/vigex/actualizacion_backup_${TIMESTAMP}"

# ── Verificaciones previas ──────────────────────────────────────────────────

if [[ "$EUID" -ne 0 ]]; then
  echo "ERROR: ejecuta este script con sudo."
  exit 1
fi

if [[ ! -d "$INSTALL_DIR" ]]; then
  echo "ERROR: Vigex no está instalado en ${INSTALL_DIR}."
  echo "       Usa install_vigex_api.sh para una instalación nueva."
  exit 1
fi

if [[ ! -d "$PACKAGE_DIR" ]]; then
  echo "ERROR: no se encuentra la carpeta package/ junto a este script."
  exit 1
fi

for required in main.py requirements.txt config.env.example templates static; do
  if [[ ! -e "${PACKAGE_DIR}/${required}" ]]; then
    echo "ERROR: falta ${required} en package/ — paquete incompleto."
    exit 1
  fi
done

APP_USER="$(stat -c '%U' "$INSTALL_DIR" 2>/dev/null || echo "${SUDO_USER:-$USER}")"

# ── Presentación ────────────────────────────────────────────────────────────

echo "==================================================================="
echo " Vigex — Actualización segura del panel"
echo "==================================================================="
echo "  Instalación actual : ${INSTALL_DIR}"
echo "  Usuario servicio   : ${APP_USER}"
echo "  Copia del código   : ${CODE_BACKUP_DIR}"
echo "==================================================================="
echo
echo "  Se actualizarán : main.py, templates/, static/, tools/, requirements.txt"
echo "  Se conservarán  : config.env, .ssh/, data/, reports/"
echo

if [[ -z "${Vigex_UPDATE_NONINTERACTIVE:-}" ]]; then
  read -rp "¿Continuar con la actualización? (S/N): " CONFIRM
  if [[ "${CONFIRM,,}" != "s" && "${CONFIRM,,}" != "si" ]]; then
    echo "Actualización cancelada."
    exit 0
  fi
fi

# ── Copia de seguridad del código actual ────────────────────────────────────

echo "==> Haciendo copia de seguridad del código actual"
mkdir -p "$CODE_BACKUP_DIR"
for item in main.py requirements.txt templates static tools config.env.example; do
  if [[ -e "${INSTALL_DIR}/${item}" ]]; then
    cp -r "${INSTALL_DIR}/${item}" "${CODE_BACKUP_DIR}/"
  fi
done
echo "==> Copia guardada en ${CODE_BACKUP_DIR}"

# ── Parar el servicio ────────────────────────────────────────────────────────

echo "==> Parando servicio ${SERVICE_NAME}"
systemctl stop "$SERVICE_NAME" 2>/dev/null || \
  echo "    AVISO: no se pudo parar el servicio (¿ya estaba parado?)"

# ── Copiar nuevos archivos de aplicación ────────────────────────────────────

echo "==> Copiando nuevos archivos de la aplicación"

# Ficheros sueltos
for item in main.py requirements.txt config.env.example; do
  cp "${PACKAGE_DIR}/${item}" "${INSTALL_DIR}/${item}"
done

# Directorios (reemplazar entero)
for dir in templates static tools; do
  if [[ -d "${PACKAGE_DIR}/${dir}" ]]; then
    rm -rf "${INSTALL_DIR:?}/${dir}"
    cp -r "${PACKAGE_DIR}/${dir}" "${INSTALL_DIR}/${dir}"
  fi
done

echo "==> Archivos de aplicación actualizados"

# ── Actualizar dependencias Python ───────────────────────────────────────────

echo "==> Actualizando dependencias Python"
if [[ -d "$VENV_DIR" ]]; then
  sudo -u "$APP_USER" "${VENV_DIR}/bin/pip" install --upgrade pip --quiet
  sudo -u "$APP_USER" "${VENV_DIR}/bin/pip" install -r "${INSTALL_DIR}/requirements.txt" --quiet
  echo "==> Dependencias actualizadas"
else
  echo "==> Entorno virtual no encontrado; creando uno nuevo"
  sudo -u "$APP_USER" python3 -m venv "$VENV_DIR"
  sudo -u "$APP_USER" "${VENV_DIR}/bin/pip" install --upgrade pip --quiet
  sudo -u "$APP_USER" "${VENV_DIR}/bin/pip" install -r "${INSTALL_DIR}/requirements.txt" --quiet
fi

# ── Ajustar permisos ─────────────────────────────────────────────────────────

echo "==> Ajustando permisos"
chown -R "${APP_USER}:${APP_USER}" "${INSTALL_DIR}"
chmod 640 "${INSTALL_DIR}/config.env"
chmod 700 "${INSTALL_DIR}/.ssh" 2>/dev/null || true
chmod 600 "${INSTALL_DIR}/.ssh/id_rsa_vigex" 2>/dev/null || true

for script in "${INSTALL_DIR}/tools/"*.sh "${INSTALL_DIR}/tools/"*.py; do
  [[ -f "$script" ]] && chmod 755 "$script" || true
done

# ── Recargar systemd y arrancar ──────────────────────────────────────────────

echo "==> Recargando configuración systemd"
systemctl daemon-reload

echo "==> Iniciando servicio"
systemctl start "$SERVICE_NAME"
sleep 2

# ── Verificación ─────────────────────────────────────────────────────────────

if systemctl is-active --quiet "$SERVICE_NAME"; then
  echo "==> Servicio activo correctamente"
else
  echo
  echo "ERROR: el servicio no arrancó después de la actualización."
  echo "       Diagnóstico: journalctl -u ${SERVICE_NAME} -n 50"
  echo "       Código anterior disponible en: ${CODE_BACKUP_DIR}"
  echo "       Para revertir: cp -r ${CODE_BACKUP_DIR}/. ${INSTALL_DIR}/ && systemctl start ${SERVICE_NAME}"
  exit 1
fi

curl -sSf -o /dev/null -w "==> Health check HTTP: %{http_code}\n" http://127.0.0.1:8000 || \
  echo "    AVISO: health check HTTP no respondió (puede necesitar unos segundos)"

# Limpiar copias de código antiguas (mantener las 5 más recientes)
BACKUP_COUNT="$(ls -1d /opt/vigex/actualizacion_backup_* 2>/dev/null | wc -l)"
if [[ "$BACKUP_COUNT" -gt 5 ]]; then
  ls -1dt /opt/vigex/actualizacion_backup_* | tail -n +6 | xargs rm -rf
  echo "==> Copias de actualización antiguas eliminadas (se mantienen las 5 más recientes)"
fi

echo
echo "==================================================================="
echo " Actualización completada correctamente"
echo " config.env, .ssh/, data/ y reports/ no han sido modificados."
echo " Código anterior preservado en: ${CODE_BACKUP_DIR}"
echo "==================================================================="
