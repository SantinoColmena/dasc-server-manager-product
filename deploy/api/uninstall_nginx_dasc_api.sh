#!/usr/bin/env bash
set -euo pipefail

NGINX_SITE_NAME="${NGINX_SITE_NAME:-dasc-api-local}"
NGINX_SITE_FILE="/etc/nginx/sites-available/${NGINX_SITE_NAME}"
NGINX_SITE_LINK="/etc/nginx/sites-enabled/${NGINX_SITE_NAME}"

if [ "$(id -u)" -ne 0 ]; then
  echo "ERROR: ejecuta este desinstalador con sudo."
  exit 1
fi

echo "==> Desinstalando configuración Nginx de DASC API / panel local"

rm -f "${NGINX_SITE_LINK}"
rm -f "${NGINX_SITE_FILE}"

if command -v nginx >/dev/null 2>&1; then
  nginx -t
  systemctl reload nginx || systemctl restart nginx || true
fi

echo "OK: configuración Nginx de DASC API / panel local eliminada."
