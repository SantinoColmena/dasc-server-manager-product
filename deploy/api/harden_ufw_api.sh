#!/usr/bin/env bash
# R-054A — UFW para el host de la API/panel.
# Abre únicamente los puertos necesarios: SSH, HTTP (→ redirect HTTPS) y HTTPS.
# El puerto 8000 (Uvicorn) NO necesita regla: ya escucha solo en 127.0.0.1.
#
# Uso:
#   sudo bash harden_ufw_api.sh
#   sudo SSH_PORT=2222 bash harden_ufw_api.sh    # SSH en puerto no estándar
set -euo pipefail

SSH_PORT="${SSH_PORT:-22}"

if [[ "$EUID" -ne 0 ]]; then
  echo "ERROR: ejecuta este script con sudo."
  exit 1
fi

echo "==> R-054A — Configurando UFW en host API/panel"

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

# ── Reglas de entrada ───────────────────────────────────────────────────────
echo "==> Permitiendo SSH en puerto ${SSH_PORT}"
ufw allow "${SSH_PORT}/tcp" comment "SSH"

echo "==> Permitiendo HTTP 80 (redirige a HTTPS vía nginx)"
ufw allow 80/tcp comment "HTTP nginx redirect"

echo "==> Permitiendo HTTPS 443"
ufw allow 443/tcp comment "HTTPS nginx proxy"

# ── Activar ─────────────────────────────────────────────────────────────────
echo "==> Activando UFW"
ufw --force enable

echo
ufw status verbose

echo
echo "OK: UFW activo en host API/panel. Puertos abiertos: ${SSH_PORT}/tcp, 80/tcp, 443/tcp."
