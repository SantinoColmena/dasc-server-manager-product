#!/usr/bin/env bash
set -euo pipefail

NGINX_SITE_AVAILABLE="/etc/nginx/sites-available/vigex-api"
NGINX_SITE_ENABLED="/etc/nginx/sites-enabled/vigex-api"
SSL_DIR="/etc/ssl/vigex"

if [[ "$EUID" -ne 0 ]]; then
  echo "ERROR: ejecuta este script con sudo."
  exit 1
fi

echo "Vas a desinstalar el reverse proxy de Vigex."
echo "Se eliminarán:"
echo "  - ${NGINX_SITE_AVAILABLE}"
echo "  - ${NGINX_SITE_ENABLED}"
echo "  - ${SSL_DIR}"
echo
read -r -p "Escribe SI para continuar: " CONFIRM

if [[ "$CONFIRM" != "SI" ]]; then
  echo "Cancelado."
  exit 0
fi

echo "==> Eliminando sitio Nginx"
rm -f "$NGINX_SITE_ENABLED"
rm -f "$NGINX_SITE_AVAILABLE"

echo "==> Eliminando certificados autofirmados"
rm -rf "$SSL_DIR"

echo "==> Validando Nginx"
nginx -t || true

echo "==> Reiniciando Nginx"
systemctl restart nginx || true

echo
echo "============================================"
echo "Reverse proxy Vigex desinstalado"
echo "============================================"
