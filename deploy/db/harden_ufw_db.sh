#!/usr/bin/env bash
# R-054A — UFW para el host de base de datos (MariaDB).
# Abre SSH y, opcionalmente, el puerto 3306 solo desde las IPs autorizadas
# (panel y/o host de backups). El resto de tráfico entrante se deniega.
#
# Uso:
#   sudo MARIADB_ALLOWED_HOSTS="192.168.1.10,192.168.1.20" bash harden_ufw_db.sh
#   sudo SSH_PORT=2222 MARIADB_ALLOWED_HOSTS="10.0.0.5" bash harden_ufw_db.sh
#
# Si MARIADB_ALLOWED_HOSTS está vacío, el puerto 3306 solo queda accesible
# desde localhost (MariaDB ya escucha en 127.0.0.1 si bind-address lo indica;
# la regla UFW actúa como segunda capa).
set -euo pipefail

SSH_PORT="${SSH_PORT:-22}"
MARIADB_ALLOWED_HOSTS="${MARIADB_ALLOWED_HOSTS:-}"   # IPs separadas por coma

if [[ "$EUID" -ne 0 ]]; then
  echo "ERROR: ejecuta este script con sudo."
  exit 1
fi

echo "==> R-054A — Configurando UFW en host DB"

# ── Instalación de UFW si no está presente ──────────────────────────────────
if ! command -v ufw >/dev/null 2>&1; then
  echo "==> Instalando UFW"
  apt-get update -q
  DEBIAN_FRONTEND=noninteractive apt-get install -y ufw
fi

# ── Reset y política restrictiva ────────────────────────────────────────────
echo "==> Aplicando política por defecto (deny incoming / allow outgoing)"
ufw --force reset
ufw default deny incoming
ufw default allow outgoing

# ── SSH ─────────────────────────────────────────────────────────────────────
echo "==> Permitiendo SSH en puerto ${SSH_PORT}"
ufw allow "${SSH_PORT}/tcp" comment "SSH"

# ── MariaDB 3306 — solo desde IPs autorizadas ───────────────────────────────
if [[ -n "$MARIADB_ALLOWED_HOSTS" ]]; then
  IFS=',' read -ra HOSTS <<< "$MARIADB_ALLOWED_HOSTS"
  for h in "${HOSTS[@]}"; do
    h="${h// /}"
    [[ -z "$h" ]] && continue
    echo "==> Permitiendo MariaDB 3306 desde ${h}"
    ufw allow from "$h" to any port 3306 proto tcp comment "MariaDB desde ${h}"
  done
else
  echo "AVISO: MARIADB_ALLOWED_HOSTS no definido."
  echo "       El puerto 3306 queda bloqueado desde el exterior."
  echo "       Pasa las IPs del panel y del host de backup si son remotas:"
  echo "       MARIADB_ALLOWED_HOSTS=\"<IP_panel>,<IP_backup>\" sudo bash $0"
fi

# ── Activar ─────────────────────────────────────────────────────────────────
echo "==> Activando UFW"
ufw --force enable

echo
ufw status verbose

echo
echo "OK: UFW activo en host DB."
[[ -n "$MARIADB_ALLOWED_HOSTS" ]] && \
  echo "    MariaDB 3306 accesible desde: ${MARIADB_ALLOWED_HOSTS}" || \
  echo "    MariaDB 3306 bloqueado desde el exterior (solo localhost)."
