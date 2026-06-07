#!/usr/bin/env bash
# R-054B — Reverse proxy HTTPS para DASC Server Manager.
# Soporta dos modos de certificado:
#
#   CERT_TYPE=selfsigned (por defecto) — certificado autofirmado RSA-4096,
#     válido 365 días. Adecuado para laboratorio y despliegues internos donde
#     no hay dominio público. El navegador mostrará aviso de certificado.
#
#   CERT_TYPE=certbot — obtiene certificado Let's Encrypt vía certbot.
#     Requiere DOMAIN con nombre DNS real, puerto 80 accesible desde Internet.
#     Renueva automáticamente con el timer systemd de certbot.
#
# Uso:
#   # Autofirmado (lab):
#   sudo bash install_reverse_proxy.sh
#
#   # Let's Encrypt (producción con dominio real):
#   sudo CERT_TYPE=certbot DOMAIN=dasc.ejemplo.com \
#        CERTBOT_EMAIL=admin@ejemplo.com bash install_reverse_proxy.sh
#
# Variables de entorno:
#   CERT_TYPE        selfsigned | certbot  (default: selfsigned)
#   DOMAIN           Nombre de dominio completo (necesario para certbot)
#   CERTBOT_EMAIL    Email para notificaciones de caducidad (necesario para certbot)
#   SERVER_NAME      Nombre nginx server_name (default: _)
#   UPSTREAM_HOST    Host del backend (default: 127.0.0.1)
#   UPSTREAM_PORT    Puerto del backend (default: 8000)
#   API_CONFIG_FILE  config.env del panel para activar HTTPS_ONLY (default: /opt/dasc/api/config.env)
set -euo pipefail

APP_NAME="DASC Server Manager"
CERT_TYPE="${CERT_TYPE:-selfsigned}"
DOMAIN="${DOMAIN:-}"
CERTBOT_EMAIL="${CERTBOT_EMAIL:-}"
SERVER_NAME="${SERVER_NAME:-_}"
UPSTREAM_HOST="${UPSTREAM_HOST:-127.0.0.1}"
UPSTREAM_PORT="${UPSTREAM_PORT:-8000}"
API_CONFIG_FILE="${API_CONFIG_FILE:-/opt/dasc/api/config.env}"

NGINX_SITE_AVAILABLE="/etc/nginx/sites-available/dasc-api"
NGINX_SITE_ENABLED="/etc/nginx/sites-enabled/dasc-api"

SSL_DIR="/etc/ssl/dasc"
SSL_CERT="${SSL_DIR}/dasc-selfsigned.crt"
SSL_KEY="${SSL_DIR}/dasc-selfsigned.key"

if [[ "$EUID" -ne 0 ]]; then
  echo "ERROR: ejecuta este script con sudo."
  exit 1
fi

if [[ "$CERT_TYPE" == "certbot" ]]; then
  if [[ -z "$DOMAIN" ]]; then
    echo "ERROR: CERT_TYPE=certbot requiere que definas DOMAIN=<nombre.dominio>."
    exit 1
  fi
  if [[ -z "$CERTBOT_EMAIL" ]]; then
    echo "ERROR: CERT_TYPE=certbot requiere que definas CERTBOT_EMAIL=<email>."
    exit 1
  fi
  SERVER_NAME="$DOMAIN"
fi

echo "==> Instalando reverse proxy para ${APP_NAME}"
echo "==> CERT_TYPE=${CERT_TYPE}"
echo "==> SERVER_NAME=${SERVER_NAME}"
echo "==> Backend interno: http://${UPSTREAM_HOST}:${UPSTREAM_PORT}"

echo "==> Instalando paquetes necesarios"
apt update
if [[ "$CERT_TYPE" == "certbot" ]]; then
  apt install -y nginx curl certbot python3-certbot-nginx
else
  apt install -y nginx openssl curl
fi

