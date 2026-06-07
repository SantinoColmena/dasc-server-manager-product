#!/usr/bin/env bash
# R-054C — fail2ban para el host API/panel.
# Configura dos jaulas:
#   1. sshd  — protección SSH estándar (usar fail2ban con backend auto).
#   2. dasc-auth — protección del panel web: bloquea IPs que acumulen N intentos
#      de login fallidos observando los logs de Nginx (GET /login?error=).
#
# La jaula DASC lee el log de Nginx configurado por install_reverse_proxy.sh
# (/var/log/nginx/access.log). Si usas install_nginx_dasc_api.sh, ajusta
# NGINX_ACCESS_LOG a /var/log/nginx/dasc-api-local.access.log.
#
# Uso:
#   sudo bash harden_fail2ban_api.sh
#   sudo NGINX_ACCESS_LOG=/var/log/nginx/dasc-api-local.access.log bash harden_fail2ban_api.sh
#
# Variables de entorno opcionales:
#   NGINX_ACCESS_LOG   — ruta al access.log de Nginx (default: /var/log/nginx/access.log)
#   DASC_BAN_TIME      — tiempo de baneo en segundos (default: 3600 = 1 hora)
#   DASC_FIND_TIME     — ventana de observación en segundos (default: 600 = 10 min)
#   DASC_MAX_RETRY     — nº de fallos antes de banear (default: 5)
#   SSH_BAN_TIME       — tiempo de baneo SSH en segundos (default: 3600)
#   SSH_MAX_RETRY      — nº de fallos SSH antes de banear (default: 5)
set -euo pipefail

NGINX_ACCESS_LOG="${NGINX_ACCESS_LOG:-/var/log/nginx/access.log}"
DASC_BAN_TIME="${DASC_BAN_TIME:-3600}"
DASC_FIND_TIME="${DASC_FIND_TIME:-600}"
DASC_MAX_RETRY="${DASC_MAX_RETRY:-5}"
SSH_BAN_TIME="${SSH_BAN_TIME:-3600}"
SSH_MAX_RETRY="${SSH_MAX_RETRY:-5}"

FILTER_DIR="/etc/fail2ban/filter.d"
JAIL_DIR="/etc/fail2ban/jail.d"

if [[ "$EUID" -ne 0 ]]; then
  echo "ERROR: ejecuta este script con sudo."
  exit 1
fi

echo "==> R-054C — Instalando y configurando fail2ban en host API/panel"

# ── Instalar fail2ban ────────────────────────────────────────────────────────
if ! command -v fail2ban-client >/dev/null 2>&1; then
  echo "==> Instalando fail2ban"
  apt-get update -q
  DEBIAN_FRONTEND=noninteractive apt-get install -y fail2ban
fi

# ── Filtro personalizado: intentos de login fallidos en DASC ─────────────────
# DASC redirige a /login?error=1 tras credenciales incorrectas y a
# /login?error=2 cuando la IP ya está bloqueada por el rate-limiter interno.
# Nginx registra la petición GET del navegador al seguir esa redirección:
#   192.0.2.10 - - [07/Jun/2026:...] "GET /login?error=1 HTTP/1.1" 200 ...
# El filtro captura esas líneas para detectar la IP origen.
echo "==> Creando filtro fail2ban: ${FILTER_DIR}/dasc-auth.conf"
cat > "${FILTER_DIR}/dasc-auth.conf" <<'FILTEREOF'
[Definition]
# Detecta intentos de login fallidos en el panel DASC observando las
# peticiones GET a /login?error= que Nginx registra tras cada redirección
# post-login fallido (303 → GET /login?error=1 o GET /login?error=2).
failregex = ^<HOST> -.*"GET /login\?error=[12] HTTP/\S+" \d+
ignoreregex =
FILTEREOF

# ── Configuración de jaulas (jail.d tiene prioridad sobre jail.conf) ─────────
echo "==> Creando configuración de jaulas: ${JAIL_DIR}/dasc.conf"
cat > "${JAIL_DIR}/dasc.conf" <<JAILEOF
# R-054C — Jaulas fail2ban para DASC Server Manager.
# Este fichero sobreescribe/amplía la configuración por defecto de fail2ban.

[sshd]
enabled  = true
port     = ssh
maxretry = ${SSH_MAX_RETRY}
bantime  = ${SSH_BAN_TIME}
# backend auto detecta systemd journal o el fichero /var/log/auth.log.

[dasc-auth]
enabled   = true
filter    = dasc-auth
port      = http,https
logpath   = ${NGINX_ACCESS_LOG}
maxretry  = ${DASC_MAX_RETRY}
findtime  = ${DASC_FIND_TIME}
bantime   = ${DASC_BAN_TIME}
JAILEOF

# ── Activar y arrancar fail2ban ──────────────────────────────────────────────
echo "==> Habilitando y reiniciando fail2ban"
systemctl enable fail2ban
systemctl restart fail2ban

# Espera breve para que fail2ban cargue las jaulas
sleep 2

echo
echo "==> Estado de fail2ban"
fail2ban-client status || true

echo
echo "==> Estado de la jaula sshd"
fail2ban-client status sshd || true

echo
echo "==> Estado de la jaula dasc-auth"
if [[ -f "${NGINX_ACCESS_LOG}" ]]; then
  fail2ban-client status dasc-auth || true
else
  echo "AVISO: ${NGINX_ACCESS_LOG} no existe todavía."
  echo "       La jaula dasc-auth se activará cuando Nginx empiece a escribir el log."
  echo "       Comprueba con: sudo fail2ban-client status dasc-auth"
fi

echo
echo "OK: fail2ban configurado en host API/panel."
echo "    SSH   — maxretry=${SSH_MAX_RETRY}, bantime=${SSH_BAN_TIME}s"
echo "    DASC  — maxretry=${DASC_MAX_RETRY}, findtime=${DASC_FIND_TIME}s, bantime=${DASC_BAN_TIME}s"
echo "    Log   — ${NGINX_ACCESS_LOG}"
