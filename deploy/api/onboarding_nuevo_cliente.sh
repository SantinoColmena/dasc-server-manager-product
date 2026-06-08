#!/usr/bin/env bash
# =============================================================================
# onboarding_nuevo_cliente.sh — DASC Server Manager
# R-084 / Ruta 11.1
#
# Asistente de onboarding técnico para un nuevo cliente.
# Genera la config.env personalizada y lanza el instalador.
#
# Uso:
#   sudo bash deploy/api/onboarding_nuevo_cliente.sh
#   O con variables ya definidas:
#   DASC_CLIENTE_NOMBRE="Empresa S.L." DASC_PERFIL=standard \
#     sudo bash deploy/api/onboarding_nuevo_cliente.sh
#
# Requisitos:
#   - Ejecutar en el servidor API del cliente (Ubuntu 22.04)
#   - El repo debe estar disponible localmente
#   - python3 disponible para generar hash bcrypt
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="${SCRIPT_DIR}/package"

# ── Colores ──────────────────────────────────────────────────────────────────
RESET="\033[0m"
BOLD="\033[1m"
GREEN="\033[32m"
BLUE="\033[34m"
YELLOW="\033[33m"
RED="\033[31m"

info()    { echo -e "${BLUE}[INFO]${RESET}  $*"; }
ok()      { echo -e "${GREEN}[OK]${RESET}    $*"; }
warn()    { echo -e "${YELLOW}[AVISO]${RESET} $*"; }
error()   { echo -e "${RED}[ERROR]${RESET} $*"; }
section() { echo -e "\n${BOLD}${BLUE}═══════════════════════════════════════════${RESET}"; \
            echo -e "${BOLD}${BLUE}  $*${RESET}"; \
            echo -e "${BOLD}${BLUE}═══════════════════════════════════════════${RESET}\n"; }

# ── Banner ───────────────────────────────────────────────────────────────────
echo ""
echo "  ██████╗  █████╗ ███████╗ ██████╗"
echo "  ██╔══██╗██╔══██╗██╔════╝██╔════╝"
echo "  ██║  ██║███████║███████╗██║"
echo "  ██║  ██║██╔══██║╚════██║██║"
echo "  ██████╔╝██║  ██║███████║╚██████╗"
echo "  ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝  Onboarding nuevo cliente"
echo ""

# ── Paso 1: Datos del cliente ────────────────────────────────────────────────
section "PASO 1 — Datos del cliente"

if [[ -z "${DASC_CLIENTE_NOMBRE:-}" ]]; then
    read -rp "Nombre del cliente (p.ej. 'Talleres García S.L.'): " DASC_CLIENTE_NOMBRE
fi
if [[ -z "${DASC_CLIENTE_NOMBRE:-}" ]]; then
    error "El nombre del cliente es obligatorio."; exit 1
fi

# Normalizar para usar como ID
DASC_CLIENTE_ID="${DASC_CLIENTE_NOMBRE,,}"  # minúsculas
DASC_CLIENTE_ID="${DASC_CLIENTE_ID// /-}"   # espacios → guiones
DASC_CLIENTE_ID="${DASC_CLIENTE_ID//[^a-z0-9\-]/}"  # solo alfanumérico y guiones
DASC_CLIENTE_ID="${DASC_CLIENTE_ID:0:30}"   # máximo 30 chars
info "ID del cliente: ${DASC_CLIENTE_ID}"

# ── Paso 2: Perfil de despliegue ─────────────────────────────────────────────
section "PASO 2 — Perfil de despliegue"

if [[ -z "${DASC_PERFIL:-}" ]]; then
    echo "Perfiles disponibles:"
    echo "  lite     — 1 servidor + copia externa (recomendado para PyME pequeña)"
    echo "  standard — 2 servidores: API/backups + DB/logs (recomendado)"
    echo "  pro      — 3 servidores: API / DB / backups"
    echo ""
    read -rp "Perfil [lite/standard/pro, defecto: standard]: " DASC_PERFIL
    DASC_PERFIL="${DASC_PERFIL:-standard}"
fi

case "${DASC_PERFIL}" in
    lite|standard|pro) ok "Perfil seleccionado: ${DASC_PERFIL}" ;;
    *) error "Perfil no reconocido: ${DASC_PERFIL}. Usa lite, standard o pro."; exit 1 ;;
esac