# ── Certificado autofirmado (modo selfsigned) ────────────────────────────────
if [[ "$CERT_TYPE" == "selfsigned" ]]; then
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
fi

# ── Configuración Nginx inicial (solo se crea en modo selfsigned) ────────────
# En modo certbot la config la genera certbot --nginx, pero dejamos un bloque
# HTTP básico para que certbot tenga algo con que trabajar.
if [[ "$CERT_TYPE" == "selfsigned" ]]; then
  echo "==> Creando configuración Nginx (modo selfsigned)"
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
else
  # Modo certbot: bloque HTTP mínimo para que certbot pueda hacer el challenge.
  echo "==> Creando configuración Nginx temporal (modo certbot)"
  cat > "$NGINX_SITE_AVAILABLE" <<EOF
server {
    listen 80;
    server_name ${DOMAIN};

    location / {
        proxy_pass http://${UPSTREAM_HOST}:${UPSTREAM_PORT};
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
fi

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

# ── Let's Encrypt con certbot ────────────────────────────────────────────────
if [[ "$CERT_TYPE" == "certbot" ]]; then
  echo "==> Obteniendo certificado Let's Encrypt para ${DOMAIN}"
  certbot --nginx \
    --non-interactive \
    --agree-tos \
    --email "${CERTBOT_EMAIL}" \
    --domains "${DOMAIN}" \
    --redirect

  echo "==> Verificando renovación automática certbot"
  certbot renew --dry-run

  echo "==> Reload Nginx tras certbot"
  systemctl reload nginx
fi

# ── Activar DASC_SESSION_HTTPS_ONLY en config.env del panel ──────────────────
echo "==> Activando DASC_SESSION_HTTPS_ONLY=true en el panel"
if [[ -f "${API_CONFIG_FILE}" ]]; then
  if grep -qE "^DASC_SESSION_HTTPS_ONLY=" "${API_CONFIG_FILE}"; then
    sed -i -E "s|^DASC_SESSION_HTTPS_ONLY=.*|DASC_SESSION_HTTPS_ONLY=true|" "${API_CONFIG_FILE}"
    echo "==> DASC_SESSION_HTTPS_ONLY actualizado a true en ${API_CONFIG_FILE}"
  else
    echo "DASC_SESSION_HTTPS_ONLY=true" >> "${API_CONFIG_FILE}"
    echo "==> DASC_SESSION_HTTPS_ONLY=true añadido a ${API_CONFIG_FILE}"
  fi
  # Reiniciar el servicio para que tome el cambio
  if systemctl is-active --quiet dasc-api 2>/dev/null; then
    systemctl restart dasc-api
    echo "==> dasc-api reiniciado para aplicar HTTPS_ONLY"
  fi
else
  echo "AVISO: ${API_CONFIG_FILE} no encontrado."
  echo "       Añade manualmente: DASC_SESSION_HTTPS_ONLY=true"
  echo "       Y reinicia dasc-api: sudo systemctl restart dasc-api"
fi

# ── Comprobación local ────────────────────────────────────────────────────────
echo "==> Comprobando acceso local"
if [[ "$CERT_TYPE" == "selfsigned" ]]; then
  curl -k -I https://127.0.0.1 || true
else
  curl -I "https://${DOMAIN}" || true
fi

echo
echo "============================================"
echo "Reverse proxy instalado"
echo "CERT_TYPE : ${CERT_TYPE}"
echo "HTTP      : redirige a HTTPS"
echo "HTTPS     : proxy a http://${UPSTREAM_HOST}:${UPSTREAM_PORT}"
if [[ "$CERT_TYPE" == "selfsigned" ]]; then
  echo "Certificado: ${SSL_CERT}"
  echo "Clave      : ${SSL_KEY}"
else
  echo "Certificado: Let's Encrypt / ${DOMAIN}"
fi
echo "Sitio nginx: ${NGINX_SITE_AVAILABLE}"
echo "HTTPS_ONLY : activado en el panel DASC"
echo "============================================"
