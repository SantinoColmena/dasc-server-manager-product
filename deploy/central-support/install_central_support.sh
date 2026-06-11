#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="vigex-central"
INSTALL_DIR="${INSTALL_DIR:-/opt/vigex/central-support}"
INSTALL_PARENT="${INSTALL_PARENT:-$(dirname "${INSTALL_DIR}")}"
APP_USER="${APP_USER:-vigex}"
APP_GROUP="${APP_GROUP:-vigex}"
APP_HOST="${APP_HOST:-0.0.0.0}"
APP_PORT="${APP_PORT:-8010}"
SOURCE_DIR="${SOURCE_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/package" && pwd)}"
ENV_FILE="${INSTALL_DIR}/config.env"

echo "==> Instalando Vigex Central"

if [ "$(id -u)" -ne 0 ]; then
  echo "ERROR: ejecuta este instalador con sudo."
  exit 1
fi

echo "==> Instalando dependencias del sistema"
apt-get update
apt-get install -y python3 python3-venv python3-pip rsync curl

echo "==> Preparando usuario ${APP_USER}"
if ! id "${APP_USER}" >/dev/null 2>&1; then
  useradd --system --home /opt/vigex --shell /usr/sbin/nologin "${APP_USER}"
fi

echo "==> Creando directorios"
mkdir -p "${INSTALL_PARENT}"
chmod 755 "${INSTALL_PARENT}"
mkdir -p "${INSTALL_DIR}"
mkdir -p "${INSTALL_DIR}/data"

echo "==> Copiando aplicación desde ${SOURCE_DIR}"
rsync -a --delete \
  --exclude "venv" \
  --exclude "__pycache__" \
  --exclude "*.pyc" \
  --exclude "*.log" \
  --exclude "data/*.db" \
  "${SOURCE_DIR}/" "${INSTALL_DIR}/"

echo "==> Creando entorno virtual"
python3 -m venv "${INSTALL_DIR}/venv"
"${INSTALL_DIR}/venv/bin/python" -m pip install --upgrade pip
"${INSTALL_DIR}/venv/bin/pip" install -r "${INSTALL_DIR}/requirements.txt"

echo "==> Preparando config.env"

CONFIG_NEEDS_INIT="false"

if [ ! -f "${ENV_FILE}" ]; then
  CONFIG_NEEDS_INIT="true"
elif [ ! -s "${ENV_FILE}" ]; then
  CONFIG_NEEDS_INIT="true"
elif ! grep -q '^VIGEX_CENTRAL_SECRET_KEY=' "${ENV_FILE}"; then
  CONFIG_NEEDS_INIT="true"
fi

if [ "${CONFIG_NEEDS_INIT}" = "true" ]; then
  CENTRAL_SECRET="$(python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(48))
PY
)"

  CENTRAL_ADMIN_PASSWORD_VALUE="${VIGEX_CENTRAL_ADMIN_PASSWORD:-$(python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(24))
PY
)}"

  CENTRAL_TECH_PASSWORD_VALUE="${VIGEX_CENTRAL_TECH_PASSWORD:-$(python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(24))
PY
)}"

  CENTRAL_DEMO_TOKEN_VALUE="${VIGEX_CENTRAL_DEMO_TOKEN:-$(python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(32))
PY
)}"

  # M-4: almacenar las contraseñas como hash PBKDF2-SHA256, nunca en texto plano.
  hash_central_password() {
    python3 - "$1" <<'PY'
import sys, os, hashlib
plain = sys.argv[1].encode("utf-8")
salt = os.urandom(16)
dk = hashlib.pbkdf2_hmac("sha256", plain, salt, 200000)
print("pbkdf2_sha256$200000$" + salt.hex() + "$" + dk.hex())
PY
  }

  CENTRAL_ADMIN_PASSWORD_HASH_VALUE="$(hash_central_password "${CENTRAL_ADMIN_PASSWORD_VALUE}")"
  CENTRAL_TECH_PASSWORD_HASH_VALUE="$(hash_central_password "${CENTRAL_TECH_PASSWORD_VALUE}")"

  cat > "${ENV_FILE}" <<EOF
# Vigex Central
VIGEX_CENTRAL_AUTH_ENABLED=true
VIGEX_CENTRAL_LAB_MODE=false
VIGEX_CENTRAL_SECRET_KEY=${CENTRAL_SECRET}

# Usuarios centrales. Contraseñas almacenadas como hash PBKDF2 (M-4).
VIGEX_CENTRAL_ADMIN_USER=${VIGEX_CENTRAL_ADMIN_USER:-admin}
VIGEX_CENTRAL_ADMIN_PASSWORD_HASH=${CENTRAL_ADMIN_PASSWORD_HASH_VALUE}
VIGEX_CENTRAL_TECH_USER=${VIGEX_CENTRAL_TECH_USER:-tecnico}
VIGEX_CENTRAL_TECH_PASSWORD_HASH=${CENTRAL_TECH_PASSWORD_HASH_VALUE}

