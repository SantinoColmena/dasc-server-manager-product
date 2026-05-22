#!/usr/bin/env bash
set -euo pipefail

APP_NAME="DASC Server Manager"
SERVER_NAME="${SERVER_NAME:-_}"
UPSTREAM_HOST="${UPSTREAM_HOST:-127.0.0.1}"
UPSTREAM_PORT="${UPSTREAM_PORT:-8000}"

NGINX_SITE_AVAILABLE="/etc/nginx/sites-available/dasc-api"
NGINX_SITE_ENABLED="/etc/nginx/sites-enabled/dasc-api"

SSL_DIR="/etc/ssl/dasc"
SSL_CERT="${SSL_DIR}/dasc-selfsigned.crt"
SSL_KEY="${SSL_DIR}/dasc-selfsigned.key"

if [[ "$EUID" -ne 0 ]]; then
  echo "ERROR: ejecuta este script con sudo."
  exit 1
fi

echo "==> Instalando reverse proxy para ${APP_NAME}"
echo "==> SERVER_NAME=${SERVER_NAME}"
echo "==> Backend interno: http://${UPSTREAM_HOST}:${UPSTREAM_PORT}"

echo "==> Instalando paquetes necesarios"
apt update
apt install -y nginx openssl curl

echo "==> Creando certificado autofirmado para laboratorio"
mkdir -p "$SSL_DIR"

if [[ ! -f "$SSL_CERT" || ! -f "$SSL_KEY" ]]; then
  openssl req -x509 -nodes -days 365 \
    -newkey rsa:4096 \
    -keyout "$SSL_KEY" \
    -out "$SSL_CERT" \
    -subj "/C=ES/ST=Lab/L=Lab/O=DASC/OU=Proyecto/CN=${SERVER_NAME}"

  chmod 600 "$SSL_KEY"
  chmod 644 "$SSL_CERT"
  echo "==> Certificado autofirmado creado"
else
  echo "==> Certificado existente detectado. Se conserva."
fi

echo "==> Creando configuración Nginx"
cat > "$NGINX_SITE_AVAILABLE" <<EOF
server {
    listen 80;
    server_name ${SERVER_NAME};

    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ${SERVER_NAME};

    ssl_certificate ${SSL_CERT};
    ssl_certificate_key ${SSL_KEY};

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;

    client_max_body_size 50M;

    proxy_read_timeout 300;
    proxy_connect_timeout 300;
    proxy_send_timeout 300;

    location / {
        proxy_pass http://${UPSTREAM_HOST}:${UPSTREAM_PORT};
        proxy_http_version 1.1;

        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;

        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

echo "==> Activando sitio"
ln -sfn "$NGINX_SITE_AVAILABLE" "$NGINX_SITE_ENABLED"

if [[ -f /etc/nginx/sites-enabled/default ]]; then
  rm -f /etc/nginx/sites-enabled/default
fi

echo "==> Validando configuración Nginx"
nginx -t

echo "==> Reiniciando Nginx"
systemctl enable nginx
systemctl restart nginx

echo "==> Comprobando acceso local"
curl -k -I https://127.0.0.1 || true

echo
echo "============================================"
echo "Reverse proxy instalado"
echo "HTTP  -> redirige a HTTPS"
echo "HTTPS -> proxy a http://${UPSTREAM_HOST}:${UPSTREAM_PORT}"
echo "Certificado: ${SSL_CERT}"
echo "Clave:       ${SSL_KEY}"
echo "Sitio:       ${NGINX_SITE_AVAILABLE}"
echo "============================================"
