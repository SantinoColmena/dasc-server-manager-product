#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="${SERVICE_NAME:-dasc-api}"
NGINX_SITE_NAME="${NGINX_SITE_NAME:-dasc-api-local}"
NGINX_SITE_FILE="/etc/nginx/sites-available/${NGINX_SITE_NAME}"
NGINX_SITE_LINK="/etc/nginx/sites-enabled/${NGINX_SITE_NAME}"

APP_HOST="${APP_HOST:-127.0.0.1}"
APP_PORT="${APP_PORT:-8000}"

# En producción puede ser 80.
# En laboratorio se recomienda 8080 si el puerto 80 ya lo usa el panel central.
PUBLIC_PORT="${PUBLIC_PORT:-80}"
SERVER_NAME="${SERVER_NAME:-_}"

if [ "$(id -u)" -ne 0 ]; then
  echo "ERROR: ejecuta este instalador con sudo."
  exit 1
fi

echo "==> Instalando Nginx para DASC API / panel local cliente"

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
    listen ${PUBLIC_PORT};
    server_name ${SERVER_NAME};

    access_log /var/log/nginx/dasc-api-local.access.log;
    error_log  /var/log/nginx/dasc-api-local.error.log;

    client_max_body_size 20M;

    location / {
        proxy_pass http://${APP_HOST}:${APP_PORT};

        proxy_http_version 1.1;
        proxy_set_header Host \$http_host;
        proxy_set_header X-Forwarded-Host \$http_host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        proxy_connect_timeout 10s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
EOF

echo "==> Activando sitio ${NGINX_SITE_NAME}"
ln -sfn "${NGINX_SITE_FILE}" "${NGINX_SITE_LINK}"

echo "==> Validando configuración Nginx"
nginx -t

echo "==> Habilitando y recargando Nginx"
systemctl enable nginx

if systemctl is-active --quiet nginx; then
  systemctl reload nginx
else
  systemctl restart nginx
fi

echo
echo "==> Estado Nginx"
systemctl --no-pager --full status nginx || true

echo
echo "==> Prueba local proxy"
curl -I "http://127.0.0.1:${PUBLIC_PORT}/" || true

echo
echo "OK: Nginx configurado como reverse proxy para DASC API / panel local."
echo "URL local: http://127.0.0.1:${PUBLIC_PORT}/"
echo "Backend:   http://${APP_HOST}:${APP_PORT}"
echo
echo "Nota:"
echo "- En cliente real se puede usar PUBLIC_PORT=80."
echo "- En lab-pruebas se recomienda PUBLIC_PORT=8080 para no pisar el panel central."