# Cliente demo para integración local-central
VIGEX_CENTRAL_DEMO_CLIENT_ID=cliente-demo-a
VIGEX_CENTRAL_DEMO_CLIENT_NAME=Cliente Demo A
VIGEX_CENTRAL_DEMO_TOKEN=${CENTRAL_DEMO_TOKEN_VALUE}

# ── Proxy LLM centralizado (R-097) ────────────────────────────────
# Proveedor LLM para el Asistente IA de todos los clientes.
# Los paneles cliente usan VIGEX_RAG_LLM_PROVIDER=central y no necesitan API key.
# Opciones: anthropic (recomendado) | gemini | openai | groq | ollama
VIGEX_CENTRAL_LLM_PROVIDER=anthropic
# Rellena SOLO la clave del proveedor elegido:
ANTHROPIC_API_KEY=
VIGEX_CENTRAL_ANTHROPIC_MODEL=claude-haiku-4-5-20251001
GOOGLE_API_KEY=
VIGEX_CENTRAL_GEMINI_MODEL=gemini-2.0-flash
OPENAI_API_KEY=
VIGEX_CENTRAL_OPENAI_MODEL=gpt-4o-mini
GROQ_API_KEY=
VIGEX_CENTRAL_GROQ_MODEL=llama-3.3-70b-versatile
VIGEX_CENTRAL_OLLAMA_URL=http://localhost:11434
VIGEX_CENTRAL_OLLAMA_MODEL=mistral
# Rate limiting por cliente: máximo de peticiones en la ventana deslizante
VIGEX_CENTRAL_LLM_RATE_REQS=30
VIGEX_CENTRAL_LLM_RATE_WIN=60
VIGEX_CENTRAL_LLM_MAX_TOKENS=700

# ── Bot Telegram centralizado @VigexBot (R-098) ───────────────────
# Token del bot único de Vigex. Los clientes solo necesitan su chat_id.
# Obtén el token creando el bot con @BotFather en Telegram.
VIGEX_CENTRAL_TELEGRAM_BOT_TOKEN=
VIGEX_CENTRAL_TELEGRAM_BOT_USERNAME=VigexBot
# Rate limiting: máximo de mensajes Telegram por cliente en la ventana
VIGEX_CENTRAL_TELEGRAM_RATE_REQS=20
VIGEX_CENTRAL_TELEGRAM_RATE_WIN=60
EOF

  chmod 600 "${ENV_FILE}"

  echo "==> config.env inicializado. Contraseñas almacenadas como hash PBKDF2."
  echo "==> Estas credenciales se muestran SOLO UNA VEZ. Guárdalas en un lugar seguro:"
  echo "    Admin: ${VIGEX_CENTRAL_ADMIN_USER:-admin} / ${CENTRAL_ADMIN_PASSWORD_VALUE}"
  echo "    Técnico: ${VIGEX_CENTRAL_TECH_USER:-tecnico} / ${CENTRAL_TECH_PASSWORD_VALUE}"
else
  echo "==> config.env ya existe, se conserva"

  if ! grep -q '^VIGEX_CENTRAL_LAB_MODE=' "${ENV_FILE}"; then
    echo "VIGEX_CENTRAL_LAB_MODE=false" >> "${ENV_FILE}"
  fi
fi
echo "==> Ajustando permisos"
chown -R "${APP_USER}:${APP_GROUP}" "${INSTALL_DIR}"
chmod 750 "${INSTALL_DIR}"
chmod 750 "${INSTALL_DIR}/data"

# config.env contiene secretos. systemd lo lee como root antes de arrancar el servicio.
# El proceso de la app no necesita editarlo.
chown root:root "${ENV_FILE}"
chmod 600 "${ENV_FILE}"

echo "==> Creando servicio systemd"
cat > "/etc/systemd/system/${SERVICE_NAME}.service" <<EOF
[Unit]
Description=Vigex Central (FastAPI/Uvicorn)
After=network.target

[Service]
Type=simple
User=${APP_USER}
Group=${APP_GROUP}
WorkingDirectory=${INSTALL_DIR}
EnvironmentFile=${ENV_FILE}
ExecStart=${INSTALL_DIR}/venv/bin/python -m uvicorn main:app --host ${APP_HOST} --port ${APP_PORT}
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

echo "==> Activando servicio"
systemctl daemon-reload
systemctl enable "${SERVICE_NAME}"
systemctl restart "${SERVICE_NAME}"

sleep 3

echo "==> Estado del servicio"
systemctl --no-pager --full status "${SERVICE_NAME}" || true

echo
echo "==> Probando health local"
curl -s "http://127.0.0.1:${APP_PORT}/health" || true
echo

echo
echo "OK: Vigex Central instalado."
echo "URL local: http://127.0.0.1:${APP_PORT}"
echo "Servicio: ${SERVICE_NAME}"
echo "Directorio: ${INSTALL_DIR}"