# ── Paso 3: IPs de los servidores ────────────────────────────────────────────
section "PASO 3 — IPs de los servidores"

read -rp "IP del servidor API/panel (este servidor) [127.0.0.1]: " IP_API
IP_API="${IP_API:-127.0.0.1}"

if [[ "${DASC_PERFIL}" == "standard" || "${DASC_PERFIL}" == "pro" ]]; then
    read -rp "IP del servidor DB/logs: " IP_DB
    if [[ -z "${IP_DB:-}" ]]; then
        error "La IP del servidor DB es obligatoria para el perfil ${DASC_PERFIL}."; exit 1
    fi
else
    IP_DB="127.0.0.1"
fi

if [[ "${DASC_PERFIL}" == "standard" ]]; then
    IP_BACKUP="${IP_API}"  # en standard, backups en el mismo host que API
elif [[ "${DASC_PERFIL}" == "pro" ]]; then
    read -rp "IP del servidor de backups: " IP_BACKUP
    if [[ -z "${IP_BACKUP:-}" ]]; then
        error "La IP del servidor de backups es obligatoria para el perfil pro."; exit 1
    fi
else
    IP_BACKUP="127.0.0.1"
fi

# ── Paso 4: Credenciales ─────────────────────────────────────────────────────
section "PASO 4 — Credenciales del panel"

read -rp "Contraseña admin del panel (dejar vacío para generar una aleatoria): " ADMIN_PASS
if [[ -z "${ADMIN_PASS:-}" ]]; then
    ADMIN_PASS="$(python3 -c "import secrets; print(secrets.token_urlsafe(16))")"
    warn "Contraseña generada automáticamente: ${BOLD}${ADMIN_PASS}${RESET}"
    warn "ANÓTALA ahora — no se volverá a mostrar."
fi

SECRET_KEY="$(python3 -c "import secrets; print(secrets.token_urlsafe(48))")"
info "SECRET_KEY generada automáticamente."

# Hash bcrypt de la contraseña admin
info "Generando hash bcrypt de la contraseña admin..."
ADMIN_HASH="$(python3 -c "
from passlib.context import CryptContext
ctx = CryptContext(schemes=['bcrypt'])
print(ctx.hash('${ADMIN_PASS}'))
" 2>/dev/null || echo "")"

if [[ -z "${ADMIN_HASH:-}" ]]; then
    warn "No se pudo generar hash bcrypt (passlib no disponible). Usando contraseña en texto plano."
    ADMIN_HASH="${ADMIN_PASS}"
fi

# ── Paso 5: Configuración SMTP (opcional) ────────────────────────────────────
section "PASO 5 — Notificaciones por email (opcional)"

read -rp "Email de notificaciones del cliente (vacío = sin email): " NOTIF_EMAIL_TO
NOTIF_SMTP_HOST=""
NOTIF_SMTP_USER=""
NOTIF_SMTP_PASS=""

if [[ -n "${NOTIF_EMAIL_TO:-}" ]]; then
    read -rp "SMTP host [smtp.gmail.com]: " NOTIF_SMTP_HOST
    NOTIF_SMTP_HOST="${NOTIF_SMTP_HOST:-smtp.gmail.com}"
    read -rp "SMTP usuario (email desde el que se envía): " NOTIF_SMTP_USER
    read -rsp "SMTP contraseña: " NOTIF_SMTP_PASS
    echo ""
fi

# ── Paso 6: Integración con Central Support ──────────────────────────────────
section "PASO 6 — Integración con DASC Central Support"

read -rp "URL de Central Support (vacío = sin integración): " CENTRAL_URL
CENTRAL_TOKEN=""
if [[ -n "${CENTRAL_URL:-}" ]]; then
    read -rsp "Token del cliente en Central Support: " CENTRAL_TOKEN
    echo ""
fi

# ── Paso 7: Generar config.env ───────────────────────────────────────────────
section "PASO 7 — Generando config.env"

CONFIG_TARGET="/tmp/config_${DASC_CLIENTE_ID}_$(date +%Y%m%d_%H%M%S).env"

cat > "${CONFIG_TARGET}" << ENVEOF
# DASC Server Manager — config.env generado por onboarding_nuevo_cliente.sh
# Cliente: ${DASC_CLIENTE_NOMBRE}
# Perfil:  ${DASC_PERFIL}
# Fecha:   $(date +%Y-%m-%d)
# ADVERTENCIA: Este fichero contiene secretos. No commitear al repositorio.

