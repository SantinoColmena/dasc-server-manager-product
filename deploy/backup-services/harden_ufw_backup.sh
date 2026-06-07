#!/usr/bin/env bash
# R-054A — UFW para el host de backup/servicios.
# Este host no expone ningún servicio público. Solo se permite SSH.
# Las conexiones de mysqldump desde aquí hacia el host DB son SALIENTES
# (outgoing allow) y no requieren reglas de entrada.
#
# Uso:
#   sudo bash harden_ufw_backup.sh
#   sudo SSH_PORT=2222 bash harden_ufw_backup.sh
set -euo pipefail

SSH_PORT="${SSH_PORT:-22}"

if [[ "$EUID" -ne 0 ]]; then
  echo "ERROR: ejecuta este script con sudo."
  exit 1
fi

echo "==> R-054A — Configurando UFW en host de backup/servicios"

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

# ── Solo SSH ─────────────────────────────────────────────────────────────────
echo "==> Permitiendo SSH en puerto ${SSH_PORT}"
ufw allow "${SSH_PORT}/tcp" comment "SSH"

# ── Activar ─────────────────────────────────────────────────────────────────
echo "==> Activando UFW"
ufw --force enable

echo
ufw status verbose

echo
echo "OK: UFW activo en host de backup/servicios."
echo "    Solo SSH (${SSH_PORT}/tcp) permitido desde el exterior."
echo "    Conexiones salientes (mysqldump, SSH inverso) se permiten por defecto."
