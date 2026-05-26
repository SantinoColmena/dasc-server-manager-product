#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="dasc-central-support"
NGINX_SITE_NAME="${NGINX_SITE_NAME:-dasc-central-support}"
NGINX_SITE_FILE="/etc/nginx/sites-available/${NGINX_SITE_NAME}"
NGINX_SITE_LINK="/etc/nginx/sites-enabled/${NGINX_SITE_NAME}"
APP_HOST="${APP_HOST:-127.0.0.1}"
APP_PORT="${APP_PORT:-8010}"
SERVER_NAME="${SERVER_NAME:-_}"

if [ "$(id -u)" -ne 0 ]; then
  echo "ERROR: ejecuta este instalador con sudo."
  exit 1
fi

echo "==> Instalando Nginx para DASC Central Support"

echo "==> Instalando paquete nginx"
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y nginx

echo "==> Comprobando servicio ${SERVICE_NAME}"
if ! systemctl is-active --quiet "${SERVICE_NAME}"; then
  echo "ERROR: ${SERVICE_NAME} no está activo."
  echo "Arráncalo primero con: sudo systemctl start ${SERVICE_NAME}"
  exit 1
fi

echo "==> Creando configuración Nginx"
cat > "${NGINX_SITE_FILE}" <<EOF
server {
    listen 80;
    server_name ${SERVER_NAME};

    access_log /var/log/nginx/dasc-central-support.access.log;
    error_log  /var/log/nginx/dasc-central-support.error.log;

    client_max_body_size 10M;

    location / {
        proxy_pass http://${APP_HOST}:${APP_PORT};

        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        proxy_connect_timeout 10s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
EOF

echo "==> Activando sitio"
ln -sfn "${NGINX_SITE_FILE}" "${NGINX_SITE_LINK}"

if [ -L /etc/nginx/sites-enabled/default ]; then
  echo "==> Desactivando sitio default de Nginx"
  rm -f /etc/nginx/sites-enabled/default
fi

echo "==> Validando configuración"
nginx -t

echo "==> Habilitando y reiniciando Nginx"
systemctl enable nginx
systemctl restart nginx

echo
echo "==> Estado Nginx"
systemctl --no-pager --full status nginx || true

echo
echo "==> Prueba local proxy"
curl -I "http://127.0.0.1/" || true

echo
echo "OK: Nginx configurado como reverse proxy para DASC Central Support."
echo "URL local: http://127.0.0.1/"
echo "URL red:   http://<IP_DEL_SERVIDOR>/"
echo "Backend:  http://${APP_HOST}:${APP_PORT}"