SECRET_KEY=${SECRET_KEY}
ADMIN_USER=admin
ADMIN_PASSWORD=${ADMIN_HASH}

DASC_PROFILE=${DASC_PERFIL}

# ── IPs de los servidores
DASC_API_HOST=${IP_API}
DASC_DB_HOST=${IP_DB}
DASC_BACKUP_HOST=${IP_BACKUP}

# ── SSH
DASC_SSH_ALLOWED_HOSTS=${IP_DB},${IP_BACKUP}

# ── Notificaciones
NOTIF_EMAIL_TO=${NOTIF_EMAIL_TO}
NOTIF_SMTP_HOST=${NOTIF_SMTP_HOST}
NOTIF_SMTP_PORT=587
NOTIF_SMTP_USER=${NOTIF_SMTP_USER}
NOTIF_SMTP_PASS=${NOTIF_SMTP_PASS}
NOTIF_EMAIL_FROM=${NOTIF_SMTP_USER}
NOTIF_DISK_THRESHOLD=80
NOTIF_BACKUP_HOURS=26
NOTIF_COOLDOWN_MINUTES=60

# ── Central Support
CENTRAL_SUPPORT_ENABLED=$([ -n "${CENTRAL_URL:-}" ] && echo "true" || echo "false")
CENTRAL_SUPPORT_URL=${CENTRAL_URL:-http://127.0.0.1:8010/api/v1/support/tickets}
CENTRAL_SUPPORT_CLIENT_ID=${DASC_CLIENTE_ID}
CENTRAL_SUPPORT_CLIENT_NAME=${DASC_CLIENTE_NOMBRE}
CENTRAL_SUPPORT_TOKEN=${CENTRAL_TOKEN}
CENTRAL_HEARTBEAT_INTERVAL=300
ENVEOF

ok "config.env generado en: ${CONFIG_TARGET}"

# ── Paso 8: Instalar DASC ────────────────────────────────────────────────────
section "PASO 8 — Instalación de DASC"

echo ""
echo "¿Ejecutar el instalador ahora con la config generada? [s/N]"
read -r EJECUTAR_INSTALL
if [[ "${EJECUTAR_INSTALL,,}" == "s" ]]; then
    info "Copiando config.env y lanzando el instalador..."
    export DASC_PROFILE="${DASC_PERFIL}"
    export DASC_API_HOST="${IP_API}"
    export DASC_DB_HOST="${IP_DB}"
    export DASC_BACKUP_HOST="${IP_BACKUP}"
    # El instalador leerá la config del env o pedirá interactivamente
    cp "${CONFIG_TARGET}" "${PACKAGE_DIR}/config.env.onboarding"
    bash "${SCRIPT_DIR}/install_dasc_api.sh"
    ok "Instalador completado."
else
    info "Instalación omitida. Ejecuta manualmente:"
    echo "  sudo bash deploy/api/install_dasc_api.sh"
    echo ""
    info "Y copia la config generada:"
    echo "  sudo cp ${CONFIG_TARGET} /opt/dasc/api/config.env"
    echo "  sudo systemctl restart dasc-api"
fi

# ── Resumen ───────────────────────────────────────────────────────────────────
section "RESUMEN DEL ONBOARDING"

echo "  Cliente:          ${DASC_CLIENTE_NOMBRE}"
echo "  ID:               ${DASC_CLIENTE_ID}"
echo "  Perfil:           ${DASC_PERFIL}"
echo "  IP API:           ${IP_API}"
echo "  IP DB:            ${IP_DB}"
echo "  IP Backup:        ${IP_BACKUP}"
echo "  Contraseña admin: ${ADMIN_PASS}"
echo "  config.env:       ${CONFIG_TARGET}"
echo ""
warn "GUARDA LA CONTRASEÑA ADMIN. Es la única copia en texto plano."
echo ""
info "Próximos pasos (ver docs/comercial/onboarding_cliente.md):"
echo "  1. Verificar: systemctl status dasc-api"
echo "  2. Acceder al panel y cambiar la contraseña"
echo "  3. Configurar alertas y ejecutar backup de prueba"
echo "  4. Verificar heartbeat en Central Support (Salud global)"
echo "  5. Programar la formación con el cliente"
echo ""
ok "Onboarding técnico completado."
