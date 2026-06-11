from dotenv import load_dotenv
load_dotenv("config.env")

from urllib.parse import quote
from urllib.request import Request as UrlRequest, urlopen
from urllib.error import URLError, HTTPError
import os
import json
import sqlite3
import subprocess
import shlex
import secrets
import posixpath
import smtplib
import threading
import time as _time_mod
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from datetime import datetime
from typing import Any
from contextlib import asynccontextmanager

from passlib.context import CryptContext
import pymysql
from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse, Response
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from markupsafe import Markup


@asynccontextmanager
async def lifespan(app: FastAPI):
    # L-5: inicialización al arranque (sustituye a @app.on_event("startup")).
    ensure_users_file()
    init_alerts_db()
    ensure_default_recipient()
    # R-060: arranque del hilo de notificaciones proactivas (solo si está habilitado)
    if NOTIF_ENABLED:
        t = threading.Thread(target=_proactivo_worker, daemon=True, name="vigex-notif")
        t.start()
    # R-062: hilo de informes periódicos (siempre activo; comprueba config al despertar)
    tr = threading.Thread(target=_reports_worker, daemon=True, name="vigex-reports")
    tr.start()
    yield


# =====================
# PROTECCIÓN CSRF (M-1)
# =====================
# Token sincronizador por sesión: se renderiza como campo oculto en cada
# formulario POST y se valida mediante una dependencia global. Las llamadas
# fetch envían el token en la cabecera X-CSRF-Token.
CSRF_EXEMPT_PATHS = {"/login", "/logout"}


def get_csrf_token(request: Request) -> str:
    token = request.session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        request.session["csrf_token"] = token
    return token


async def csrf_protect(request: Request) -> None:
    if request.method in ("GET", "HEAD", "OPTIONS", "TRACE"):
        return
    if request.url.path in CSRF_EXEMPT_PATHS:
        return

    session_token = request.session.get("csrf_token")
    sent = request.headers.get("x-csrf-token")

    if not sent:
        try:
            form = await request.form()
            sent = form.get("csrf_token")
        except Exception:
            sent = None

    if not session_token or not sent or not secrets.compare_digest(str(sent), str(session_token)):
        raise HTTPException(status_code=403, detail="CSRF token inválido o ausente.")


app = FastAPI(lifespan=lifespan, dependencies=[Depends(csrf_protect)])

# =====================
# CONFIG LOGIN / SESIÓN
# =====================
SECRET_KEY = os.getenv("SECRET_KEY", "cambia-esta-clave-por-una-segura")
ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

templates = Jinja2Templates(directory="templates")


def csrf_input(request: Request):
    """Campo oculto con el token CSRF para insertar dentro de cada formulario."""
    return Markup(f'<input type="hidden" name="csrf_token" value="{get_csrf_token(request)}">')


templates.env.globals["csrf_input"] = csrf_input
templates.env.globals["csrf_token_value"] = get_csrf_token
app.mount("/static", StaticFiles(directory="static"), name="static")

# =====================
# CONFIG MULTI-SERVIDOR
# =====================
USUARIO = os.getenv("SSH_USER", "vigex")
SERVIDOR_BACKUPS = os.getenv("BACKUPS_HOST", "127.0.0.1")
SERVIDOR_SERVICIOS = os.getenv("SERVICIOS_HOST", "127.0.0.1")
CACTI_URL = os.getenv("CACTI_URL", "http://127.0.0.1/cacti/")

LOGS_DB_HOST = os.getenv("LOGS_DB_HOST", "127.0.0.1")
LOGS_DB_NAME = os.getenv("LOGS_DB_NAME", "vigex_logs")
LOGS_DB_USER = os.getenv("LOGS_DB_USER", "vigex_logs")
LOGS_DB_PASS = os.getenv("LOGS_DB_PASS", "vigexpass")
LOGS_ORIGIN = os.getenv("LOGS_ORIGIN", "vigex-web")

TERMINAL_MAIN_HOST = os.getenv("TERMINAL_MAIN_HOST", "127.0.0.1")
TERMINAL_DATABASE_HOST = os.getenv("TERMINAL_DATABASE_HOST", LOGS_DB_HOST)
TERMINAL_TIMEOUT = int(os.getenv("TERMINAL_TIMEOUT", "30"))
TERMINAL_MAX_COMMAND_LENGTH = int(os.getenv("TERMINAL_MAX_COMMAND_LENGTH", "4000"))

SCRIPT_SERVICIOS = os.getenv("SCRIPT_SERVICIOS", "/usr/local/bin/servicios_api.sh")
SCRIPT_BACKUPS = os.getenv("SCRIPT_BACKUPS", "/usr/local/bin/backups_api.sh")
SCRIPT_RESTORE = os.getenv("SCRIPT_RESTORE", "/usr/local/bin/restore_api.sh")
BACKUP_AUTOMATION_MARKER = "# VIGEX_BACKUP_AUTO"
BACKUP_AUTOMATION_LOG = os.getenv("BACKUP_AUTOMATION_LOG", "/home/vigex/backups/.vigex/cron.log")


# =====================
# CONFIG SSH ENDURECIDO
# =====================
SSH_KEY_PATH = os.getenv("VIGEX_SSH_KEY", "/opt/vigex/api/.ssh/id_rsa_vigex")
SSH_KNOWN_HOSTS_PATH = os.getenv("VIGEX_SSH_KNOWN_HOSTS", "/opt/vigex/api/.ssh/known_hosts_vigex")
SSH_TIMEOUT = int(os.getenv("VIGEX_SSH_TIMEOUT", "30"))
SSH_CONNECT_TIMEOUT = int(os.getenv("VIGEX_SSH_CONNECT_TIMEOUT", "10"))
SSH_STDIN_MAX_LENGTH = int(os.getenv("VIGEX_SSH_STDIN_MAX_LENGTH", "20000"))

_default_ssh_hosts = f"{SERVIDOR_BACKUPS},{SERVIDOR_SERVICIOS}"
SSH_ALLOWED_HOSTS = {
    item.strip()
    for item in os.getenv("VIGEX_SSH_ALLOWED_HOSTS", _default_ssh_hosts).split(",")
    if item.strip()
}


# =====================
# CONFIG NOTIFICACIONES PROACTIVAS (R-060 / Ruta 7.5)
# =====================
NOTIF_ENABLED        = os.getenv("NOTIF_ENABLED", "false").lower() == "true"
NOTIF_EMAIL_TO       = os.getenv("NOTIF_EMAIL_TO", "").strip()
NOTIF_EMAIL_FROM     = os.getenv("NOTIF_EMAIL_FROM", "").strip()
NOTIF_SMTP_HOST      = os.getenv("NOTIF_SMTP_HOST", "").strip()
NOTIF_SMTP_PORT      = int(os.getenv("NOTIF_SMTP_PORT", "587"))
NOTIF_SMTP_USER      = os.getenv("NOTIF_SMTP_USER", "").strip()
NOTIF_SMTP_PASS      = os.getenv("NOTIF_SMTP_PASS", "").strip()
NOTIF_DISK_THRESHOLD = int(os.getenv("NOTIF_DISK_THRESHOLD", "80"))
NOTIF_CHECK_INTERVAL = int(os.getenv("NOTIF_CHECK_INTERVAL", "900"))   # segundos (15 min)
NOTIF_COOLDOWN       = int(os.getenv("NOTIF_COOLDOWN", "14400"))        # segundos entre alertas iguales (4 h)


def is_allowed_ssh_host(host: str) -> bool:
    return bool(host and host in SSH_ALLOWED_HOSTS)


def validate_ssh_run(host: str, script: str, args: list[str]) -> None:
    if not is_allowed_ssh_host(host):
        raise ValueError(f"Host SSH no permitido: {host}")

    allowed_scripts = {
        SCRIPT_SERVICIOS,
        SCRIPT_BACKUPS,
        SCRIPT_RESTORE,
        "cat",
        "crontab",
        "/bin/bash",
        "df",  # R-058 dashboard 7.2: uso de disco (solo df -h /)
    }

    if script not in allowed_scripts:
        raise ValueError(f"Script SSH no permitido: {script}")

    if any(len(str(arg)) > 1000 for arg in args):
        raise ValueError("Argumento SSH demasiado largo")

    # R-059 monitoreo 7.4: cat permitido solo para estos ficheros exactos
    _CAT_ALLOWED = {
        "/home/vigex/backups/.vigex/history.tsv",      # historial de backups
        "/home/vigex/backups/.vigex/checksums.sha256",  # checksums SHA256 (R-064 / 7.9)
        "/proc/loadavg",   # carga del sistema
        "/proc/meminfo",   # información de memoria RAM
        "/proc/uptime",    # tiempo activo del sistema
    }
    if script == "cat" and (not args or len(args) != 1 or args[0] not in _CAT_ALLOWED):
        raise ValueError(f"cat: ruta no permitida. Rutas válidas: {', '.join(sorted(_CAT_ALLOWED))}")

    if script == "crontab" and args != ["-l"]:
        raise ValueError("Uso de crontab no permitido")

    if script == "/bin/bash" and args != ["-lc", "hostname && date"]:
        raise ValueError("Uso de /bin/bash no permitido en ssh_run")

    if script == "df" and args != ["-h", "/"]:
        raise ValueError("Uso de df no permitido (solo df -h /)")


def build_ssh_base_command(host: str) -> list[str]:
    return [
        "ssh",
        "-i", SSH_KEY_PATH,
        "-o", "BatchMode=yes",
        "-o", "StrictHostKeyChecking=yes",
        "-o", f"UserKnownHostsFile={SSH_KNOWN_HOSTS_PATH}",
        "-o", f"ConnectTimeout={SSH_CONNECT_TIMEOUT}",
        f"{USUARIO}@{host}",
    ]


# =====================
# ALERTAS TELEGRAM
# =====================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()
ALERTS_DB_PATH = os.getenv("ALERTS_DB_PATH", "data/alerts.db")
ALERTS_DEFAULT_CHANNEL = os.getenv("ALERTS_DEFAULT_CHANNEL", "telegram")

# =====================
# USUARIOS Y PERMISOS
# =====================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
USERS_FILE = DATA_DIR / "users.json"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
PASSWORD_HASH_PREFIXES = ("$2a$", "$2b$", "$2y$")
AUTH_LOGS_FILE = DATA_DIR / "auth_logs.json"

AVAILABLE_PERMISSIONS = {
    "logs": "Logs",
    "backups": "Copias",
    "servicios": "Servicios",
    "alertas": "Alertas",
    "terminal": "Terminal",
    "asistente": "Asistente IA",   # R-090: permiso para acceder al chat IA
}


def ensure_users_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not USERS_FILE.exists():
        USERS_FILE.write_text("[]", encoding="utf-8")


def is_password_hash(value: str) -> bool:
    return isinstance(value, str) and value.startswith(PASSWORD_HASH_PREFIXES)


def hash_password(password: str) -> str:
    return pwd_context.hash(password or "")


def password_or_empty(value: str) -> str:
    return value or ""


def verify_password(plain_password: str, stored_password: str) -> bool:
    plain_password = password_or_empty(plain_password)
    stored_password = password_or_empty(stored_password)

    if not stored_password:
        return False

    if is_password_hash(stored_password):
        try:
            return pwd_context.verify(plain_password, stored_password)
        except Exception:
            return False

    # Compatibilidad temporal con usuarios antiguos en texto plano.
    return plain_password == stored_password


def ensure_auth_logs_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not AUTH_LOGS_FILE.exists():
        AUTH_LOGS_FILE.write_text("[]", encoding="utf-8")


def load_auth_logs(limit: int | None = 200) -> list[dict[str, Any]]:
    ensure_auth_logs_file()
    try:
        data = json.loads(AUTH_LOGS_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list):
            valid_logs: list[dict[str, Any]] = []
            for item in data:
                if isinstance(item, dict):
                    valid_logs.append(
                        {
                            "fecha": str(item.get("fecha", "")),
                            "accion": str(item.get("accion", "")),
                            "usuario": str(item.get("usuario", "anon")),
                            "resultado": str(item.get("resultado", "")),
                            "ip_origen": str(item.get("ip_origen", "")),
                            "user_agent": str(item.get("user_agent", "")),
                            "rol": str(item.get("rol", "")),
                            "detalle": str(item.get("detalle", "")),
                        }
                    )
            valid_logs.reverse()
            if limit is None:
                return valid_logs
            return valid_logs[:limit]
    except Exception as e:
        print(f"Error cargando logs de inicio de sesión: {e}")
    return []


def save_auth_logs(logs: list[dict[str, Any]]) -> None:
    ensure_auth_logs_file()
    AUTH_LOGS_FILE.write_text(
        json.dumps(logs, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def register_auth_log(
    request: Request,
    accion: str,
    usuario: str | None,
    resultado: str,
    rol: str | None = None,
    detalle: str | None = None,
) -> None:
    ensure_auth_logs_file()
    ip_origen = request.client.host if request.client else "desconocida"
    user_agent = request.headers.get("user-agent", "desconocido")

    try:
        logs = json.loads(AUTH_LOGS_FILE.read_text(encoding="utf-8"))
        if not isinstance(logs, list):
            logs = []
    except Exception:
        logs = []

    logs.append(
        {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "accion": accion,
            "usuario": (usuario or "anon").strip() or "anon",
            "resultado": resultado,
            "ip_origen": ip_origen,
            "user_agent": user_agent,
            "rol": rol or "",
            "detalle": detalle or "",
        }
    )

    logs = logs[-1000:]
    save_auth_logs(logs)


def normalize_permissions(permissions: Any) -> list[str]:
    if not isinstance(permissions, list):
        return []

    result: list[str] = []
    for p in permissions:
        if p in AVAILABLE_PERMISSIONS and p not in result:
            result.append(p)
    return result


def load_users() -> list[dict[str, Any]]:
    ensure_users_file()
    try:
        data = json.loads(USERS_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list):
            valid_users: list[dict[str, Any]] = []
            changed = False

            for item in data:
                if isinstance(item, dict) and item.get("username"):
                    username = str(item.get("username")).strip()
                    permissions = normalize_permissions(item.get("permissions", []))

                    password_hash = str(item.get("password_hash", "")).strip()
                    legacy_password = str(item.get("password", ""))

                    if password_hash:
                        stored_hash = password_hash
                    elif legacy_password:
                        stored_hash = hash_password(legacy_password)
                        changed = True
                    else:
                        stored_hash = ""

                    valid_users.append(
                        {
                            "username": username,
                            "password_hash": stored_hash,
                            "permissions": permissions,
                        }
                    )

            if changed:
                save_users(valid_users)

            return valid_users

    except Exception:
        pass

    return []


def save_users(users: list[dict[str, Any]]) -> None:
    ensure_users_file()
    safe_users: list[dict[str, Any]] = []

    for user in users:
        if not isinstance(user, dict) or not user.get("username"):
            continue

        safe_users.append(
            {
                "username": str(user.get("username")).strip(),
                "password_hash": str(user.get("password_hash", "")),
                "permissions": normalize_permissions(user.get("permissions", [])),
            }
        )

    USERS_FILE.write_text(
        json.dumps(safe_users, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def find_user(username: str) -> dict[str, Any] | None:
    username = (username or "").strip()
    for user in load_users():
        if user["username"] == username:
            return user
    return None


def get_auth_user(username: str, password: str) -> dict[str, Any] | None:
    username = (username or "").strip()
    password = password or ""

    # Admin configurado por config.env.
    # Compatible con contraseña plana o hash bcrypt.
    if username == ADMIN_USER and verify_password(password, ADMIN_PASSWORD):
        return {
            "username": ADMIN_USER,
            "permissions": list(AVAILABLE_PERMISSIONS.keys()),
            "is_admin": True,
        }

    # Usuarios creados desde panel.
    user = find_user(username)
    stored_password = ""
    if user:
        stored_password = user.get("password_hash") or user.get("password", "")

    if user and verify_password(password, stored_password):
        return {
            "username": user["username"],
            "permissions": normalize_permissions(user.get("permissions", [])),
            "is_admin": False,
        }

    return None


# =====================
# PROTECCIÓN FUERZA BRUTA LOGIN (M-3)
# =====================
# Limitador en memoria por IP. Apropiado para el despliegue de un solo worker
# de Uvicorn. Si se escalan los workers, conviene un almacén compartido.
LOGIN_MAX_ATTEMPTS = int(os.getenv("VIGEX_LOGIN_MAX_ATTEMPTS", "5"))
LOGIN_WINDOW_SECONDS = int(os.getenv("VIGEX_LOGIN_WINDOW_SECONDS", "900"))
_login_failures: dict[str, list[float]] = {}


def _login_prune(ip: str, now: float) -> list[float]:
    recientes = [t for t in _login_failures.get(ip, []) if now - t < LOGIN_WINDOW_SECONDS]
    if recientes:
        _login_failures[ip] = recientes
    else:
        _login_failures.pop(ip, None)
    return recientes


def login_is_blocked(ip: str) -> bool:
    now = datetime.now().timestamp()
    return len(_login_prune(ip, now)) >= LOGIN_MAX_ATTEMPTS


def register_login_failure(ip: str) -> None:
    now = datetime.now().timestamp()
    intentos = _login_prune(ip, now)
    intentos.append(now)
    _login_failures[ip] = intentos


def reset_login_failures(ip: str) -> None:
    _login_failures.pop(ip, None)


def is_authenticated(request: Request) -> bool:
    return request.session.get("user") is not None


def is_admin(request: Request) -> bool:
    return bool(request.session.get("is_admin", False))


def get_permissions(request: Request) -> list[str]:
    permissions = request.session.get("permissions", [])
    if not isinstance(permissions, list):
        return []
    return permissions


def has_permission(request: Request, permission: str) -> bool:
    return is_admin(request) or permission in get_permissions(request)


def permission_labels_from_keys(keys: list[str]) -> list[str]:
    return [AVAILABLE_PERMISSIONS[k] for k in keys if k in AVAILABLE_PERMISSIONS]


def get_common_context(request: Request) -> dict[str, Any]:
    perms = get_permissions(request)
    admin = is_admin(request)
    effective_keys = list(AVAILABLE_PERMISSIONS.keys()) if admin else perms

    return {
        "user": request.session.get("user"),
        "is_admin": admin,
        "role_label": "Administrador" if admin else "Usuario",
        "can_logs": admin or "logs" in perms,
        "can_backups": admin or "backups" in perms,
        "can_servicios": admin or "servicios" in perms,
        "can_alertas": admin or "alertas" in perms,
        "can_terminal": admin or "terminal" in perms,
        "permission_labels": permission_labels_from_keys(effective_keys),
        "permissions_count": len(effective_keys),
        "auto_logout_minutes": AUTO_LOGOUT_MINUTES,
    }


def permission_redirect(message: str = "No tienes permisos para acceder a esta sección."):
    return RedirectResponse(url=f"/?msg={quote(message)}", status_code=303)


# =====================
# ALERTAS SQLITE
# =====================
def resolve_alerts_db_path() -> Path:
    raw_path = (ALERTS_DB_PATH or "").strip()
    if not raw_path or raw_path.startswith("/ruta/real/al/proyecto"):
        return BASE_DIR / "data" / "alerts.db"

    db_path = Path(raw_path)
    if not db_path.is_absolute():
        db_path = BASE_DIR / db_path
    return db_path


def get_db() -> sqlite3.Connection:
    db_path = resolve_alerts_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn



def init_alerts_db() -> None:
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS alert_channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            is_enabled INTEGER NOT NULL DEFAULT 1,
            token TEXT,
            destination TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS alert_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_code TEXT NOT NULL,
            severity TEXT NOT NULL,
            channel_code TEXT NOT NULL,
            is_enabled INTEGER NOT NULL DEFAULT 1
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS alert_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_code TEXT NOT NULL,
            severity TEXT NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            source TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS alert_deliveries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            channel_code TEXT NOT NULL,
            recipient_id INTEGER,
            recipient_name TEXT,
            destination TEXT,
            status TEXT NOT NULL,
            response_text TEXT,
            delivered_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(event_id) REFERENCES alert_events(id)
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS alert_recipients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_code TEXT NOT NULL,
            company TEXT,
            name TEXT NOT NULL,
            username TEXT,
            kind TEXT NOT NULL DEFAULT 'user',
            destination TEXT NOT NULL,
            is_enabled INTEGER NOT NULL DEFAULT 1,
            is_default INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cur.execute(
        """
        INSERT OR IGNORE INTO alert_channels(code, name, is_enabled, token, destination)
        VALUES (?, ?, ?, ?, ?)
        """,
        ("telegram", "Telegram", 1, "", ""),
    )

    default_rules = [
        ("backup.ok", "info", "telegram", 0),
        ("backup.error", "critical", "telegram", 1),
        ("service.ok", "info", "telegram", 0),
        ("service.error", "critical", "telegram", 1),
        ("api.error", "critical", "telegram", 1),
    ]
    for event_code, severity, channel_code, is_enabled in default_rules:
        cur.execute(
            """
            INSERT INTO alert_rules(event_code, severity, channel_code, is_enabled)
            SELECT ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM alert_rules
                WHERE event_code = ? AND channel_code = ?
            )
            """,
            (event_code, severity, channel_code, is_enabled, event_code, channel_code),
        )

    conn.commit()
    conn.close()
    sync_channel_destination()


def sync_channel_destination() -> None:
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT destination
        FROM alert_recipients
        WHERE channel_code = 'telegram' AND is_default = 1
        LIMIT 1
        """
    )
    row = cur.fetchone()
    destination = row["destination"] if row else ""
    cur.execute(
        """
        UPDATE alert_channels
        SET token = ?, destination = ?
        WHERE code = 'telegram'
        """,
        (TELEGRAM_BOT_TOKEN, destination),
    )
    conn.commit()
    conn.close()


def get_default_recipient(channel_code: str = "telegram") -> dict[str, Any] | None:
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT *
        FROM alert_recipients
        WHERE channel_code = ? AND is_default = 1
        LIMIT 1
        """,
        (channel_code,),
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def get_enabled_recipients(channel_code: str = "telegram") -> list[dict[str, Any]]:
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT *
        FROM alert_recipients
        WHERE channel_code = ? AND is_enabled = 1
        ORDER BY is_default DESC, id ASC
        """,
        (channel_code,),
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def ensure_default_recipient() -> None:
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id FROM alert_recipients
        WHERE channel_code = 'telegram' AND is_default = 1
        LIMIT 1
        """
    )
    has_default = cur.fetchone()
    if not has_default:
        cur.execute(
            """
            SELECT id
            FROM alert_recipients
            WHERE channel_code = 'telegram' AND is_enabled = 1
            ORDER BY id ASC
            LIMIT 1
            """
        )
        first_enabled = cur.fetchone()
        if first_enabled:
            cur.execute(
                "UPDATE alert_recipients SET is_default = 1 WHERE id = ?",
                (first_enabled["id"],),
            )
    conn.commit()
    conn.close()
    sync_channel_destination()


def fetch_recent_telegram_chats() -> list[dict[str, Any]]:
    token = TELEGRAM_BOT_TOKEN
    if not token:
        return []

    url = f"https://api.telegram.org/bot{token}/getUpdates"
    req = UrlRequest(url, method="GET")

    with urlopen(req, timeout=20) as response:
        raw = response.read().decode("utf-8", errors="replace")
        data = json.loads(raw)

    if not data.get("ok"):
        return []

    unique: dict[str, dict[str, Any]] = {}
    updates = data.get("result", [])
    for item in reversed(updates):
        message = item.get("message") or item.get("edited_message") or item.get("channel_post") or {}
        chat = message.get("chat") or {}
        chat_id = str(chat.get("id", "")).strip()
        if not chat_id or chat_id in unique:
            continue

        chat_type = chat.get("type", "unknown")
        username = ""
        if chat_type == "private":
            if chat.get("username"):
                username = f"@{chat.get('username')}"
            else:
                full_name = " ".join([str(chat.get("first_name") or "").strip(), str(chat.get("last_name") or "").strip()]).strip()
                username = full_name or "(sin username)"
        else:
            username = str(chat.get("title") or chat.get("username") or "(grupo sin nombre)").strip()

        unique[chat_id] = {
            "chat_id": chat_id,
            "username": username,
            "kind": "group" if chat_type in ("group", "supergroup") else "user",
            "chat_type": chat_type,
        }

    return list(unique.values())


# L-5: inicialización movida a la función `lifespan` (ver arriba).



def send_telegram_message(text: str, chat_id: str | None = None) -> dict[str, Any]:
    token = TELEGRAM_BOT_TOKEN
    target_chat = (chat_id or "").strip()

    if not token:
        return {"ok": False, "status": "ERROR", "text": "Falta TELEGRAM_BOT_TOKEN en config.env"}

    if not target_chat:
        return {"ok": False, "status": "ERROR", "text": "No hay destinatario configurado. Añade un chat o grupo en Alertas."}

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps(
        {
            "chat_id": target_chat,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
    ).encode("utf-8")

    req = UrlRequest(
        url,
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    try:
        with urlopen(req, timeout=15) as response:
            raw = response.read().decode("utf-8", errors="replace")
            data = json.loads(raw)
            return {
                "ok": bool(data.get("ok") is True),
                "status": response.status,
                "text": json.dumps(data, ensure_ascii=False),
            }
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else str(e)
        return {"ok": False, "status": e.code, "text": body}
    except URLError as e:
        return {"ok": False, "status": "ERROR", "text": str(e.reason)}
    except Exception as e:
        return {"ok": False, "status": "ERROR", "text": str(e)}



def emit_alert(event_code: str, severity: str, title: str, message: str, source: str) -> int:
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO alert_events(event_code, severity, title, message, source)
        VALUES (?, ?, ?, ?, ?)
        """,
        (event_code, severity, title, message, source),
    )
    event_id = int(cur.lastrowid)

    cur.execute(
        """
        SELECT r.channel_code
        FROM alert_rules r
        JOIN alert_channels c ON c.code = r.channel_code
        WHERE r.event_code = ? AND r.is_enabled = 1 AND c.is_enabled = 1
        """,
        (event_code,),
    )
    rules = cur.fetchall()
    channels = [row["channel_code"] for row in rules] or [ALERTS_DEFAULT_CHANNEL]

    for channel_code in channels:
        if channel_code == "telegram":
            recipients = get_enabled_recipients("telegram")
            if not recipients:
                cur.execute(
                    """
                    INSERT INTO alert_deliveries(event_id, channel_code, recipient_id, recipient_name, destination, status, response_text)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (event_id, channel_code, None, None, None, "ERROR", "No hay destinatarios Telegram activos"),
                )
                continue

            for recipient in recipients:
                result = send_telegram_message(message, recipient["destination"])
                status = "OK" if result["ok"] else "ERROR"
                cur.execute(
                    """
                    INSERT INTO alert_deliveries(event_id, channel_code, recipient_id, recipient_name, destination, status, response_text)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        event_id,
                        channel_code,
                        recipient["id"],
                        recipient["name"],
                        recipient["destination"],
                        status,
                        result["text"],
                    ),
                )

    conn.commit()
    conn.close()
    return event_id


def get_alert_stats() -> dict[str, Any]:
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) AS total FROM alert_events")
    total_events = int(cur.fetchone()["total"])

    cur.execute("SELECT COUNT(*) AS total FROM alert_deliveries")
    total_deliveries = int(cur.fetchone()["total"])

    cur.execute("SELECT COUNT(*) AS total FROM alert_deliveries WHERE status = 'OK'")
    ok_deliveries = int(cur.fetchone()["total"])

    cur.execute("SELECT delivered_at FROM alert_deliveries ORDER BY id DESC LIMIT 1")
    last_delivery = cur.fetchone()

    conn.close()

    return {
        "alerts_total": total_events,
        "alerts_deliveries": total_deliveries,
        "alerts_ok": ok_deliveries,
        "alerts_error": total_deliveries - ok_deliveries,
        "alerts_last": last_delivery["delivered_at"] if last_delivery else None,
    }


# =====================
# SSH + LOGS
# =====================
def ssh_run(host: str, script: str, args: list[str]) -> dict[str, Any]:
    try:
        validate_ssh_run(host, script, args)
        # Seguridad (H-1): OpenSSH reconcatena los operandos con espacios y los
        # entrega al shell del host remoto, que sí interpreta metacaracteres.
        # Para evitar inyección de comandos a través de argumentos (p. ej. ';',
        # '$()', backticks o espacios) se construye un único comando remoto con
        # cada token escapado mediante shlex.quote.
        remote_command = " ".join(shlex.quote(part) for part in [script, *args])
        cmd = build_ssh_base_command(host) + [remote_command]

        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=SSH_TIMEOUT,
        )

        out = (res.stdout or "").strip()
        err = (res.stderr or "").strip()

        return {
            "ok": res.returncode == 0,
            "code": res.returncode,
            "host": host,
            "script": script,
            "stdout": out,
            "stderr": err,
            "text": out if res.returncode == 0 else f"ERROR ({res.returncode}): {err or out}",
        }

    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "code": 124,
            "host": host,
            "script": script,
            "stdout": "",
            "stderr": "Timeout SSH",
            "text": f"ERROR (124): Timeout SSH tras {SSH_TIMEOUT} segundos",
        }

    except Exception as e:
        return {
            "ok": False,
            "code": 1,
            "host": host,
            "script": script,
            "stdout": "",
            "stderr": str(e),
            "text": f"ERROR: {e}",
        }


def ssh_run_stdin(host: str, script_text: str) -> dict[str, Any]:
    try:
        if not is_allowed_ssh_host(host):
            raise ValueError(f"Host SSH no permitido: {host}")

        if len(script_text or "") > SSH_STDIN_MAX_LENGTH:
            raise ValueError("Script remoto demasiado largo")

        cmd = build_ssh_base_command(host) + ["bash", "-s"]

        res = subprocess.run(
            cmd,
            input=script_text,
            capture_output=True,
            text=True,
            timeout=SSH_TIMEOUT,
        )

        out = (res.stdout or "").strip()
        err = (res.stderr or "").strip()

        return {
            "ok": res.returncode == 0,
            "code": res.returncode,
            "host": host,
            "script": "bash -s",
            "stdout": out,
            "stderr": err,
            "text": out if res.returncode == 0 else f"ERROR ({res.returncode}): {err or out}",
        }

    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "code": 124,
            "host": host,
            "script": "bash -s",
            "stdout": "",
            "stderr": "Timeout SSH",
            "text": f"ERROR (124): Timeout SSH tras {SSH_TIMEOUT} segundos",
        }

    except Exception as e:
        return {
            "ok": False,
            "code": 1,
            "host": host,
            "script": "bash -s",
            "stdout": "",
            "stderr": str(e),
            "text": f"ERROR: {e}",
        }


def cargar_historial_backups(limit: int = 50) -> list[dict[str, str]]:
    """Carga el historial generado por backups_api.sh desde el servidor de backups."""

    result = ssh_run(
        SERVIDOR_BACKUPS,
        "cat",
        ["/home/vigex/backups/.vigex/history.tsv"],
    )

    raw = result.get("stdout", "") if result.get("ok") else ""

    if not raw.strip():
        return []

    lines = [line for line in raw.splitlines() if line.strip()]

    if len(lines) <= 1:
        return []

    header = lines[0].split("\t")
    history: list[dict[str, str]] = []

    for line in lines[1:]:
        parts = line.split("\t")

        while len(parts) < len(header):
            parts.append("")

        item = dict(zip(header, parts))

        path = item.get("file", "")
        item["filename"] = path.split("/")[-1] if path else "-"

        backup_type = item.get("type", "")

        if backup_type == "full":
            item["tipo_label"] = "Completo"
        elif backup_type == "incremental":
            item["tipo_label"] = "Incremental"
        elif backup_type == "differential":
            item["tipo_label"] = "Diferencial"
        else:
            item["tipo_label"] = backup_type or "-"

        item["rango"] = "-"

        if item.get("start_file") and item.get("start_pos") and item.get("end_file") and item.get("end_pos"):
            item["rango"] = f"{item['start_file']}:{item['start_pos']} → {item['end_file']}:{item['end_pos']}"

        # Alias: backups_api.sh escribe la columna 'timestamp'; normalizar a 'date'
        # para que dashboard, salud e integridad no muestren '—' (R-083-fix-1)
        if not item.get("date"):
            item["date"] = item.get("timestamp", "")

        # Alias: backups_api.sh escribe la columna 'path'; normalizar a 'file'
        # para que la descarga no falle con "no tiene archivo asociado" (R-083-fix-5a)
        if not item.get("file"):
            item["file"] = item.get("path", "")

        history.append(item)

    return list(reversed(history[-limit:]))


def backup_has_incremental_base(db: str, history: list[dict[str, str]]) -> bool:
    db = (db or "").strip()
    for item in history:
        if item.get("db") == db and item.get("end_file") and item.get("end_pos"):
            return True
    return False


def backup_has_full_base(db: str, history: list[dict[str, str]]) -> bool:
    db = (db or "").strip()
    for item in history:
        if item.get("db") == db and item.get("type") == "full" and item.get("end_file") and item.get("end_pos"):
            return True
    return False


def backup_type_label(tipo: str) -> str:
    if tipo == "full":
        return "Completo"
    if tipo == "incremental":
        return "Incremental"
    if tipo == "differential":
        return "Diferencial"
    return tipo or "-"


def es_token_simple(valor: str, extra: str = "._-", max_len: int = 128) -> bool:
    """Valida que un valor solo contenga caracteres seguros (sin metacaracteres
    de shell). Defensa en profundidad para argumentos que viajan por SSH."""
    valor = (valor or "").strip()
    if not valor or len(valor) > max_len:
        return False
    return all(ch.isalnum() or ch in extra for ch in valor)


def build_backup_cron_expression(schedule_type: str, schedule_time: str, weekday: str, monthday: str) -> tuple[str, str]:
    schedule_type = (schedule_type or "daily").strip()
    schedule_time = (schedule_time or "02:00").strip()
    weekday = (weekday or "1").strip()
    monthday = (monthday or "1").strip()

    if ":" not in schedule_time:
        raise ValueError("La hora debe tener formato HH:MM.")

    hour_raw, minute_raw = schedule_time.split(":", 1)

    if not hour_raw.isdigit() or not minute_raw.isdigit():
        raise ValueError("La hora debe tener formato HH:MM.")

    hour = int(hour_raw)
    minute = int(minute_raw)

    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        raise ValueError("La hora indicada no es válida.")

    if schedule_type == "hourly":
        return f"{minute} * * * *", f"Cada hora en el minuto {minute:02d}"

    if schedule_type == "daily":
        return f"{minute} {hour} * * *", f"Cada día a las {hour:02d}:{minute:02d}"

    if schedule_type == "weekly":
        if weekday not in ["0", "1", "2", "3", "4", "5", "6"]:
            raise ValueError("El día de la semana no es válido.")
        weekday_labels = {
            "0": "domingo",
            "1": "lunes",
            "2": "martes",
            "3": "miércoles",
            "4": "jueves",
            "5": "viernes",
            "6": "sábado",
        }
        return f"{minute} {hour} * * {weekday}", f"Cada {weekday_labels[weekday]} a las {hour:02d}:{minute:02d}"

    if schedule_type == "monthly":
        if not monthday.isdigit():
            raise ValueError("El día del mes no es válido.")
        day = int(monthday)
        if day < 1 or day > 28:
            raise ValueError("Para evitar problemas con meses cortos, usa un día entre 1 y 28.")
        return f"{minute} {hour} {day} * *", f"Día {day} de cada mes a las {hour:02d}:{minute:02d}"

    raise ValueError("La frecuencia seleccionada no es válida.")


def build_backup_automation_name(tipo: str, db: str) -> str:
    prefix = {
        "full": "auto-full",
        "incremental": "auto-inc",
        "differential": "auto-diff",
    }.get(tipo, "auto-backup")
    clean_db = "".join(ch if ch.isalnum() or ch in ["_", "-"] else "_" for ch in db.strip()) or "db"
    return f"{prefix}-{clean_db}-YYYYMMDD-HHMM.sql"


def cargar_automatizaciones_backups() -> list[dict[str, Any]]:
    result = ssh_run(SERVIDOR_BACKUPS, "crontab", ["-l"])

    if not result.get("ok") and "no crontab" not in result.get("text", "").lower():
        return []

    raw = result.get("stdout", "") if result.get("ok") else ""
    lines = raw.splitlines()
    automations: list[dict[str, Any]] = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if line.startswith(BACKUP_AUTOMATION_MARKER):
            metadata_raw = line.replace(BACKUP_AUTOMATION_MARKER, "", 1).strip()
            command_line = ""

            if i + 1 < len(lines):
                command_line = lines[i + 1].strip()

            try:
                metadata = json.loads(metadata_raw)
                if isinstance(metadata, dict):
                    metadata["cron_line"] = command_line
                    metadata["tipo_label"] = backup_type_label(str(metadata.get("type", "")))
                    automations.append(metadata)
            except Exception:
                pass

            i += 2
            continue

        i += 1

    return list(reversed(automations))


def crear_automatizacion_backup_remota(metadata: dict[str, Any], cron_expression: str, command_line: str) -> dict[str, Any]:
    metadata_json = json.dumps(metadata, ensure_ascii=False)
    block = f"{BACKUP_AUTOMATION_MARKER} {metadata_json}\n{cron_expression} {command_line}\n"

    script = f"""
set -euo pipefail
TMP="$(mktemp)"
crontab -l 2>/dev/null > "$TMP" || true
cat >> "$TMP" <<'VIGEX_CRON_BLOCK'
{block.rstrip()}
VIGEX_CRON_BLOCK
crontab "$TMP"
rm -f "$TMP"
mkdir -p "$(dirname {shlex.quote(BACKUP_AUTOMATION_LOG)})"
echo "OK: Automatización creada con ID {metadata['id']}"
"""
    return ssh_run_stdin(SERVIDOR_BACKUPS, script)


def eliminar_automatizacion_backup_remota(automation_id: str) -> dict[str, Any]:
    automation_id = (automation_id or "").strip()

    if not automation_id:
        return {
            "ok": False,
            "code": 400,
            "stdout": "",
            "stderr": "",
            "text": "ERROR: No se ha indicado ninguna automatización.",
        }

    script = f"""
set -euo pipefail
AUTO_ID={shlex.quote(automation_id)}
TMP_IN="$(mktemp)"
TMP_OUT="$(mktemp)"
crontab -l 2>/dev/null > "$TMP_IN" || true
SKIP_NEXT=0
FOUND=0
while IFS= read -r LINE; do
  if [[ "$SKIP_NEXT" == "1" ]]; then
    SKIP_NEXT=0
    continue
  fi

  if [[ "$LINE" == "{BACKUP_AUTOMATION_MARKER}"* && "$LINE" == *"\\\"id\\\": \\\"$AUTO_ID\\\""* ]]; then
    FOUND=1
    SKIP_NEXT=1
    continue
  fi

  printf '%s\n' "$LINE" >> "$TMP_OUT"
done < "$TMP_IN"
crontab "$TMP_OUT"
rm -f "$TMP_IN" "$TMP_OUT"
if [[ "$FOUND" == "1" ]]; then
  echo "OK: Automatización eliminada con ID $AUTO_ID"
else
  echo "ERROR: No existe una automatización con ID $AUTO_ID"
  exit 1
fi
"""
    return ssh_run_stdin(SERVIDOR_BACKUPS, script)


def plan_eliminacion_backups(backup_id: int, history: list[dict[str, str]]) -> dict[str, Any]:

    target_id = str(backup_id)

    by_id: dict[str, dict[str, str]] = {}
    children: dict[str, list[dict[str, str]]] = {}

    for item in history:
        item_id = str(item.get("id", "")).strip()
        if not item_id:
            continue

        by_id[item_id] = item

        base_id = str(item.get("base_id", "") or "").strip()
        if base_id:
            children.setdefault(base_id, []).append(item)

    if target_id not in by_id:
        raise ValueError(f"No existe ningún backup con ID={backup_id}.")

    for key in children:
        children[key].sort(key=lambda x: int(str(x.get("id", "0")) or 0))

    ids_to_delete: list[str] = []
    visited: set[str] = set()

    def visit(current_id: str) -> None:
        if current_id in visited:
            return

        visited.add(current_id)
        ids_to_delete.append(current_id)

        for child in children.get(current_id, []):
            child_id = str(child.get("id", "")).strip()
            if child_id:
                visit(child_id)

    visit(target_id)

    items = [by_id[item_id] for item_id in ids_to_delete if item_id in by_id]

    return {
        "target": by_id[target_id],
        "items": items,
        "ids": ids_to_delete,
        "ids_csv": ", ".join(ids_to_delete),
        "has_dependents": len(ids_to_delete) > 1,
        "dependents_count": max(0, len(ids_to_delete) - 1),
    }



def plan_restauracion_backups(backup_id: int, history: list[dict[str, str]]) -> dict[str, Any]:
    """Calcula la cadena de restauración desde un full hasta el backup seleccionado."""

    target_id = str(backup_id)
    by_id: dict[str, dict[str, str]] = {}

    for item in history:
        item_id = str(item.get("id", "")).strip()
        if item_id:
            by_id[item_id] = item

    if target_id not in by_id:
        raise ValueError(f"No existe ningún backup con ID={backup_id}.")

    reverse_chain: list[dict[str, str]] = []
    visited: set[str] = set()
    current_id = target_id

    while True:
        if current_id in visited:
            raise ValueError(f"Se ha detectado un ciclo en la cadena de restauración en ID={current_id}.")

        visited.add(current_id)

        item = by_id.get(current_id)
        if not item:
            raise ValueError(f"La cadena de restauración está rota. Falta la copia ID={current_id}.")

        reverse_chain.append(item)

        if item.get("type") == "full":
            break

        base_id = str(item.get("base_id", "") or "").strip()
        if not base_id:
            raise ValueError(f"La copia ID={current_id} no es completa y no tiene base_id.")

        current_id = base_id

    items = list(reversed(reverse_chain))
    full_item = items[0]
    target = by_id[target_id]
    db = full_item.get("db", "-")

    for item in items:
        if item.get("db") != db:
            raise ValueError("La cadena de restauración mezcla bases de datos diferentes.")

    return {
        "target": target,
        "items": items,
        "ids": [str(item.get("id")) for item in items],
        "ids_csv": ", ".join([str(item.get("id")) for item in items]),
        "db": db,
        "full": full_item,
        "has_chain": len(items) > 1,
        "chain_count": len(items),
    }


def restaurar_backup_remoto(backup_id: int) -> dict[str, Any]:
    return ssh_run(
        SERVIDOR_BACKUPS,
        SCRIPT_RESTORE,
        [str(backup_id), "/home/vigex/backups", "SI"],
    )


def buscar_backup_por_id(backup_id: int, history: list[dict[str, str]]) -> dict[str, str]:
    """Busca una copia concreta dentro del historial ya cargado."""

    target_id = str(backup_id).strip()

    for item in history:
        if str(item.get("id", "")).strip() == target_id:
            return item

    raise ValueError(f"No existe ningún backup con ID={backup_id}.")


def validar_ruta_backup_descarga(remote_path: str) -> str:
    """Valida que la ruta descargada pertenece al directorio de backups permitido."""

    raw_path = (remote_path or "").strip()

    if not raw_path:
        raise ValueError("La copia seleccionada no tiene archivo asociado.")

    if "\x00" in raw_path:
        raise ValueError("Ruta de backup no válida.")

    normalized = posixpath.normpath(raw_path)
    allowed_root = "/home/vigex/backups"

    if normalized == allowed_root:
        raise ValueError("No se puede descargar el directorio de backups completo.")

    if not normalized.startswith(f"{allowed_root}/"):
        raise ValueError("Ruta de backup no permitida para descarga.")

    return normalized


def leer_backup_remoto(remote_path: str) -> dict[str, Any]:
    """Lee un archivo de backup remoto en binario usando SSH.

    Importante: el comando remoto se envía como una única cadena.
    Si se manda como ["bash", "-lc", "..."] a ssh, OpenSSH lo recompone
    sin conservar las comillas y el test puede fallar aunque el archivo exista.
    """

    safe_path = validar_ruta_backup_descarga(remote_path)
    quoted_path = shlex.quote(safe_path)

    remote_cmd = (
        f"test -f {quoted_path} && "
        f"test -r {quoted_path} && "
        f"cat -- {quoted_path}"
    )

    cmd = [
        "ssh",
        "-i", SSH_KEY_PATH,
        "-o", "BatchMode=yes",
        "-o", "StrictHostKeyChecking=yes",
        "-o", f"UserKnownHostsFile={SSH_KNOWN_HOSTS_PATH}",
        f"{USUARIO}@{SERVIDOR_BACKUPS}",
        remote_cmd,
    ]

    res = subprocess.run(cmd, capture_output=True, timeout=SSH_TIMEOUT)
    err = (res.stderr or b"").decode("utf-8", errors="replace").strip()

    if res.returncode == 0:
        return {
            "ok": True,
            "code": 0,
            "path": safe_path,
            "content": res.stdout or b"",
            "stderr": err,
            "text": "OK",
        }

    detail = err or "No se pudo leer el archivo remoto"
    return {
        "ok": False,
        "code": res.returncode,
        "path": safe_path,
        "content": b"",
        "stderr": err,
        "text": f"ERROR ({res.returncode}): {detail}",
    }


def eliminar_backups_cascada_remoto(ids: list[str]) -> dict[str, Any]:

    clean_ids: list[str] = []

    for item_id in ids:
        item_id = str(item_id).strip()
        if not item_id.isdigit():
            return {
                "ok": False,
                "code": 400,
                "stdout": "",
                "stderr": "",
                "text": f"ERROR: ID no válido para eliminación: {item_id}",
            }
        clean_ids.append(item_id)

    if not clean_ids:
        return {
            "ok": False,
            "code": 400,
            "stdout": "",
            "stderr": "",
            "text": "ERROR: No se ha indicado ningún ID para eliminar.",
        }

    ids_str = " ".join(clean_ids)

    remote_cmd = f"""
set -euo pipefail

HIST="/home/vigex/backups/.vigex/history.tsv"
IDS="{ids_str}"

if [[ ! -f "$HIST" ]]; then
  echo "ERROR: No existe el historial de backups."
  exit 1
fi

for ID in $IDS; do
  FILE="$(awk -F'\\t' -v id="$ID" 'NR > 1 && $1 == id {{ print $5; exit }}' "$HIST")"

  if [[ -z "$FILE" ]]; then
    echo "ERROR: No existe ningún backup con ID=$ID."
    exit 2
  fi

  case "$FILE" in
    /home/vigex/backups/*)
      ;;
    *)
      echo "ERROR: Ruta no permitida para ID=$ID: $FILE"
      exit 3
      ;;
  esac

  rm -f -- "$FILE"
done

TMP="${{HIST}}.tmp.$$"
awk -F'\\t' -v ids="$IDS" '
BEGIN {{
  split(ids, arr, " ")
  for (i in arr) {{
    del[arr[i]] = 1
  }}
}}
NR == 1 || !($1 in del) {{ print }}
' "$HIST" > "$TMP"

mv "$TMP" "$HIST"

echo "OK: Backups eliminados correctamente. IDs: $IDS"
"""

    return ssh_run_stdin(SERVIDOR_BACKUPS, remote_cmd)

def log_event(
    tipo: str,
    resultado: str,
    usuario: str | None = "anon",
    ip_origen: str | None = None,
    recurso: str | None = None,
    detalle: str | None = None,
) -> None:
    if recurso and len(recurso) > 120:
        recurso = recurso[:117] + "..."

    if detalle and len(detalle) > 240:
        detalle = detalle[:237] + "..."

    try:
        conn = pymysql.connect(
            host=LOGS_DB_HOST,
            user=LOGS_DB_USER,
            password=LOGS_DB_PASS,
            database=LOGS_DB_NAME,
            autocommit=True,
            connect_timeout=2,
        )
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO eventos(origen,tipo,usuario,ip_origen,recurso,resultado,detalle)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                """,
                (LOGS_ORIGIN, tipo, usuario, ip_origen, recurso, resultado, detalle),
            )
        conn.close()
    except Exception as e:
        print(f"Error guardando evento: {e}")


class AuthAndLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ip = request.client.host if request.client else None
        path = request.url.path
        method = request.method

        public_routes = {"/login"}
        public_prefixes = ("/static", "/favicon.ico")

        is_public = path in public_routes or any(path.startswith(p) for p in public_prefixes)

        if not is_public and not is_authenticated(request):
            log_event(
                tipo="acceso",
                resultado="ERROR",
                usuario="anon",
                ip_origen=ip,
                recurso=f"{method} {path}",
                detalle="Acceso bloqueado por no autenticado",
            )
            return RedirectResponse(url="/login", status_code=303)

        try:
            response = await call_next(request)
        except Exception as e:
            usuario = request.session.get("user", "anon")
            detalle = f"Excepción no controlada: {e}"
            log_event(
                tipo="api",
                resultado="ERROR",
                usuario=usuario,
                ip_origen=ip,
                recurso=f"{method} {path}",
                detalle=detalle,
            )
            try:
                emit_alert(
                    "api.error",
                    "critical",
                    "Error interno de la API",
                    (
                        "<b>API ERROR</b>\n"
                        f"Ruta: {path}\n"
                        f"Método: {method}\n"
                        f"Detalle: {str(e)}"
                    ),
                    "api",
                )
            except Exception as alert_error:
                print(f"Error enviando alerta de API: {alert_error}")
            raise

        usuario = request.session.get("user", "anon")
        status = response.status_code

        if path.startswith("/login") or path.startswith("/logout"):
            return response

        if path in ["/", "/servicios", "/backups", "/logs", "/admin/usuarios", "/admin/login-logs", "/alertas", "/terminal"]:
            tipo = "acceso"
        elif path.startswith("/servicios"):
            tipo = "servicio"
        elif path.startswith("/backups") or path.startswith("/api/backups"):
            tipo = "backup"
        elif path.startswith("/admin"):
            tipo = "admin"
        elif path.startswith("/alertas"):
            tipo = "alerta"
        elif path.startswith("/terminal") or path.startswith("/api/terminal"):
            tipo = "terminal"
        elif path.startswith("/login") or path.startswith("/logout"):
            tipo = "login"
        else:
            tipo = "acceso"

        resultado = "OK" if status < 400 else "ERROR"
        log_event(
            tipo=tipo,
            resultado=resultado,
            usuario=usuario,
            ip_origen=ip,
            recurso=f"{method} {path}",
            detalle=f"HTTP {status}",
        )

        return response


# =====================
# CONFIG SEGURIDAD WEB (M-1 CORS, M-2 sesión)
# =====================
# CORS: por defecto sin orígenes cross-site (el panel se sirve a sí mismo y
# usa fetch del mismo origen). Si se necesita un frontend externo, indicar
# orígenes separados por comas en VIGEX_CORS_ALLOWED_ORIGINS.
_cors_origins_raw = os.getenv("VIGEX_CORS_ALLOWED_ORIGINS", "").strip()
CORS_ALLOWED_ORIGINS = [o.strip() for o in _cors_origins_raw.split(",") if o.strip()]

# Sesión: https_only configurable (activar cuando el proxy sirva HTTPS real).
SESSION_HTTPS_ONLY = os.getenv("VIGEX_SESSION_HTTPS_ONLY", "false").strip().lower() in ("1", "true", "yes", "on")
SESSION_MAX_AGE = int(os.getenv("VIGEX_SESSION_MAX_AGE", "28800"))  # 8 horas
AUTO_LOGOUT_MINUTES = int(os.getenv("VIGEX_AUTO_LOGOUT_MINUTES", "60"))  # Inactividad JS: 0=desactivado

# ── Asistente IA / RAG (R-090) ─────────────────────────────────────────────
# Fase 1: Ollama local (sin dependencias extra, solo urllib stdlib)
# Fase 2: cambiar VIGEX_RAG_LLM_PROVIDER=anthropic y añadir ANTHROPIC_API_KEY
RAG_ENABLED         = os.getenv("VIGEX_RAG_ENABLED", "true").lower() in ("1", "true", "yes")
RAG_LLM_PROVIDER    = os.getenv("VIGEX_RAG_LLM_PROVIDER", "ollama")   # "ollama" | "anthropic" | "gemini" | "openai" | "groq"
RAG_OLLAMA_URL      = os.getenv("VIGEX_RAG_OLLAMA_URL", "http://localhost:11434")
RAG_OLLAMA_MODEL    = os.getenv("VIGEX_RAG_OLLAMA_MODEL", "mistral")
RAG_ANTHROPIC_KEY   = os.getenv("ANTHROPIC_API_KEY", "")
RAG_ANTHROPIC_MODEL = os.getenv("VIGEX_RAG_ANTHROPIC_MODEL", "claude-3-haiku-20240307")
RAG_GEMINI_KEY      = os.getenv("GOOGLE_API_KEY", "")
RAG_GEMINI_MODEL    = os.getenv("VIGEX_RAG_GEMINI_MODEL", "gemini-2.0-flash")
RAG_OPENAI_KEY      = os.getenv("OPENAI_API_KEY", "")
RAG_OPENAI_MODEL    = os.getenv("VIGEX_RAG_OPENAI_MODEL", "gpt-4o-mini")
RAG_GROQ_KEY        = os.getenv("GROQ_API_KEY", "")
RAG_GROQ_MODEL      = os.getenv("VIGEX_RAG_GROQ_MODEL", "llama-3.3-70b-versatile")
RAG_TOP_K           = int(os.getenv("VIGEX_RAG_TOP_K", "5"))
RAG_MAX_TOKENS      = int(os.getenv("VIGEX_RAG_MAX_TOKENS", "700"))
# Rate limiting del asistente IA (R-090-sec): peticiones máximas por usuario en la ventana
RAG_RATE_LIMIT_REQS   = int(os.getenv("VIGEX_RAG_RATE_LIMIT_REQS", "30"))   # 30 req por usuario
RAG_RATE_LIMIT_WINDOW = int(os.getenv("VIGEX_RAG_RATE_LIMIT_WINDOW", "60")) # en una ventana de 60 s

app.add_middleware(AuthAndLogMiddleware)
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    same_site="lax",
    https_only=SESSION_HTTPS_ONLY,
    max_age=SESSION_MAX_AGE,
)

# Solo se habilita CORS si hay orígenes configurados explícitamente.
# Evita la combinación insegura allow_origins=["*"] + allow_credentials=True.
if CORS_ALLOWED_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# =====================
# LOGIN / LOGOUT
# =====================
@app.get("/login")
def login_page(request: Request):
    if is_authenticated(request):
        return RedirectResponse(url="/", status_code=303)

    error = request.query_params.get("error")
    return templates.TemplateResponse(
        request,
        "login.html",
        {
            "error": error,
        },
    )


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    ip = request.client.host if request.client else "desconocida"

    if login_is_blocked(ip):
        register_auth_log(
            request=request,
            accion="LOGIN",
            usuario=(username or "anon").strip() or "anon",
            resultado="BLOQUEADO",
            rol="No autenticado",
            detalle="Demasiados intentos fallidos; acceso temporalmente bloqueado",
        )
        return RedirectResponse(url="/login?error=2", status_code=303)

    auth_user = get_auth_user(username, password)
    if auth_user:
        reset_login_failures(ip)
        request.session["user"] = auth_user["username"]
        request.session["is_admin"] = auth_user["is_admin"]
        request.session["permissions"] = auth_user["permissions"]

        rol = "Administrador" if auth_user["is_admin"] else "Usuario"
        register_auth_log(
            request=request,
            accion="LOGIN",
            usuario=auth_user["username"],
            resultado="OK",
            rol=rol,
            detalle="Inicio de sesión correcto",
        )
        log_event(
            tipo="login",
            resultado="OK",
            usuario=auth_user["username"],
            ip_origen=request.client.host if request.client else None,
            recurso="POST /login",
            detalle="Inicio de sesión correcto",
        )
        return RedirectResponse(url="/", status_code=303)

    register_login_failure(ip)
    attempted_user = (username or "anon").strip() or "anon"
    register_auth_log(
        request=request,
        accion="LOGIN",
        usuario=attempted_user,
        resultado="ERROR",
        rol="No autenticado",
        detalle="Intento de inicio de sesión fallido",
    )
    log_event(
        tipo="login",
        resultado="ERROR",
        usuario=attempted_user,
        ip_origen=request.client.host if request.client else None,
        recurso="POST /login",
        detalle="Intento de inicio de sesión fallido",
    )

    return RedirectResponse(url="/login?error=1", status_code=303)


@app.get("/logout")
def logout_get(request: Request):
    usuario = request.session.get("user", "anon")
    rol = "Administrador" if request.session.get("is_admin", False) else "Usuario"
    register_auth_log(
        request=request,
        accion="LOGOUT",
        usuario=usuario,
        resultado="OK",
        rol=rol,
        detalle="Cierre de sesión correcto",
    )
    log_event(
        tipo="login",
        resultado="OK",
        usuario=usuario,
        ip_origen=request.client.host if request.client else None,
        recurso="GET /logout",
        detalle="Cierre de sesión correcto",
    )
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


@app.post("/logout")
def logout_post(request: Request):
    usuario = request.session.get("user", "anon")
    rol = "Administrador" if request.session.get("is_admin", False) else "Usuario"
    register_auth_log(
        request=request,
        accion="LOGOUT",
        usuario=usuario,
        resultado="OK",
        rol=rol,
        detalle="Cierre de sesión correcto",
    )
    log_event(
        tipo="login",
        resultado="OK",
        usuario=usuario,
        ip_origen=request.client.host if request.client else None,
        recurso="POST /logout",
        detalle="Cierre de sesión correcto",
    )
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


# =====================
# PANEL PRINCIPAL
# =====================
@app.get("/")
def home(request: Request):
    context = get_common_context(request)
    context["msg"] = request.query_params.get("msg")
    context["managed_sections"] = sum(
        [
            1 if context["can_backups"] else 0,
            1 if context["can_logs"] else 0,
            1 if context["can_servicios"] else 0,
            1 if context["can_alertas"] else 0,
            1 if context["can_terminal"] else 0,
            1 if context["is_admin"] else 0,
        ]
    )
    context["users_count"] = len(load_users()) + 1 if context["is_admin"] else None
    context.update(get_alert_stats())
    return templates.TemplateResponse(request, "index.html", context)


# =====================
# DASHBOARD STATUS (R-058 / Ruta 7.2)
# =====================

def _parse_df_output(stdout: str) -> dict[str, Any]:
    """Parsea la salida de 'df -h /' y devuelve porcentaje, usado y total."""
    for line in stdout.strip().splitlines():
        parts = line.split()
        if len(parts) >= 5 and "%" in parts[4]:
            try:
                percent = int(parts[4].replace("%", ""))
                return {
                    "available": True,
                    "percent": percent,
                    "used": parts[2],
                    "total": parts[1],
                    "free": parts[3],
                }
            except (ValueError, IndexError):
                pass
    return {"available": False}


def _backup_age_label(date_str: str) -> str:
    """Convierte una fecha 'YYYY-MM-DD HH:MM:SS' en 'hace X min/h/días'."""
    try:
        from datetime import datetime, timezone
        dt = datetime.strptime(date_str[:19], "%Y-%m-%d %H:%M:%S")
        # El historial no guarda timezone; asumimos UTC == local en el servidor
        now = datetime.now()
        diff = now - dt
        secs = int(diff.total_seconds())
        if secs < 60:
            return "ahora mismo"
        if secs < 3600:
            return f"hace {secs // 60} min"
        if secs < 86400:
            return f"hace {secs // 3600}h"
        return f"hace {secs // 86400} días"
    except Exception:
        return date_str[:16] if date_str else "—"


@app.get("/api/dashboard/status")
def dashboard_status(request: Request):
    """Endpoint JSON para el dashboard de estado (Ruta 7.2).
    Devuelve datos de backup, servicios, disco y alertas con timeout propio.
    Nunca lanza excepción: si un origen falla devuelve available=false."""
    if not is_authenticated(request):
        return JSONResponse({"error": "no autenticado"}, status_code=401)

    perms_context = get_common_context(request)

    # ── Alertas (local SQLite, siempre rápido) ──────────────────────────────
    try:
        stats = get_alert_stats()
        alert_block = {
            "available": True,
            "total": stats["alerts_total"],
            "ok": stats["alerts_ok"],
            "error": stats["alerts_error"],
            "last": stats["alerts_last"],
        }
    except Exception:
        alert_block = {"available": False}

    # ── Último backup (SSH historial) ───────────────────────────────────────
    backup_block: dict[str, Any] = {"available": False}
    if perms_context.get("can_backups"):
        try:
            history = cargar_historial_backups(limit=1)
            if history:
                last = history[0]
                status_raw = (last.get("status") or last.get("result") or "").upper()
                status_ok = status_raw in ("OK", "SUCCESS", "0", "")
                backup_block = {
                    "available": True,
                    "date": last.get("date") or last.get("start_time") or "",
                    "age_label": _backup_age_label(
                        last.get("date") or last.get("start_time") or ""
                    ),
                    "status": "OK" if status_ok else "ERROR",
                    "type": last.get("tipo_label") or last.get("type") or "—",
                    "db": last.get("db") or "—",
                }
        except Exception:
            backup_block = {"available": False}

    # ── Servicios (SSH) ─────────────────────────────────────────────────────
    services_block: dict[str, Any] = {"available": False}
    if perms_context.get("can_servicios"):
        try:
            result = ssh_run(SERVIDOR_SERVICIOS, SCRIPT_SERVICIOS, ["list"])
            lista: list[dict[str, str]] = []
            for linea in result.get("text", "").split("\n"):
                if "|" in linea:
                    nombre, estado = linea.split("|", 1)
                    lista.append({"nombre": nombre.strip(), "estado": estado.strip()})
            total = len(lista)
            active = sum(1 for s in lista if s["estado"] == "active")
            services_block = {
                "available": True,
                "total": total,
                "active": active,
                "inactive": total - active,
            }
        except Exception:
            services_block = {"available": False}

    # ── Disco (SSH df -h /) ─────────────────────────────────────────────────
    disk_block: dict[str, Any] = {"available": False}
    try:
        result_df = ssh_run(SERVIDOR_BACKUPS, "df", ["-h", "/"])
        if result_df.get("ok"):
            disk_block = _parse_df_output(result_df.get("stdout", "") or result_df.get("text", ""))
    except Exception:
        disk_block = {"available": False}

    return JSONResponse({
        "backup": backup_block,
        "services": services_block,
        "disk": disk_block,
        "alerts": alert_block,
    })


# =====================
# MONITORIZACIÓN (R-059 / Ruta 7.4)
# =====================

def _parse_loadavg(stdout: str) -> dict[str, Any]:
    """Parsea /proc/loadavg → load1, load5, load15."""
    try:
        parts = stdout.strip().split()
        return {
            "available": True,
            "load1":  float(parts[0]),
            "load5":  float(parts[1]),
            "load15": float(parts[2]),
            "procs":  parts[3] if len(parts) > 3 else "—",
        }
    except Exception:
        return {"available": False}


def _parse_meminfo(stdout: str) -> dict[str, Any]:
    """Parsea /proc/meminfo → total, usada, disponible y porcentaje."""
    try:
        data: dict[str, int] = {}
        for line in stdout.splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                nums = [int(t) for t in val.split() if t.isdigit()]
                if nums:
                    data[key.strip()] = nums[0]  # en kB
        total = data.get("MemTotal", 0)
        avail = data.get("MemAvailable", 0)
        used  = total - avail
        pct   = round(used * 100 / total) if total else 0

        def _kb_hr(kb: int) -> str:
            if kb >= 1024 * 1024:
                return f"{kb / 1024 / 1024:.1f} GB"
            return f"{kb // 1024} MB"

        return {
            "available": True,
            "percent":   pct,
            "total_hr":  _kb_hr(total),
            "used_hr":   _kb_hr(used),
            "avail_hr":  _kb_hr(avail),
        }
    except Exception:
        return {"available": False}


def _parse_uptime_secs(stdout: str) -> dict[str, Any]:
    """Parsea /proc/uptime → etiqueta human-readable."""
    try:
        secs = float(stdout.strip().split()[0])
        days  = int(secs // 86400)
        hours = int((secs % 86400) // 3600)
        mins  = int((secs % 3600) // 60)
        if days > 0:
            label = f"{days}d {hours}h"
        elif hours > 0:
            label = f"{hours}h {mins}m"
        else:
            label = f"{mins} min"
        return {"available": True, "seconds": secs, "label": label}
    except Exception:
        return {"available": False}


@app.get("/monitoreo")
def monitoreo_page(request: Request):
    """Página de monitorización del servidor (Ruta 7.4)."""
    if not is_authenticated(request):
        return RedirectResponse("/login")
    context = get_common_context(request)
    context["monitor_host"] = SERVIDOR_BACKUPS
    return templates.TemplateResponse(request, "monitoreo.html", context)


@app.get("/api/monitoreo/metrics")
def monitoreo_metrics(request: Request):
    """Endpoint JSON de métricas del servidor para la página de monitoreo."""
    if not is_authenticated(request):
        return JSONResponse({"error": "no autenticado"}, status_code=401)

    import time as _time

    # ── Carga del sistema (/proc/loadavg) ──────────────────────────────────
    load_block: dict[str, Any] = {"available": False}
    try:
        r = ssh_run(SERVIDOR_BACKUPS, "cat", ["/proc/loadavg"])
        if r.get("ok"):
            load_block = _parse_loadavg(r["stdout"])
    except Exception:
        pass

    # ── Memoria (/proc/meminfo) ─────────────────────────────────────────────
    mem_block: dict[str, Any] = {"available": False}
    try:
        r = ssh_run(SERVIDOR_BACKUPS, "cat", ["/proc/meminfo"])
        if r.get("ok"):
            mem_block = _parse_meminfo(r["stdout"])
    except Exception:
        pass

    # ── Disco (df -h /, ya allowlisted) ────────────────────────────────────
    disk_block: dict[str, Any] = {"available": False}
    try:
        r = ssh_run(SERVIDOR_BACKUPS, "df", ["-h", "/"])
        if r.get("ok"):
            disk_block = _parse_df_output(r["stdout"])
    except Exception:
        pass

    # ── Tiempo activo (/proc/uptime) ────────────────────────────────────────
    uptime_block: dict[str, Any] = {"available": False}
    try:
        r = ssh_run(SERVIDOR_BACKUPS, "cat", ["/proc/uptime"])
        if r.get("ok"):
            uptime_block = _parse_uptime_secs(r["stdout"])
    except Exception:
        pass

    return JSONResponse({
        "load":   load_block,
        "mem":    mem_block,
        "disk":   disk_block,
        "uptime": uptime_block,
        "ts":     _time.time(),
    })


# =====================
# NOTIFICACIONES PROACTIVAS (R-060 / Ruta 7.5)
# =====================

# Estado en memoria (se reinicia con el panel; suficiente para uso operacional)
_proactivo_estado: dict[str, Any] = {
    "enabled":    NOTIF_ENABLED,
    "last_run":   None,          # ISO-string última ejecución
    "runs_total": 0,
    "checks": {
        "disk":     {"last_value": None, "last_ok": None, "last_ts": None, "alerts_sent": 0},
        "backup":   {"last_value": None, "last_ok": None, "last_ts": None, "alerts_sent": 0},
        "services": {"last_value": None, "last_ok": None, "last_ts": None, "alerts_sent": 0,
                     "inactive_list": []},
    },
    "alert_log": [],   # lista de dicts {ts, tipo, canal, ok}
}

_last_alert_time: dict[str, float] = {}  # condition_key → timestamp último envío


def _can_alert(key: str) -> bool:
    return (_time_mod.time() - _last_alert_time.get(key, 0.0)) >= NOTIF_COOLDOWN


def _mark_alerted(key: str) -> None:
    _last_alert_time[key] = _time_mod.time()


# ── Email ──────────────────────────────────────────────────────────────────

def _send_email_alert(subject: str, body_html: str) -> bool:
    """Envía un email de alerta vía SMTP. Devuelve True si el envío tuvo éxito."""
    if not all([NOTIF_EMAIL_TO, NOTIF_SMTP_HOST, NOTIF_SMTP_USER, NOTIF_SMTP_PASS]):
        return False
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[Vigex Alert] {subject}"
        msg["From"]    = NOTIF_EMAIL_FROM or NOTIF_SMTP_USER
        msg["To"]      = NOTIF_EMAIL_TO
        msg.attach(MIMEText(body_html, "html", "utf-8"))

        with smtplib.SMTP(NOTIF_SMTP_HOST, NOTIF_SMTP_PORT, timeout=20) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(NOTIF_SMTP_USER, NOTIF_SMTP_PASS)
            smtp.sendmail(msg["From"], [NOTIF_EMAIL_TO], msg.as_string())
        return True
    except Exception:
        return False


def _send_email_bugreport(ticket_id: str, tipo: str, descripcion: str, usuario: str) -> bool:
    """Reenvía un reporte de bug/sugerencia/pregunta a soporte@vigex.es. R-083-fix-2
    Silencioso si SMTP no está configurado (no bloquea la respuesta al usuario).
    """
    if not all([NOTIF_SMTP_HOST, NOTIF_SMTP_USER, NOTIF_SMTP_PASS]):
        return False
    try:
        asunto = f"[Vigex Reporte #{ticket_id}] {tipo.capitalize()} · usuario: {usuario}"
        cuerpo_html = (
            f"<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'></head><body>"
            f"<div style='font-family:sans-serif;background:#f3f4f6;padding:24px;'>"
            f"<div style='background:#fff;border-radius:14px;padding:28px 32px;max-width:580px;margin:0 auto;'>"
            f"<h2 style='color:#4f46e5;margin:0 0 12px;'>Vigex — Reporte #{ticket_id}</h2>"
            f"<p style='margin:0 0 6px;'><strong>Tipo:</strong> {tipo}</p>"
            f"<p style='margin:0 0 6px;'><strong>Enviado por:</strong> {usuario}</p>"
            f"<hr style='border:none;border-top:1px solid #e5e7eb;margin:14px 0;'>"
            f"<pre style='background:#f8fafc;padding:14px;border-radius:8px;"
            f"font-size:13px;white-space:pre-wrap;color:#374151;'>{descripcion}</pre>"
            f"</div></div></body></html>"
        )
        msg = MIMEMultipart("alternative")
        msg["Subject"] = asunto
        msg["From"]    = NOTIF_EMAIL_FROM or NOTIF_SMTP_USER
        msg["To"]      = "soporte@vigex.es"
        msg.attach(MIMEText(cuerpo_html, "html", "utf-8"))
        with smtplib.SMTP(NOTIF_SMTP_HOST, NOTIF_SMTP_PORT, timeout=20) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(NOTIF_SMTP_USER, NOTIF_SMTP_PASS)
            smtp.sendmail(msg["From"], ["soporte@vigex.es"], msg.as_string())
        return True
    except Exception:
        return False


def _html_email(title: str, body: str) -> str:
    """Genera el HTML base para emails de alerta Vigex."""
    return f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8">
<style>
  body {{ font-family: -apple-system, sans-serif; background:#f3f4f6; margin:0; padding:24px; }}
  .card {{ background:#fff; border-radius:14px; padding:28px 32px; max-width:540px; margin:0 auto; }}
  h1 {{ color:#1e1b4b; font-size:18px; margin:0 0 16px; }}
  p {{ color:#374151; font-size:14px; line-height:1.6; }}
  .badge {{ display:inline-block; padding:4px 12px; border-radius:99px; font-size:12px; font-weight:700; }}
  .badge.error {{ background:#fee2e2; color:#b91c1c; }}
  .badge.warn {{ background:#fef3c7; color:#b45309; }}
  .footer {{ color:#9ca3af; font-size:11px; margin-top:20px; border-top:1px solid #e5e7eb; padding-top:12px; }}
</style>
</head>
<body><div class="card">
  <h1>🚨 {title}</h1>
  {body}
  <div class="footer">Vigex · Notificación automática · No responder a este correo.</div>
</div></body></html>"""


# ── Envío combinado Telegram + Email ────────────────────────────────────────

def _send_proactive_alert(tipo: str, tg_text: str, email_subject: str, email_body: str) -> None:
    """Envía alerta por Telegram (si hay destinatario) y por email (si está config)."""
    log_entry: dict[str, Any] = {
        "ts":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tipo": tipo,
        "tg":   False,
        "mail": False,
    }
    # Telegram
    default = get_default_recipient("telegram")
    if default:
        r = send_telegram_message(tg_text, default["destination"])
        log_entry["tg"] = bool(r.get("ok"))

    # Email
    if NOTIF_EMAIL_TO and NOTIF_SMTP_HOST:
        log_entry["mail"] = _send_email_alert(email_subject, _html_email(email_subject, email_body))

    _proactivo_estado["alert_log"].append(log_entry)
    if len(_proactivo_estado["alert_log"]) > 30:
        _proactivo_estado["alert_log"] = _proactivo_estado["alert_log"][-30:]


# ── Comprobaciones individuales ─────────────────────────────────────────────

def _check_disk_proactive() -> None:
    check = _proactivo_estado["checks"]["disk"]
    try:
        r = ssh_run(SERVIDOR_BACKUPS, "df", ["-h", "/"])
        if not r.get("ok"):
            check["last_ok"] = None
            return
        info = _parse_df_output(r["stdout"])
        if not info.get("available"):
            check["last_ok"] = None
            return
        pct = info.get("percent", 0)
        check["last_value"] = f"{pct}% ({info.get('used','?')} de {info.get('total','?')})"
        check["last_ts"] = datetime.now().isoformat()
        ok = pct < NOTIF_DISK_THRESHOLD
        check["last_ok"] = ok
        if not ok and _can_alert("disk"):
            _mark_alerted("disk")
            check["alerts_sent"] += 1
            tg = (f"🚨 <b>Vigex — Disco casi lleno</b>\n\n"
                  f"El disco del servidor está al <b>{pct}%</b> de capacidad.\n"
                  f"Umbral configurado: {NOTIF_DISK_THRESHOLD}%.\n\n"
                  f"<i>Elimina archivos o amplía el espacio antes de que se llene.</i>")
            mail_body = (f"<p>El disco del servidor ha superado el umbral configurado.</p>"
                         f"<p><span class='badge error'>Disco al {pct}%</span></p>"
                         f"<p>Umbral: {NOTIF_DISK_THRESHOLD}% &nbsp;|&nbsp; "
                         f"Usado: {info.get('used','?')} de {info.get('total','?')}</p>"
                         f"<p>Revisa el servidor y libera espacio cuanto antes.</p>")
            _send_proactive_alert("disco", tg, f"Disco casi lleno ({pct}%)", mail_body)
    except Exception:
        check["last_ok"] = None


def _check_backup_proactive() -> None:
    check = _proactivo_estado["checks"]["backup"]
    try:
        history = cargar_historial_backups(limit=1)
        if not history:
            check["last_ok"] = None
            return
        last = history[0]
        status_raw = (last.get("status") or last.get("result") or "").upper()
        ok = status_raw in ("OK", "SUCCESS", "0", "")
        date_str = last.get("date") or last.get("start_time") or "—"
        check["last_value"] = f"{status_raw or 'OK'} · {date_str[:16]}"
        check["last_ts"]    = datetime.now().isoformat()
        check["last_ok"]    = ok
        if not ok and _can_alert("backup"):
            _mark_alerted("backup")
            check["alerts_sent"] += 1
            tipo_label = last.get("tipo_label") or last.get("type") or "—"
            tg = (f"🚨 <b>Vigex — Copia de seguridad fallida</b>\n\n"
                  f"La última copia registrada ha terminado con error.\n"
                  f"Tipo: <b>{tipo_label}</b> &nbsp;|&nbsp; Fecha: {date_str[:16]}\n\n"
                  f"<i>Revisa el servidor de backups y comprueba el historial.</i>")
            mail_body = (f"<p>La última copia de seguridad ha terminado con error.</p>"
                         f"<p><span class='badge error'>Estado: {status_raw}</span></p>"
                         f"<p>Tipo: {tipo_label} &nbsp;|&nbsp; Fecha: {date_str[:16]}</p>"
                         f"<p>Accede al panel de Vigex y revisa el historial de copias.</p>")
            _send_proactive_alert("backup", tg, "Copia de seguridad fallida", mail_body)
    except Exception:
        check["last_ok"] = None


def _check_services_proactive() -> None:
    check = _proactivo_estado["checks"]["services"]
    try:
        result = ssh_run(SERVIDOR_SERVICIOS, SCRIPT_SERVICIOS, ["list"])
        lista: list[dict[str, str]] = []
        for linea in result.get("text", "").split("\n"):
            if "|" in linea:
                nombre, estado = linea.split("|", 1)
                lista.append({"nombre": nombre.strip(), "estado": estado.strip()})
        if not lista:
            check["last_ok"] = None
            return
        inactive = [s["nombre"] for s in lista if s["estado"] != "active"]
        ok = len(inactive) == 0
        check["last_value"]     = f"{len(lista) - len(inactive)}/{len(lista)} activos"
        check["last_ts"]        = datetime.now().isoformat()
        check["last_ok"]        = ok
        check["inactive_list"]  = inactive
        if not ok and _can_alert("services"):
            _mark_alerted("services")
            check["alerts_sent"] += 1
            inactive_str = ", ".join(inactive)
            tg = (f"🚨 <b>Vigex — Servicio(s) caído(s)</b>\n\n"
                  f"Se ha detectado {'un servicio inactivo' if len(inactive)==1 else f'{len(inactive)} servicios inactivos'}:\n"
                  f"<b>{inactive_str}</b>\n\n"
                  f"<i>Revisa el servidor y reinicia el servicio si es necesario.</i>")
            mail_body = (f"<p>Se ha detectado {'un servicio inactivo' if len(inactive)==1 else f'{len(inactive)} servicios inactivos'}.</p>"
                         f"<p><span class='badge error'>Inactivos: {inactive_str}</span></p>"
                         f"<p>Accede al panel &gt; Servicios y reinicia los servicios afectados.</p>")
            _send_proactive_alert("servicios", tg,
                                  f"Servicio caído: {inactive_str}", mail_body)
    except Exception:
        check["last_ok"] = None


def _run_proactive_checks() -> None:
    """Ejecuta las tres comprobaciones y actualiza el estado en memoria."""
    _proactivo_estado["last_run"]   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _proactivo_estado["runs_total"] += 1
    _check_disk_proactive()
    _check_backup_proactive()
    _check_services_proactive()


def _proactivo_worker() -> None:
    """Hilo daemon de comprobaciones periódicas (se inicia solo si NOTIF_ENABLED=true)."""
    _time_mod.sleep(90)           # espera inicial para no sobrecargar el arranque
    while True:
        try:
            _run_proactive_checks()
        except Exception:
            pass
        _time_mod.sleep(NOTIF_CHECK_INTERVAL)


# ── Rutas ────────────────────────────────────────────────────────────────────

@app.get("/alertas/proactivas")
def alertas_proactivas_page(request: Request):
    """Página de configuración y estado de notificaciones proactivas (Ruta 7.5)."""
    if not is_admin(request):
        return permission_redirect()
    context = get_common_context(request)
    context["estado"]            = _proactivo_estado
    context["notif_enabled"]     = NOTIF_ENABLED
    context["notif_email_to"]    = NOTIF_EMAIL_TO
    context["notif_smtp_host"]   = NOTIF_SMTP_HOST
    context["notif_threshold"]   = NOTIF_DISK_THRESHOLD
    context["notif_interval_min"] = NOTIF_CHECK_INTERVAL // 60
    context["notif_cooldown_h"]  = NOTIF_COOLDOWN // 3600
    context["has_email"]         = bool(NOTIF_EMAIL_TO and NOTIF_SMTP_HOST)
    context["has_telegram"]      = bool(get_default_recipient("telegram"))
    return templates.TemplateResponse(request, "alertas_proactivas.html", context)


@app.post("/alertas/proactivas/check")
def alertas_proactivas_check(request: Request):
    """Dispara una comprobación inmediata (solo admins)."""
    if not is_admin(request):
        return JSONResponse({"error": "sin permiso"}, status_code=403)
    try:
        _run_proactive_checks()
        return JSONResponse({
            "ok": True,
            "last_run":  _proactivo_estado["last_run"],
            "checks": {
                k: {
                    "last_value": v["last_value"],
                    "last_ok":    v["last_ok"],
                }
                for k, v in _proactivo_estado["checks"].items()
            },
        })
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)


# =====================
# ADMIN USUARIOS
# =====================
@app.get("/admin/usuarios")
def admin_users_page(request: Request):
    if not is_admin(request):
        return permission_redirect()

    context = get_common_context(request)
    context["ok"] = request.query_params.get("ok")
    context["msg"] = request.query_params.get("msg")
    context["users"] = load_users()
    context["available_permissions"] = AVAILABLE_PERMISSIONS
    context["users_count"] = len(context["users"]) + 1
    return templates.TemplateResponse(request, "admin_users.html", context)


@app.get("/admin/login-logs")
def admin_login_logs_page(request: Request):
    if not is_admin(request):
        return permission_redirect()

    auth_logs = load_auth_logs(limit=200)

    context = get_common_context(request)
    context["auth_logs"] = auth_logs
    context["auth_logs_total"] = len(auth_logs)
    context["auth_logs_ok"] = sum(1 for e in auth_logs if e.get("resultado") == "OK")
    context["auth_logs_error"] = sum(1 for e in auth_logs if e.get("resultado") != "OK")
    context["auth_logs_login"] = sum(1 for e in auth_logs if e.get("accion") == "LOGIN")
    context["auth_logs_logout"] = sum(1 for e in auth_logs if e.get("accion") == "LOGOUT")
    context["auth_logs_last"] = auth_logs[0].get("fecha") if auth_logs else None
    return templates.TemplateResponse(request, "admin_login_logs.html", context)


@app.post("/admin/usuarios")
def create_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    permissions: list[str] = Form([]),
):
    if not is_admin(request):
        return permission_redirect()

    username = (username or "").strip()
    password = (password or "").strip()
    permissions = normalize_permissions(permissions)

    if " " in username:
        return RedirectResponse(
            url="/admin/usuarios?ok=0&msg=El+usuario+no+puede+contener+espacios",
            status_code=303,
        )

    if not username or not password:
        return RedirectResponse(
            url="/admin/usuarios?ok=0&msg=Usuario+y+contraseña+son+obligatorios",
            status_code=303,
        )

    if username == ADMIN_USER:
        return RedirectResponse(
            url="/admin/usuarios?ok=0&msg=No+puedes+crear+otro+usuario+con+el+nombre+del+admin",
            status_code=303,
        )

    if find_user(username):
        return RedirectResponse(
            url="/admin/usuarios?ok=0&msg=Ese+usuario+ya+existe",
            status_code=303,
        )

    users = load_users()
    users.append(
        {
            "username": username,
            "password_hash": hash_password(password),
            "permissions": permissions,
        }
    )
    save_users(users)

    return RedirectResponse(
        url="/admin/usuarios?ok=1&msg=Usuario+creado+correctamente",
        status_code=303,
    )


@app.post("/admin/usuarios/delete")
def delete_user(
    request: Request,
    username: str = Form(...),
):
    if not is_admin(request):
        return permission_redirect()

    username = (username or "").strip()

    if username == ADMIN_USER:
        return RedirectResponse(
            url="/admin/usuarios?ok=0&msg=El+usuario+admin+no+se+puede+eliminar",
            status_code=303,
        )

    users = load_users()
    filtered = [u for u in users if u["username"] != username]

    if len(filtered) == len(users):
        return RedirectResponse(
            url="/admin/usuarios?ok=0&msg=Usuario+no+encontrado",
            status_code=303,
        )

    save_users(filtered)
    return RedirectResponse(
        url="/admin/usuarios?ok=1&msg=Usuario+eliminado+correctamente",
        status_code=303,
    )



# =====================
# TERMINAL WEB
# =====================
def get_terminal_machines() -> dict[str, dict[str, str]]:
    return {
        "main": {
            "key": "main",
            "label": "Máquina Main",
            "description": "Servidor donde se ejecuta el panel Vigex y la API principal.",
            "host": TERMINAL_MAIN_HOST,
            "mode": "local",
            "icon": "fa-computer",
        },
        "backup": {
            "key": "backup",
            "label": "Máquina Backup",
            "description": "Servidor encargado de las copias de seguridad.",
            "host": SERVIDOR_BACKUPS,
            "mode": "ssh",
            "icon": "fa-database",
        },
        "database": {
            "key": "database",
            "label": "Máquina Database",
            "description": "Servidor de base de datos y almacenamiento de logs.",
            "host": TERMINAL_DATABASE_HOST,
            "mode": "ssh",
            "icon": "fa-server",
        },
    }


def get_terminal_machine(machine_key: str) -> dict[str, str] | None:
    machine_key = (machine_key or "").strip().lower()
    return get_terminal_machines().get(machine_key)


def run_local_terminal_command(command: str) -> dict[str, Any]:
    started = datetime.now()
    try:
        res = subprocess.run(
            ["/bin/bash", "-lc", command],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            timeout=TERMINAL_TIMEOUT,
        )
        finished = datetime.now()
        out = res.stdout or ""
        err = res.stderr or ""
        return {
            "ok": res.returncode == 0,
            "code": res.returncode,
            "stdout": out,
            "stderr": err,
            "text": out if res.returncode == 0 else (err or out),
            "started_at": started.strftime("%Y-%m-%d %H:%M:%S"),
            "finished_at": finished.strftime("%Y-%m-%d %H:%M:%S"),
        }
    except subprocess.TimeoutExpired as e:
        finished = datetime.now()
        out = e.stdout or ""
        err = e.stderr or ""
        return {
            "ok": False,
            "code": 124,
            "stdout": out if isinstance(out, str) else out.decode("utf-8", errors="replace"),
            "stderr": err if isinstance(err, str) else err.decode("utf-8", errors="replace"),
            "text": f"ERROR: el comando superó el tiempo máximo de {TERMINAL_TIMEOUT} segundos.",
            "started_at": started.strftime("%Y-%m-%d %H:%M:%S"),
            "finished_at": finished.strftime("%Y-%m-%d %H:%M:%S"),
        }
    except Exception as e:
        finished = datetime.now()
        return {
            "ok": False,
            "code": 1,
            "stdout": "",
            "stderr": str(e),
            "text": f"ERROR: {e}",
            "started_at": started.strftime("%Y-%m-%d %H:%M:%S"),
            "finished_at": finished.strftime("%Y-%m-%d %H:%M:%S"),
        }


def run_ssh_terminal_command(host: str, command: str) -> dict[str, Any]:
    started = datetime.now()
    cmd = [
        "ssh",
        "-i", SSH_KEY_PATH,
        "-o", "BatchMode=yes",
        "-o", "StrictHostKeyChecking=yes",
        "-o", f"UserKnownHostsFile={SSH_KNOWN_HOSTS_PATH}",
        f"{USUARIO}@{host}",
        "bash",
        "-s",
    ]

    try:
        res = subprocess.run(
            cmd,
            input=command,
            capture_output=True,
            text=True,
            timeout=TERMINAL_TIMEOUT,
        )
        finished = datetime.now()
        out = res.stdout or ""
        err = res.stderr or ""
        return {
            "ok": res.returncode == 0,
            "code": res.returncode,
            "stdout": out,
            "stderr": err,
            "text": out if res.returncode == 0 else (err or out),
            "started_at": started.strftime("%Y-%m-%d %H:%M:%S"),
            "finished_at": finished.strftime("%Y-%m-%d %H:%M:%S"),
        }
    except subprocess.TimeoutExpired as e:
        finished = datetime.now()
        out = e.stdout or ""
        err = e.stderr or ""
        return {
            "ok": False,
            "code": 124,
            "stdout": out if isinstance(out, str) else out.decode("utf-8", errors="replace"),
            "stderr": err if isinstance(err, str) else err.decode("utf-8", errors="replace"),
            "text": f"ERROR: el comando superó el tiempo máximo de {TERMINAL_TIMEOUT} segundos.",
            "started_at": started.strftime("%Y-%m-%d %H:%M:%S"),
            "finished_at": finished.strftime("%Y-%m-%d %H:%M:%S"),
        }
    except Exception as e:
        finished = datetime.now()
        return {
            "ok": False,
            "code": 1,
            "stdout": "",
            "stderr": str(e),
            "text": f"ERROR: {e}",
            "started_at": started.strftime("%Y-%m-%d %H:%M:%S"),
            "finished_at": finished.strftime("%Y-%m-%d %H:%M:%S"),
        }


@app.get("/terminal")
def terminal_page(request: Request):
    if not has_permission(request, "terminal"):
        return permission_redirect()

    machines = get_terminal_machines()
    context = get_common_context(request)
    context["machines"] = machines
    context["selected_machine"] = None
    context["selected_key"] = None
    context["terminal_timeout"] = TERMINAL_TIMEOUT
    return templates.TemplateResponse(request, "terminal.html", context)


@app.get("/terminal/{machine_key}")
def terminal_machine_page(request: Request, machine_key: str):
    if not has_permission(request, "terminal"):
        return permission_redirect()

    machine = get_terminal_machine(machine_key)
    if not machine:
        return RedirectResponse(
            url="/terminal?msg=Maquina+no+valida",
            status_code=303,
        )

    machines = get_terminal_machines()
    context = get_common_context(request)
    context["machines"] = machines
    context["selected_machine"] = machine
    context["selected_key"] = machine_key
    context["terminal_timeout"] = TERMINAL_TIMEOUT
    return templates.TemplateResponse(request, "terminal.html", context)


@app.post("/api/terminal/run")
def terminal_run_command(
    request: Request,
    machine: str = Form(...),
    command: str = Form(...),
):
    if not has_permission(request, "terminal"):
        return JSONResponse(
            {"ok": False, "error": "No tienes permisos para usar la terminal."},
            status_code=403,
        )

    terminal_machine = get_terminal_machine(machine)
    if not terminal_machine:
        return JSONResponse(
            {"ok": False, "error": "Máquina no válida."},
            status_code=400,
        )

    command = (command or "").strip()
    if not command:
        return JSONResponse(
            {"ok": False, "error": "El comando no puede estar vacío."},
            status_code=400,
        )

    if len(command) > TERMINAL_MAX_COMMAND_LENGTH:
        return JSONResponse(
            {"ok": False, "error": f"El comando supera el límite de {TERMINAL_MAX_COMMAND_LENGTH} caracteres."},
            status_code=400,
        )

    if terminal_machine["mode"] == "local":
        result = run_local_terminal_command(command)
    else:
        result = run_ssh_terminal_command(terminal_machine["host"], command)

    usuario = request.session.get("user", "anon")
    ip = request.client.host if request.client else None
    detalle = (
        f"Máquina: {terminal_machine['label']} ({terminal_machine['host']}) | "
        f"Comando: {command} | Código: {result['code']}"
    )
    log_event(
        tipo="terminal",
        resultado="OK" if result["ok"] else "ERROR",
        usuario=usuario,
        ip_origen=ip,
        recurso=f"POST /api/terminal/run/{terminal_machine['key']}",
        detalle=detalle,
    )

    return {
        "ok": result["ok"],
        "code": result["code"],
        "machine": terminal_machine,
        "command": command,
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "text": result["text"],
        "started_at": result["started_at"],
        "finished_at": result["finished_at"],
    }


# =====================
# LOGS
# =====================
@app.get("/logs")
def ver_logs(request: Request):
    if not has_permission(request, "logs"):
        return permission_redirect()

    try:
        conn = pymysql.connect(
            host=LOGS_DB_HOST,
            user=LOGS_DB_USER,
            password=LOGS_DB_PASS,
            database=LOGS_DB_NAME,
            autocommit=True,
            connect_timeout=2,
            cursorclass=pymysql.cursors.DictCursor,
        )
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, fecha, origen, tipo, usuario, ip_origen, recurso, resultado, detalle
                FROM eventos
                ORDER BY fecha DESC
                LIMIT 100
                """
            )
            eventos = cur.fetchall()
        conn.close()
    except Exception as e:
        eventos = []
        print(f"Error cargando eventos: {e}")

    context = get_common_context(request)
    context["cacti_url"] = CACTI_URL
    context["eventos"] = eventos
    context["logs_total"] = len(eventos)
    context["logs_ok"] = sum(1 for e in eventos if e.get("resultado") == "OK")
    context["logs_error"] = sum(1 for e in eventos if e.get("resultado") != "OK")
    context["logs_last"] = eventos[0].get("fecha") if eventos else None
    return templates.TemplateResponse(request, "logs.html", context)



# =====================
# ALERTAS
# =====================
@app.get("/alertas")
def alertas(request: Request):
    if not has_permission(request, "alertas"):
        return permission_redirect()

    ensure_default_recipient()

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM alert_channels ORDER BY id")
    channels = [dict(row) for row in cur.fetchall()]

    cur.execute("SELECT * FROM alert_rules ORDER BY event_code")
    rules = [dict(row) for row in cur.fetchall()]

    cur.execute("SELECT * FROM alert_recipients ORDER BY is_default DESC, id ASC")
    recipients = [dict(row) for row in cur.fetchall()]

    cur.execute(
        """
        SELECT d.delivered_at, e.event_code, e.title, d.channel_code, d.recipient_name, d.destination, d.status
        FROM alert_deliveries d
        JOIN alert_events e ON e.id = d.event_id
        ORDER BY d.id DESC
        LIMIT 20
        """
    )
    deliveries = [dict(row) for row in cur.fetchall()]
    conn.close()

    detected_chats = request.session.get("telegram_detected_chats", [])

    tg = next((c for c in channels if c.get("code") == "telegram"), None)

    context = get_common_context(request)
    context["channels"] = channels
    context["tg"] = tg
    context["rules"] = rules
    context["recipients"] = recipients
    context["detected_chats"] = detected_chats
    context["deliveries"] = deliveries
    context["ok"] = request.query_params.get("ok")
    context["msg"] = request.query_params.get("msg")
    context["manual_url"] = "/static/docs/guia_alertas_telegram.pdf"
    context["bot_link"] = f"https://t.me/{TELEGRAM_BOT_USERNAME}" if TELEGRAM_BOT_USERNAME else None
    context.update(get_alert_stats())

    return templates.TemplateResponse(request, "alertas.html", context)


@app.post("/alertas/test")
def alertas_test(request: Request):
    if not has_permission(request, "alertas"):
        return RedirectResponse(
            url="/alertas?ok=0&msg=No+tienes+permisos",
            status_code=303,
        )

    default_recipient = get_default_recipient("telegram")
    if not default_recipient:
        return RedirectResponse(
            url="/alertas?ok=0&msg=No+hay+destino+por+defecto.+Añade+un+destinatario+primero",
            status_code=303,
        )

    text = (
        "<b>Vigex</b>\n"
        "Prueba de alerta Telegram desde el panel.\n"
        f"Usuario: {request.session.get('user', 'anon')}\n"
        f"Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Destino: {default_recipient['name']}"
    )

    result = send_telegram_message(text, default_recipient["destination"])
    if result.get("ok"):
        msg = "Prueba+de+Telegram+enviada+correctamente"
    else:
        msg = quote(str(result.get("text") or result.get("error") or "Error desconocido"))

    return RedirectResponse(
        url=f"/alertas?ok={1 if result.get('ok') else 0}&msg={msg}",
        status_code=303,
    )


@app.post("/alertas/detect")
def alertas_detect(request: Request):
    if not has_permission(request, "alertas"):
        return permission_redirect()

    try:
        detected = fetch_recent_telegram_chats()
        request.session["telegram_detected_chats"] = detected
        if detected:
            return RedirectResponse(
                url=f"/alertas?ok=1&msg={quote(f'Se detectaron {len(detected)} chats recientes')}",
                status_code=303,
            )
        return RedirectResponse(
            url="/alertas?ok=0&msg=No+se+detectaron+chats.+Haz+/start+y+vuelve+a+probar",
            status_code=303,
        )
    except Exception as e:
        return RedirectResponse(
            url=f"/alertas?ok=0&msg={quote(str(e))}",
            status_code=303,
        )


@app.post("/alertas/recipient/add")
def alertas_recipient_add(
    request: Request,
    company: str = Form(""),
    name: str = Form(...),
    kind: str = Form(...),
    destination: str = Form(...),
    username: str = Form(""),
):
    if not has_permission(request, "alertas"):
        return permission_redirect()

    kind = (kind or "user").strip()
    if kind not in {"user", "group"}:
        return RedirectResponse(
            url="/alertas?ok=0&msg=Tipo+de+destinatario+no+válido",
            status_code=303,
        )

    destination = (destination or "").strip()
    name = (name or "").strip()
    username = (username or "").strip()
    company = (company or "").strip()

    if not destination or not name:
        return RedirectResponse(
            url="/alertas?ok=0&msg=Nombre+y+chat_id+son+obligatorios",
            status_code=303,
        )

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) AS total FROM alert_recipients WHERE destination = ? AND channel_code = 'telegram'",
        (destination,),
    )
    exists = int(cur.fetchone()["total"])
    if exists:
        conn.close()
        return RedirectResponse(
            url="/alertas?ok=0&msg=Ese+chat_id+ya+está+guardado",
            status_code=303,
        )

    cur.execute("SELECT COUNT(*) AS total FROM alert_recipients WHERE channel_code = 'telegram'",)
    total_before = int(cur.fetchone()["total"])
    is_default = 1 if total_before == 0 else 0

    cur.execute(
        """
        INSERT INTO alert_recipients(channel_code, company, name, username, kind, destination, is_enabled, is_default)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        ("telegram", company, name, username, kind, destination, 1, is_default),
    )
    conn.commit()
    conn.close()
    ensure_default_recipient()

    return RedirectResponse(
        url="/alertas?ok=1&msg=Destinatario+guardado+correctamente",
        status_code=303,
    )


@app.post("/alertas/recipient/add-detected")
def alertas_recipient_add_detected(
    request: Request,
    username: str = Form(""),
    chat_id: str = Form(...),
    kind: str = Form("user"),
):
    display_name = (username or "").strip() or "(sin username)"
    company = "Detectado Telegram"
    return alertas_recipient_add(
        request=request,
        company=company,
        name=display_name,
        kind=kind,
        destination=chat_id,
        username=username,
    )


@app.post("/alertas/recipient/toggle")
def alertas_recipient_toggle(request: Request, recipient_id: int = Form(...)):
    if not has_permission(request, "alertas"):
        return permission_redirect()

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE alert_recipients
        SET is_enabled = CASE WHEN is_enabled = 1 THEN 0 ELSE 1 END
        WHERE id = ?
        """,
        (recipient_id,),
    )

    cur.execute("SELECT is_enabled, is_default FROM alert_recipients WHERE id = ?", (recipient_id,))
    row = cur.fetchone()
    conn.commit()
    conn.close()

    if row and int(row["is_enabled"]) == 0 and int(row["is_default"]) == 1:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE alert_recipients SET is_default = 0 WHERE id = ?", (recipient_id,))
        conn.commit()
        conn.close()

    ensure_default_recipient()
    return RedirectResponse(
        url="/alertas?ok=1&msg=Destinatario+actualizado",
        status_code=303,
    )


@app.post("/alertas/recipient/delete")
def alertas_recipient_delete(request: Request, recipient_id: int = Form(...)):
    if not has_permission(request, "alertas"):
        return permission_redirect()

    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM alert_recipients WHERE id = ?", (recipient_id,))
    conn.commit()
    conn.close()

    ensure_default_recipient()
    return RedirectResponse(
        url="/alertas?ok=1&msg=Destinatario+eliminado",
        status_code=303,
    )


@app.post("/alertas/recipient/default")
def alertas_recipient_default(request: Request, recipient_id: int = Form(...)):
    if not has_permission(request, "alertas"):
        return permission_redirect()

    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE alert_recipients SET is_default = 0 WHERE channel_code = 'telegram'")
    cur.execute("UPDATE alert_recipients SET is_default = 1, is_enabled = 1 WHERE id = ?", (recipient_id,))
    conn.commit()
    conn.close()

    sync_channel_destination()
    return RedirectResponse(
        url="/alertas?ok=1&msg=Destino+por+defecto+actualizado",
        status_code=303,
    )


@app.post("/alertas/rule/toggle")
def alertas_rule_toggle(request: Request, rule_id: int = Form(...)):
    if not has_permission(request, "alertas"):
        return permission_redirect()

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE alert_rules
        SET is_enabled = CASE WHEN is_enabled = 1 THEN 0 ELSE 1 END
        WHERE id = ?
        """,
        (rule_id,),
    )
    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/alertas?ok=1&msg=Regla+actualizada",
        status_code=303,
    )


@app.post("/alertas/channel/toggle")
def alertas_channel_toggle(request: Request, channel_code: str = Form(...)):
    if not has_permission(request, "alertas"):
        return permission_redirect()

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE alert_channels
        SET is_enabled = CASE WHEN is_enabled = 1 THEN 0 ELSE 1 END
        WHERE code = ?
        """,
        (channel_code,),
    )
    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/alertas?ok=1&msg=Canal+actualizado",
        status_code=303,
    )


# =====================
# SERVICIOS
# =====================
@app.get("/servicios")
def ver_servicios(request: Request):
    if not has_permission(request, "servicios"):
        return permission_redirect()

    result = ssh_run(SERVIDOR_SERVICIOS, SCRIPT_SERVICIOS, ["list"])
    salida = result["text"]

    ok = request.query_params.get("ok")
    msg = request.query_params.get("msg")

    if salida.startswith("ERROR") and not msg:
        ok = "0"
        msg = salida

    lista_servicios: list[dict[str, str]] = []
    for linea in salida.split("\n"):
        if "|" in linea:
            nombre, estado = linea.split("|", 1)
            lista_servicios.append(
                {
                    "nombre": nombre.strip(),
                    "estado": estado.strip(),
                }
            )

    context = get_common_context(request)
    context["servicios"] = lista_servicios
    context["ok"] = ok
    context["msg"] = msg
    context["services_total"] = len(lista_servicios)
    context["services_active"] = sum(1 for s in lista_servicios if s["estado"] == "active")
    context["services_inactive"] = len(lista_servicios) - context["services_active"]
    return templates.TemplateResponse(request, "servicios.html", context)


@app.post("/servicios/accion")
def accion_servicio(
    request: Request,
    service: str = Form(...),
    action: str = Form(...),
):
    if not has_permission(request, "servicios"):
        return permission_redirect()

    action = (action or "").strip().lower()
    service = (service or "").strip()

    if action not in ("start", "stop", "restart"):
        return RedirectResponse(
            url="/servicios?ok=0&msg=Accion+no+valida",
            status_code=303,
        )

    if not es_token_simple(service, "@:._-"):
        return RedirectResponse(
            url="/servicios?ok=0&msg=Nombre+de+servicio+no+valido",
            status_code=303,
        )

    result = ssh_run(SERVIDOR_SERVICIOS, SCRIPT_SERVICIOS, [action, service])
    ok = 1 if result["ok"] else 0

    if result["ok"]:
        emit_alert(
            "service.ok",
            "info",
            "Acción de servicio completada",
            (
                "<b>Servicio OK</b>\n"
                f"Acción: {action}\n"
                f"Servicio: {service}\n"
                f"Servidor: {SERVIDOR_SERVICIOS}"
            ),
            "services",
        )
    else:
        emit_alert(
            "service.error",
            "critical",
            "Error en servicio",
            (
                "<b>Servicio ERROR</b>\n"
                f"Acción: {action}\n"
                f"Servicio: {service}\n"
                f"Servidor: {SERVIDOR_SERVICIOS}\n"
                f"Detalle: {result['text']}"
            ),
            "services",
        )

    return RedirectResponse(
        url=f"/servicios?ok={ok}&msg={quote(result['text'])}",
        status_code=303,
    )


# =====================
# BACKUPS
# =====================
@app.get("/backups")
def backups(request: Request):
    if not has_permission(request, "backups"):
        return permission_redirect()

    ok = request.query_params.get("ok")
    msg = request.query_params.get("msg")

    context = get_common_context(request)
    context["ok"] = ok
    context["msg"] = msg
    context["cacti_url"] = CACTI_URL
    context["backup_history"] = cargar_historial_backups()
    context["backup_automations"] = cargar_automatizaciones_backups()
    context["delete_plan"] = None
    context["restore_plan"] = None

    return templates.TemplateResponse(request, "backups.html", context)


@app.post("/api/backups/{tipo}")
def ejecutar_backup(request: Request, tipo: str):
    if not has_permission(request, "backups"):
        return JSONResponse(
            {"ok": False, "error": "No tienes permisos"},
            status_code=403,
        )

    if tipo not in ["full", "incremental", "differential"]:
        return JSONResponse(
            {"ok": False, "error": "Tipo de backup no válido"},
            status_code=400,
        )

    result = ssh_run(SERVIDOR_BACKUPS, SCRIPT_BACKUPS, [tipo])
    ok = result["ok"]

    if ok:
        emit_alert(
            "backup.ok",
            "info",
            "Backup completado",
            (
                "<b>Backup OK</b>\n"
                f"Tipo: {tipo}\n"
                f"Servidor: {SERVIDOR_BACKUPS}"
            ),
            "backups",
        )
    else:
        emit_alert(
            "backup.error",
            "critical",
            "Error en backup",
            (
                "<b>Backup ERROR</b>\n"
                f"Tipo: {tipo}\n"
                f"Servidor: {SERVIDOR_BACKUPS}\n"
                f"Detalle: {result['text']}"
            ),
            "backups",
        )

    return {
        "ok": ok,
        "tipo": tipo,
        "resultado": result["text"],
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/api/test-backups")
def test_backups(request: Request):
    if not has_permission(request, "backups"):
        return JSONResponse(
            {"ok": False, "error": "No tienes permisos"},
            status_code=403,
        )

    result = ssh_run(SERVIDOR_BACKUPS, "/bin/bash", ["-lc", "hostname && date"])
    return {
        "ok": result["ok"],
        "resultado": result["text"],
    }


def is_ok(output: str) -> bool:
    if not output:
        return False

    o = output.lower()

    if "error" in o:
        return False

    return (
        o.startswith("ok")
        or " ok:" in o
        or "\nok:" in o
        or "ok: backup" in o
        or "ok: restauración" in o
        or "ok: restauracion" in o
        or "restauración completada" in o
        or "restauracion completada" in o
        or "backup full creado" in o
        or "backup incremental creado" in o
        or "backup differential creado" in o
        or "backup diferencial creado" in o
        or "backups eliminados correctamente" in o
        or "creado en" in o
        or "backup completed" in o
        or "success" in o
    )


@app.post("/backups/automation/create")
def backups_automation_create(
    request: Request,
    type: str = Form(...),
    db: str = Form(...),
    dest: str = Form("/home/vigex/backups"),
    compress: str = Form("gzip"),
    retention: int = Form(7),
    schedule_type: str = Form("daily"),
    schedule_time: str = Form("02:00"),
    weekday: str = Form("1"),
    monthday: str = Form("1"),
    notes: str = Form(""),
):
    if not has_permission(request, "backups"):
        return permission_redirect()

    if type not in ["full", "incremental", "differential"]:
        return RedirectResponse(
            url="/backups?ok=0&msg=Tipo+de+backup+no+valido",
            status_code=303,
        )

    db = (db or "").strip()
    dest = (dest or "/home/vigex/backups").strip()

    if not db:
        return RedirectResponse(
            url="/backups?ok=0&msg=La+base+de+datos+es+obligatoria",
            status_code=303,
        )

    if not dest.startswith("/home/vigex/backups"):
        return RedirectResponse(
            url="/backups?ok=0&msg=La+ruta+destino+debe+estar+dentro+de+/home/vigex/backups",
            status_code=303,
        )

    if compress not in ["gzip", "none"]:
        return RedirectResponse(
            url="/backups?ok=0&msg=Compresion+no+valida",
            status_code=303,
        )

    if retention < 0 or retention > 365:
        return RedirectResponse(
            url="/backups?ok=0&msg=Retencion+no+valida",
            status_code=303,
        )

    history = cargar_historial_backups(limit=1000)

    if type == "incremental" and not backup_has_incremental_base(db, history):
        return RedirectResponse(
            url="/backups?ok=0&msg=No+puedes+automatizar+una+incremental+sin+tener+antes+una+copia+base+de+esa+BD",
            status_code=303,
        )

    if type == "differential" and not backup_has_full_base(db, history):
        return RedirectResponse(
            url="/backups?ok=0&msg=No+puedes+automatizar+una+diferencial+sin+tener+antes+una+copia+completa+de+esa+BD",
            status_code=303,
        )

    try:
        cron_expression, schedule_label = build_backup_cron_expression(schedule_type, schedule_time, weekday, monthday)
    except ValueError as exc:
        return RedirectResponse(
            url=f"/backups?ok=0&msg={quote(str(exc))}",
            status_code=303,
        )

    automation_id = datetime.now().strftime("auto-%Y%m%d%H%M%S")
    name = build_backup_automation_name(type, db)

    base_ref = ""
    if type == "incremental":
        base_ref = "latest"
    elif type == "differential":
        base_ref = "last_full"

    final_notes = (notes or "").strip()
    if not final_notes:
        final_notes = f"Automática CRON {automation_id}"

    command_parts = [
        SCRIPT_BACKUPS,
        type,
        db,
        dest,
        name,
        compress,
        str(retention),
        base_ref,
        final_notes,
    ]

    command_line = " ".join(shlex.quote(part) for part in command_parts)
    command_line = f"mkdir -p {shlex.quote(str(Path(BACKUP_AUTOMATION_LOG).parent))} && {command_line} >> {shlex.quote(BACKUP_AUTOMATION_LOG)} 2>&1"

    metadata = {
        "id": automation_id,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "created_by": request.session.get("user", "desconocido"),
        "type": type,
        "db": db,
        "dest": dest,
        "compress": compress,
        "retention": retention,
        "schedule_type": schedule_type,
        "schedule_time": schedule_time,
        "weekday": weekday,
        "monthday": monthday,
        "schedule_label": schedule_label,
        "cron_expression": cron_expression,
        "name": name,
        "notes": final_notes,
    }

    result = crear_automatizacion_backup_remota(metadata, cron_expression, command_line)
    ok = 1 if result["ok"] else 0

    if ok:
        emit_alert(
            "backup.automation.ok",
            "info",
            "Automatización de backup creada",
            (
                "<b>Automatización CRON creada</b>\n"
                f"Tipo: {type}\n"
                f"BD: {db}\n"
                f"Horario: {schedule_label}\n"
                f"Servidor: {SERVIDOR_BACKUPS}"
            ),
            "backups",
        )
    else:
        emit_alert(
            "backup.automation.error",
            "warning",
            "Error al crear automatización",
            (
                "<b>Error al crear automatización CRON</b>\n"
                f"Tipo: {type}\n"
                f"BD: {db}\n"
                f"Servidor: {SERVIDOR_BACKUPS}\n"
                f"Detalle: {result['text']}"
            ),
            "backups",
        )

    return RedirectResponse(
        url=f"/backups?ok={ok}&msg={quote(result['text'])}",
        status_code=303,
    )


@app.post("/backups/automation/delete")
def backups_automation_delete(
    request: Request,
    automation_id: str = Form(...),
):
    if not has_permission(request, "backups"):
        return permission_redirect()

    result = eliminar_automatizacion_backup_remota(automation_id)
    ok = 1 if result["ok"] else 0

    if ok:
        emit_alert(
            "backup.automation.delete.ok",
            "info",
            "Automatización de backup eliminada",
            (
                "<b>Automatización CRON eliminada</b>\n"
                f"ID: {automation_id}\n"
                f"Servidor: {SERVIDOR_BACKUPS}"
            ),
            "backups",
        )
    else:
        emit_alert(
            "backup.automation.delete.error",
            "warning",
            "Error al eliminar automatización",
            (
                "<b>Error al eliminar automatización CRON</b>\n"
                f"ID: {automation_id}\n"
                f"Servidor: {SERVIDOR_BACKUPS}\n"
                f"Detalle: {result['text']}"
            ),
            "backups",
        )

    return RedirectResponse(
        url=f"/backups?ok={ok}&msg={quote(result['text'])}",
        status_code=303,
    )



@app.get("/backups/download/{backup_id}")
def backups_download(
    request: Request,
    backup_id: int,
):
    if not has_permission(request, "backups"):
        return permission_redirect()

    history = cargar_historial_backups(limit=1000)

    try:
        item = buscar_backup_por_id(backup_id, history)
        remote_path = validar_ruta_backup_descarga(item.get("file", ""))
    except ValueError as exc:
        return RedirectResponse(
            url=f"/backups?ok=0&msg={quote(str(exc))}",
            status_code=303,
        )

    result = leer_backup_remoto(remote_path)

    if not result.get("ok"):
        return RedirectResponse(
            url=f"/backups?ok=0&msg={quote(result.get('text', 'No se pudo descargar el backup'))}",
            status_code=303,
        )

    filename = item.get("filename") or posixpath.basename(remote_path) or f"backup-{backup_id}.sql"
    filename = filename.replace('"', "").replace("'", "").strip() or f"backup-{backup_id}.sql"

    log_event(
        tipo="backup",
        resultado="OK",
        usuario=request.session.get("user", "anon"),
        ip_origen=request.client.host if request.client else None,
        recurso=f"GET /backups/download/{backup_id}",
        detalle=f"Descarga de backup ID={backup_id}: {filename}",
    )

    headers = {
        "Content-Disposition": f"attachment; filename=\"{filename}\"; filename*=UTF-8''{quote(filename)}",
        "X-Vigex-Backup-ID": str(backup_id),
    }

    return Response(
        content=result["content"],
        media_type="application/octet-stream",
        headers=headers,
    )


@app.post("/backups/restore/preview")
def backups_restore_preview(
    request: Request,
    backup_id: int = Form(...),
):
    if not has_permission(request, "backups"):
        return permission_redirect()

    history = cargar_historial_backups(limit=1000)

    try:
        restore_plan = plan_restauracion_backups(backup_id, history)
    except ValueError as exc:
        return RedirectResponse(
            url=f"/backups?ok=0&msg={quote(str(exc))}",
            status_code=303,
        )

    context = get_common_context(request)
    context["ok"] = None
    context["msg"] = None
    context["cacti_url"] = CACTI_URL
    context["backup_history"] = history[:50]
    context["backup_automations"] = cargar_automatizaciones_backups()
    context["delete_plan"] = None
    context["restore_plan"] = restore_plan

    return templates.TemplateResponse(request, "backups.html", context)


@app.post("/backups/restore/confirm")
def backups_restore_confirm(
    request: Request,
    backup_id: int = Form(...),
    confirm_restore: str = Form(""),
):
    if not has_permission(request, "backups"):
        return permission_redirect()

    if confirm_restore != "SI":
        return RedirectResponse(
            url="/backups?ok=0&msg=Restauracion+cancelada",
            status_code=303,
        )

    history = cargar_historial_backups(limit=1000)

    try:
        restore_plan = plan_restauracion_backups(backup_id, history)
    except ValueError as exc:
        return RedirectResponse(
            url=f"/backups?ok=0&msg={quote(str(exc))}",
            status_code=303,
        )

    result = restaurar_backup_remoto(backup_id)
    ok = 1 if result["ok"] and is_ok(result["text"]) else 0

    if ok:
        emit_alert(
            "backup.restore.ok",
            "info",
            "Backup restaurado",
            (
                "<b>Backup restaurado</b>\n"
                f"ID objetivo: {backup_id}\n"
                f"BD: {restore_plan.get('db', '-')}\n"
                f"Cadena: {restore_plan.get('ids_csv', '-')}\n"
                f"Servidor: {SERVIDOR_BACKUPS}"
            ),
            "backups",
        )
    else:
        emit_alert(
            "backup.restore.error",
            "critical",
            "Error al restaurar backup",
            (
                "<b>Error al restaurar backup</b>\n"
                f"ID objetivo: {backup_id}\n"
                f"Servidor: {SERVIDOR_BACKUPS}\n"
                f"Detalle: {result['text']}"
            ),
            "backups",
        )

    return RedirectResponse(
        url=f"/backups?ok={ok}&msg={quote(result['text'])}",
        status_code=303,
    )

@app.post("/backups/delete/preview")
def backups_delete_preview(
    request: Request,
    backup_id: int = Form(...),
):
    if not has_permission(request, "backups"):
        return permission_redirect()

    history = cargar_historial_backups(limit=1000)

    try:
        delete_plan = plan_eliminacion_backups(backup_id, history)
    except ValueError as exc:
        return RedirectResponse(
            url=f"/backups?ok=0&msg={quote(str(exc))}",
            status_code=303,
        )

    context = get_common_context(request)
    context["ok"] = None
    context["msg"] = None
    context["cacti_url"] = CACTI_URL
    context["backup_history"] = history[:50]
    context["backup_automations"] = cargar_automatizaciones_backups()
    context["delete_plan"] = delete_plan
    context["restore_plan"] = None

    return templates.TemplateResponse(request, "backups.html", context)


@app.post("/backups/delete/confirm")
def backups_delete_confirm(
    request: Request,
    backup_id: int = Form(...),
    confirm_delete: str = Form(""),
):
    if not has_permission(request, "backups"):
        return permission_redirect()

    if confirm_delete != "SI":
        return RedirectResponse(
            url="/backups?ok=0&msg=Eliminacion+cancelada",
            status_code=303,
        )

    history = cargar_historial_backups(limit=1000)

    try:
        delete_plan = plan_eliminacion_backups(backup_id, history)
    except ValueError as exc:
        return RedirectResponse(
            url=f"/backups?ok=0&msg={quote(str(exc))}",
            status_code=303,
        )

    ids = delete_plan["ids"]
    result = eliminar_backups_cascada_remoto(ids)
    ok = 1 if result["ok"] and is_ok(result["text"]) else 0

    if ok:
        emit_alert(
            "backup.delete.ok",
            "info",
            "Backups eliminados",
            (
                "<b>Backups eliminados</b>\n"
                f"IDs: {', '.join(ids)}\n"
                f"Servidor: {SERVIDOR_BACKUPS}"
            ),
            "backups",
        )
    else:
        emit_alert(
            "backup.delete.error",
            "critical",
            "Error al eliminar backups",
            (
                "<b>Error al eliminar backups</b>\n"
                f"IDs: {', '.join(ids)}\n"
                f"Servidor: {SERVIDOR_BACKUPS}\n"
                f"Detalle: {result['text']}"
            ),
            "backups",
        )

    return RedirectResponse(
        url=f"/backups?ok={ok}&msg={quote(result['text'])}",
        status_code=303,
    )


@app.post("/backups/run")
def backups_run(
    request: Request,
    type: str = Form(...),
    db: str = Form(...),
    dest: str = Form("/home/vigex/backups"),
    name: str = Form(...),
    compress: str = Form("gzip"),
    retention: int = Form(7),
    base_ref: str = Form(""),
    notes: str = Form(""),
):
    if not has_permission(request, "backups"):
        return permission_redirect()

    if type not in ["full", "incremental", "differential"]:
        return RedirectResponse(
            url="/backups?ok=0&msg=Tipo+de+backup+no+valido",
            status_code=303,
        )

    db = (db or "").strip()
    dest = (dest or "/home/vigex/backups").strip()
    name = (name or "").strip()
    base_ref = (base_ref or "").strip()
    notes = (notes or "").strip()

    if not es_token_simple(db):
        return RedirectResponse(
            url="/backups?ok=0&msg=Nombre+de+base+de+datos+no+valido",
            status_code=303,
        )

    if not es_token_simple(name):
        return RedirectResponse(
            url="/backups?ok=0&msg=Nombre+de+copia+no+valido",
            status_code=303,
        )

    if not dest.startswith("/home/vigex/backups"):
        return RedirectResponse(
            url="/backups?ok=0&msg=La+ruta+destino+debe+estar+dentro+de+/home/vigex/backups",
            status_code=303,
        )

    if compress not in ["gzip", "none"]:
        return RedirectResponse(
            url="/backups?ok=0&msg=Compresion+no+valida",
            status_code=303,
        )

    if retention < 0 or retention > 365:
        return RedirectResponse(
            url="/backups?ok=0&msg=Retencion+no+valida",
            status_code=303,
        )

    if base_ref and not es_token_simple(base_ref):
        return RedirectResponse(
            url="/backups?ok=0&msg=Referencia+base+no+valida",
            status_code=303,
        )

    args = [type, db, dest, name, compress, str(retention), base_ref, notes]
    result = ssh_run(SERVIDOR_BACKUPS, SCRIPT_BACKUPS, args)
    ok = 1 if (result["ok"] and is_ok(result["text"])) else 0

    if ok:
        emit_alert(
            "backup.ok",
            "info",
            "Backup completado",
            (
                "<b>Backup OK</b>\n"
                f"BD: {db}\n"
                f"Tipo: {type}\n"
                f"Destino: {dest}\n"
                f"Servidor: {SERVIDOR_BACKUPS}"
            ),
            "backups",
        )
    else:
        emit_alert(
            "backup.error",
            "critical",
            "Error en backup",
            (
                "<b>Backup ERROR</b>\n"
                f"BD: {db}\n"
                f"Tipo: {type}\n"
                f"Servidor: {SERVIDOR_BACKUPS}\n"
                f"Detalle: {result['text']}"
            ),
            "backups",
        )

    return RedirectResponse(
        url=f"/backups?ok={ok}&msg={quote(result['text'])}",
        status_code=303,
    )

# =====================
# R-049A/R-049B - SOPORTE BASICO + SQLITE
# =====================

import json as _support_json
import sqlite3 as _support_sqlite3
import urllib.request as _support_urlrequest
import urllib.error as _support_urlerror
from datetime import datetime as _support_datetime
from pathlib import Path as _SupportPath

SUPPORT_DATA_DIR = globals().get("DATA_DIR", _SupportPath(__file__).resolve().parent / "data")
SUPPORT_TICKETS_FILE = SUPPORT_DATA_DIR / "support_tickets.json"
SUPPORT_TICKETS_DB = SUPPORT_DATA_DIR / "support_tickets.db"
# =====================
# R-049L - CONFIG API CENTRAL SOPORTE
# =====================

CENTRAL_SUPPORT_ENABLED = os.getenv("CENTRAL_SUPPORT_ENABLED", "false").strip().lower() in ("1", "true", "yes", "on")
CENTRAL_SUPPORT_URL = os.getenv("CENTRAL_SUPPORT_URL", "http://127.0.0.1:8010/api/v1/support/tickets").strip()
CENTRAL_SUPPORT_CLIENT_ID = os.getenv("CENTRAL_SUPPORT_CLIENT_ID", "cliente-demo-a").strip()
CENTRAL_SUPPORT_CLIENT_NAME = os.getenv("CENTRAL_SUPPORT_CLIENT_NAME", "Cliente Demo A").strip()
CENTRAL_SUPPORT_TOKEN = os.getenv("CENTRAL_SUPPORT_TOKEN", "vigex-central-demo-token-lab").strip()
CENTRAL_SUPPORT_TIMEOUT = int(os.getenv("CENTRAL_SUPPORT_TIMEOUT", "5"))

# R-069 / Ruta 8.5 — Webhook Jira (opcional; vacío = desactivado)
JIRA_WEBHOOK_URL = os.getenv("JIRA_WEBHOOK_URL", "").strip()
JIRA_WEBHOOK_TIMEOUT = int(os.getenv("JIRA_WEBHOOK_TIMEOUT", "5"))

# R-080 / Ruta 10.4 — Heartbeat a Central Support
# URL base de la Central (sin path); 0 = desactivado
_CENTRAL_BASE_URL = CENTRAL_SUPPORT_URL.rstrip("/")
if _CENTRAL_BASE_URL.endswith("/api/v1/support/tickets"):
    _CENTRAL_BASE_URL = _CENTRAL_BASE_URL[: -len("/api/v1/support/tickets")]
CENTRAL_HEARTBEAT_URL = (
    f"{_CENTRAL_BASE_URL}/api/v1/heartbeat" if CENTRAL_SUPPORT_ENABLED else ""
)
CENTRAL_HEARTBEAT_INTERVAL = int(os.getenv("CENTRAL_HEARTBEAT_INTERVAL", "300"))  # segundos


SUPPORT_TYPES = [
    "Incidencia",
    "Consulta",
    "Cambio",
    "Mantenimiento",
    "Restauración",
    "Informe",
]

SUPPORT_PRIORITIES = [
    "Crítica",
    "Alta",
    "Media",
    "Baja",
]

SUPPORT_SERVICES = [
    "API / Panel",
    "DB / Logs",
    "Backups",
    "Alertas",
    "Informes",
    "Soporte",
    "Otro",
]


def support_now():
    return _support_datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def support_db_connect():
    SUPPORT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = _support_sqlite3.connect(str(SUPPORT_TICKETS_DB))
    conn.row_factory = _support_sqlite3.Row
    return conn


def ensure_support_db():
    SUPPORT_DATA_DIR.mkdir(parents=True, exist_ok=True)

    with support_db_connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS support_tickets (
                id TEXT PRIMARY KEY,
                fecha_apertura TEXT NOT NULL,
                fecha_actualizacion TEXT NOT NULL,
                cliente TEXT NOT NULL,
                contacto TEXT NOT NULL,
                email TEXT NOT NULL,
                telefono TEXT,
                canal TEXT NOT NULL,
                tipo TEXT NOT NULL,
                prioridad TEXT NOT NULL,
                servicio TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                evidencia TEXT,
                estado TEXT NOT NULL,
                creado_por TEXT NOT NULL,
                origen TEXT NOT NULL DEFAULT 'panel'
            )
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_support_tickets_estado
            ON support_tickets (estado)
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_support_tickets_prioridad
            ON support_tickets (prioridad)
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_support_tickets_fecha
            ON support_tickets (fecha_apertura)
            """
        )

        conn.commit()

        # Migración: añadir columna 'origen' si no existe (tablas creadas antes de R-083)
        try:
            conn.execute("ALTER TABLE support_tickets ADD COLUMN origen TEXT NOT NULL DEFAULT 'panel'")
            conn.commit()
        except Exception:
            pass  # columna ya existe — ignorar

    migrate_support_json_to_sqlite()


def migrate_support_json_to_sqlite():
    if not SUPPORT_TICKETS_FILE.exists():
        return

    try:
        data = _support_json.loads(SUPPORT_TICKETS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return

    if not isinstance(data, list):
        return

    with support_db_connect() as conn:
        for ticket in data:
            if not isinstance(ticket, dict):
                continue

            ticket_id = str(ticket.get("id", "")).strip()
            if not ticket_id:
                continue

            fecha_apertura = str(ticket.get("fecha_apertura", support_now()))
            estado = str(ticket.get("estado", "Abierto"))

            conn.execute(
                """
                INSERT OR IGNORE INTO support_tickets (
                    id,
                    fecha_apertura,
                    fecha_actualizacion,
                    cliente,
                    contacto,
                    email,
                    telefono,
                    canal,
                    tipo,
                    prioridad,
                    servicio,
                    descripcion,
                    evidencia,
                    estado,
                    creado_por,
                    origen
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    ticket_id,
                    fecha_apertura,
                    fecha_apertura,
                    str(ticket.get("cliente", "")),
                    str(ticket.get("contacto", "")),
                    str(ticket.get("email", "")),
                    str(ticket.get("telefono", "")),
                    str(ticket.get("canal", "Panel Vigex")),
                    str(ticket.get("tipo", "Incidencia")),
                    str(ticket.get("prioridad", "Media")),
                    str(ticket.get("servicio", "Otro")),
                    str(ticket.get("descripcion", "")),
                    str(ticket.get("evidencia", "")),
                    estado,
                    str(ticket.get("creado_por", "anon")),
                    "json_migrado",
                ),
            )

        conn.commit()


def support_row_to_dict(row):
    return dict(row)


def load_support_tickets(limit=10):
    ensure_support_db()

    with support_db_connect() as conn:
        rows = conn.execute(
            """
            SELECT
                id,
                fecha_apertura,
                fecha_actualizacion,
                cliente,
                contacto,
                email,
                telefono,
                canal,
                tipo,
                prioridad,
                servicio,
                descripcion,
                evidencia,
                estado,
                creado_por,
                origen
            FROM support_tickets
            ORDER BY fecha_apertura DESC, id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [support_row_to_dict(row) for row in rows]


def _push_ticket_jira_webhook(ticket: dict) -> None:
    """Envía el ticket a un webhook Jira configurado en JIRA_WEBHOOK_URL (R-069).
    Fire-and-forget en hilo daemon; nunca bloquea ni lanza excepción al llamador."""
    if not JIRA_WEBHOOK_URL:
        return

    def _fire():
        try:
            import urllib.request as _req
            import json as _json
            payload = {
                "summary":     f"[Vigex] {ticket.get('tipo','Incidencia')}: {ticket.get('descripcion','')[:120]}",
                "description": ticket.get("descripcion", ""),
                "issue_type":  ticket.get("tipo", "Incidencia"),
                "priority":    ticket.get("prioridad", "Media"),
                "ticket_id":   ticket.get("id", ""),
                "servicio":    ticket.get("servicio", ""),
                "contacto":    ticket.get("contacto", ""),
                "email":       ticket.get("email", ""),
                "cliente":     ticket.get("cliente", ""),
                "fecha":       ticket.get("fecha_apertura", ""),
                "origen":      "vigex-panel",
            }
            body = _json.dumps(payload).encode("utf-8")
            req = _req.Request(
                JIRA_WEBHOOK_URL,
                data=body,
                headers={"Content-Type": "application/json", "User-Agent": "Vigex-Panel/1.0"},
                method="POST",
            )
            with _req.urlopen(req, timeout=JIRA_WEBHOOK_TIMEOUT) as _r:
                pass  # respuesta ignorada intencionadamente
        except Exception:
            pass  # webhook no bloquea el flujo principal

    threading.Thread(target=_fire, daemon=True, name="vigex-jira-hook").start()


def save_support_ticket(ticket):
    ensure_support_db()

    now = support_now()

    with support_db_connect() as conn:
        conn.execute(
            """
            INSERT INTO support_tickets (
                id,
                fecha_apertura,
                fecha_actualizacion,
                cliente,
                contacto,
                email,
                telefono,
                canal,
                tipo,
                prioridad,
                servicio,
                descripcion,
                evidencia,
                estado,
                creado_por,
                origen
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ticket["id"],
                ticket["fecha_apertura"],
                now,
                ticket["cliente"],
                ticket["contacto"],
                ticket["email"],
                ticket.get("telefono", ""),
                ticket["canal"],
                ticket["tipo"],
                ticket["prioridad"],
                ticket["servicio"],
                ticket["descripcion"],
                ticket.get("evidencia", ""),
                ticket["estado"],
                ticket["creado_por"],
                ticket.get("origen", "panel"),  # R-083-fix-6c: respetar el origen del ticket
            ),
        )
        conn.commit()

    # R-069: notificar webhook Jira si está configurado (fire-and-forget)
    _push_ticket_jira_webhook(ticket)


def next_support_ticket_id():
    ensure_support_db()

    year = _support_datetime.now().year
    prefix = f"Vigex-{year}-"
    max_num = 0

    with support_db_connect() as conn:
        rows = conn.execute(
            "SELECT id FROM support_tickets WHERE id LIKE ?",
            (f"{prefix}%",),
        ).fetchall()

    for row in rows:
        ticket_id = str(row["id"])
        try:
            num = int(ticket_id.replace(prefix, ""))
            max_num = max(max_num, num)
        except Exception:
            pass

    return f"{prefix}{max_num + 1:03d}"


# =====================
# R-049M - CENTRAL TICKET ID LOCAL
# =====================

def ensure_support_ticket_central_columns():
    SUPPORT_DATA_DIR.mkdir(parents=True, exist_ok=True)

    with _support_sqlite3.connect(str(SUPPORT_TICKETS_DB)) as conn:
        rows = conn.execute("PRAGMA table_info(support_tickets)").fetchall()
        columns = {row[1] for row in rows}

        if not columns:
            return

        if "central_ticket_id" not in columns:
            conn.execute("ALTER TABLE support_tickets ADD COLUMN central_ticket_id TEXT DEFAULT ''")

        if "central_sync_status" not in columns:
            conn.execute("ALTER TABLE support_tickets ADD COLUMN central_sync_status TEXT DEFAULT ''")

        if "central_sync_detail" not in columns:
            conn.execute("ALTER TABLE support_tickets ADD COLUMN central_sync_detail TEXT DEFAULT ''")

        if "central_sync_at" not in columns:
            conn.execute("ALTER TABLE support_tickets ADD COLUMN central_sync_at TEXT DEFAULT ''")

        conn.commit()


def update_support_ticket_central_sync(
    ticket_id,
    central_ticket_id="",
    central_sync_status="",
    central_sync_detail="",
):
    ensure_support_ticket_central_columns()

    if not ticket_id:
        return

    with _support_sqlite3.connect(str(SUPPORT_TICKETS_DB)) as conn:
        conn.execute(
            """
            UPDATE support_tickets
            SET
                central_ticket_id = ?,
                central_sync_status = ?,
                central_sync_detail = ?,
                central_sync_at = ?
            WHERE id = ?
            """,
            (
                central_ticket_id or "",
                central_sync_status or "",
                central_sync_detail or "",
                _support_datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ticket_id,
            ),
        )
        conn.commit()


# =====================
# R-049N-FIX - ENRIQUECER TICKETS CON CENTRAL
# =====================

def get_support_ticket_central_sync(ticket_id):
    if not ticket_id:
        return {}

    ensure_support_ticket_central_columns()

    with _support_sqlite3.connect(str(SUPPORT_TICKETS_DB)) as conn:
        conn.row_factory = _support_sqlite3.Row
        row = conn.execute(
            """
            SELECT
                central_ticket_id,
                central_sync_status,
                central_sync_detail,
                central_sync_at
            FROM support_tickets
            WHERE id = ?
            """,
            (ticket_id,),
        ).fetchone()

    if not row:
        return {}

    return {
        "central_ticket_id": row["central_ticket_id"] or "",
        "central_sync_status": row["central_sync_status"] or "",
        "central_sync_detail": row["central_sync_detail"] or "",
        "central_sync_at": row["central_sync_at"] or "",
    }


def enrich_support_ticket_with_central(ticket):
    if not ticket:
        return ticket

    try:
        ticket_id = ticket.get("id")
    except Exception:
        return ticket

    sync = get_support_ticket_central_sync(ticket_id)

    for key, value in sync.items():
        ticket[key] = value

    return ticket


def enrich_support_tickets_with_central(tickets):
    if not tickets:
        return tickets

    return [enrich_support_ticket_with_central(ticket) for ticket in tickets]

# =====================
# R-049L - ENVIO A API CENTRAL
# =====================

def send_support_ticket_to_central(ticket):
    if not CENTRAL_SUPPORT_ENABLED:
        return {
            "ok": True,
            "sent": False,
            "skipped": True,
            "detail": "Integración central desactivada",
        }

    if not CENTRAL_SUPPORT_URL or not CENTRAL_SUPPORT_CLIENT_ID or not CENTRAL_SUPPORT_TOKEN:
        return {
            "ok": False,
            "sent": False,
            "skipped": False,
            "detail": "Faltan variables CENTRAL_SUPPORT_URL, CENTRAL_SUPPORT_CLIENT_ID o CENTRAL_SUPPORT_TOKEN",
        }

    payload = {
        "cliente_id": CENTRAL_SUPPORT_CLIENT_ID,
        "nombre_cliente": ticket.get("cliente") or CENTRAL_SUPPORT_CLIENT_NAME,
        "ticket_local_id": ticket.get("id", ""),
        "tipo": ticket.get("tipo", "Incidencia"),
        "prioridad": ticket.get("prioridad", "Media"),
        "servicio": ticket.get("servicio", "Otro"),
        "descripcion": ticket.get("descripcion", ""),
        "evidencia": ticket.get("evidencia", ""),
        "contacto": ticket.get("contacto", ""),
        "email": ticket.get("email", ""),
        "fecha_origen": ticket.get("fecha_apertura", ""),
        "version_panel": os.getenv("VIGEX_VERSION", "lab-local"),
        "origen": "panel-local",
    }

    data = _support_json.dumps(payload, ensure_ascii=False).encode("utf-8")

    req = _support_urlrequest.Request(
        CENTRAL_SUPPORT_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "X-Vigex-Client-Token": CENTRAL_SUPPORT_TOKEN,
        },
        method="POST",
    )

    try:
        with _support_urlrequest.urlopen(req, timeout=CENTRAL_SUPPORT_TIMEOUT) as response:
            raw = response.read().decode("utf-8", errors="replace")
            try:
                parsed = _support_json.loads(raw)
            except Exception:
                parsed = {}

            return {
                "ok": 200 <= response.status < 300,
                "sent": 200 <= response.status < 300,
                "skipped": False,
                "status": response.status,
                "central_ticket_id": parsed.get("central_ticket_id", ""),
                "detail": raw,
            }

    except _support_urlerror.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        return {
            "ok": False,
            "sent": False,
            "skipped": False,
            "status": e.code,
            "central_ticket_id": "",
            "detail": raw,
        }

    except Exception as e:
        return {
            "ok": False,
            "sent": False,
            "skipped": False,
            "status": 0,
            "central_ticket_id": "",
            "detail": str(e),
        }




# =====================
# R-049T-A - SEPARACION SOPORTE LOCAL CLIENTE
# =====================

def is_local_internal_support_enabled():
    return os.getenv("VIGEX_LOCAL_INTERNAL_SUPPORT_ENABLED", "false").strip().lower() in ("1", "true", "yes", "on")


def local_internal_support_redirect():
    return RedirectResponse(
        url="/soporte?ok=0&msg=Gestion+interna+reservada+al+panel+central+Vigex",
        status_code=303,
    )

@app.get("/soporte")
def soporte_page(request: Request):
    if not is_admin(request):
        return permission_redirect("Acceso reservado al equipo técnico Vigex.")

    context = get_common_context(request)
    context["local_internal_support_enabled"] = is_local_internal_support_enabled()
    tickets = load_support_tickets(limit=10)

    context["ok"] = request.query_params.get("ok")
    context["msg"] = request.query_params.get("msg")
    context["ticket_id"] = request.query_params.get("ticket_id")
    context["support_types"] = SUPPORT_TYPES
    context["support_priorities"] = SUPPORT_PRIORITIES
    context["support_services"] = SUPPORT_SERVICES
    context["tickets"] = tickets
    context["support_storage"] = "SQLite"

    return templates.TemplateResponse(request, "soporte.html", context)


@app.post("/soporte")
def soporte_create(
    request: Request,
    empresa: str = Form(...),
    contacto: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(""),
    tipo: str = Form(...),
    prioridad: str = Form(...),
    servicio: str = Form(...),
    descripcion: str = Form(...),
    evidencia: str = Form(""),
):
    if not is_admin(request):
        return permission_redirect("Acceso reservado al equipo técnico Vigex.")

    empresa = (empresa or "").strip()
    contacto = (contacto or "").strip()
    email = (email or "").strip()
    telefono = (telefono or "").strip()
    tipo = (tipo or "").strip()
    prioridad = (prioridad or "").strip()
    servicio = (servicio or "").strip()
    descripcion = (descripcion or "").strip()
    evidencia = (evidencia or "").strip()

    if not empresa or not contacto or not email or not descripcion:
        return RedirectResponse(
            url="/soporte?ok=0&msg=Faltan+campos+obligatorios",
            status_code=303,
        )

    if tipo not in SUPPORT_TYPES:
        tipo = "Incidencia"

    if prioridad not in SUPPORT_PRIORITIES:
        prioridad = "Media"

    if servicio not in SUPPORT_SERVICES:
        servicio = "Otro"

    ticket_id = next_support_ticket_id()

    ticket = {
        "id": ticket_id,
        "fecha_apertura": support_now(),
        "cliente": empresa,
        "contacto": contacto,
        "email": email,
        "telefono": telefono,
        "canal": "Panel Vigex",
        "tipo": tipo,
        "prioridad": prioridad,
        "servicio": servicio,
        "descripcion": descripcion,
        "evidencia": evidencia,
        "estado": "Abierto",
        "creado_por": request.session.get("user", "anon"),
    }

    save_support_ticket(ticket)

    central_result = send_support_ticket_to_central(ticket)

    if central_result.get("sent"):
        central_msg = f"Ticket creado y enviado al panel central: {central_result.get('central_ticket_id', '')}"
        central_log_result = "OK"
        central_log_detail = f"Enviado a central: {central_result.get('central_ticket_id', '')}"
    elif central_result.get("skipped"):
        central_msg = "Ticket creado correctamente"
        central_log_result = "OK"
        central_log_detail = central_result.get("detail", "Integración central desactivada")
    else:
        central_msg = "Ticket creado. Aviso: no se pudo enviar al panel central"
        central_log_result = "ERROR"
        central_log_detail = central_result.get("detail", "Error desconocido")

    if central_result.get("sent"):
        central_sync_status = "sent"
    elif central_result.get("skipped"):
        central_sync_status = "disabled"
    else:
        central_sync_status = "error"

    update_support_ticket_central_sync(
        ticket_id=ticket_id,
        central_ticket_id=central_result.get("central_ticket_id", ""),
        central_sync_status=central_sync_status,
        central_sync_detail=central_log_detail[:500],
    )

    log_event(
        tipo="soporte",
        resultado=central_log_result,
        usuario=request.session.get("user", "anon"),
        ip_origen=request.client.host if request.client else None,
        recurso=f"POST /soporte central {ticket_id}",
        detalle=central_log_detail[:250],
    )

    log_event(
        tipo="soporte",
        resultado="OK",
        usuario=request.session.get("user", "anon"),
        ip_origen=request.client.host if request.client else None,
        recurso=f"POST /soporte {ticket_id}",
        detalle=f"Ticket de soporte creado: {tipo} / {prioridad} / {servicio}",
    )

    return RedirectResponse(
        url=f"/soporte?ok=1&ticket_id={ticket_id}&msg={quote(central_msg)}",
        status_code=303,
    )

# =====================
# R-049C - VISTA INTERNA TICKETS
# =====================

SUPPORT_STATUSES = [
    "Abierto",
    "En análisis",
    "En curso",
    "Esperando cliente",
    "Cerrado",
]


def search_support_tickets(estado="", prioridad="", tipo="", q="", limit=100,
                           origen="", exclude_origen=""):
    """Busca tickets con filtros. origen/exclude_origen filtran por columna 'origen'. R-083-fix-6"""
    ensure_support_db()

    where = []
    params = []

    estado = (estado or "").strip()
    prioridad = (prioridad or "").strip()
    tipo = (tipo or "").strip()
    q = (q or "").strip()
    origen = (origen or "").strip()
    exclude_origen = (exclude_origen or "").strip()

    if estado:
        where.append("estado = ?")
        params.append(estado)

    if prioridad:
        where.append("prioridad = ?")
        params.append(prioridad)

    if tipo:
        where.append("tipo = ?")
        params.append(tipo)

    if origen:
        where.append("origen = ?")
        params.append(origen)

    if exclude_origen:
        where.append("origen != ?")
        params.append(exclude_origen)

    if q:
        like = f"%{q}%"
        where.append(
            """
            (
                id LIKE ?
                OR cliente LIKE ?
                OR contacto LIKE ?
                OR email LIKE ?
                OR servicio LIKE ?
                OR descripcion LIKE ?
                OR evidencia LIKE ?
            )
            """
        )
        params.extend([like, like, like, like, like, like, like])

    sql = """
        SELECT
            id,
            fecha_apertura,
            fecha_actualizacion,
            cliente,
            contacto,
            email,
            telefono,
            canal,
            tipo,
            prioridad,
            servicio,
            descripcion,
            evidencia,
            estado,
            creado_por,
            origen
        FROM support_tickets
    """

    if where:
        sql += " WHERE " + " AND ".join(where)

    sql += " ORDER BY fecha_apertura DESC, id DESC LIMIT ?"
    params.append(limit)

    with support_db_connect() as conn:
        rows = conn.execute(sql, params).fetchall()

    tickets = [support_row_to_dict(row) for row in rows]

    # R-049N-FIX4 search_support_tickets enriched real
    if "enrich_support_tickets_with_central" in globals():
        tickets = enrich_support_tickets_with_central(tickets)

    return tickets


def get_support_ticket(ticket_id):
    ensure_support_ticket_central_columns()  # R-049N detail
    ensure_support_db()

    with support_db_connect() as conn:
        row = conn.execute(
            """
            SELECT
                id,
                fecha_apertura,
                fecha_actualizacion,
                cliente,
                contacto,
                email,
                telefono,
                canal,
                tipo,
                prioridad,
                servicio,
                descripcion,
                evidencia,
                estado,
                creado_por,
                origen
            FROM support_tickets
            WHERE id = ?
            """,
            (ticket_id,),
        ).fetchone()

    if not row:
        return None

    return support_row_to_dict(row)


def support_ticket_counts(origen: str = "", exclude_origen: str = ""):
    """Cuenta tickets con filtro opcional de origen. R-083-fix-6b"""
    ensure_support_db()

    counts = {
        "total": 0,
        "por_estado": {},
        "por_prioridad": {},
    }

    where_parts = []
    params: list = []
    if origen:
        where_parts.append("origen = ?")
        params.append(origen)
    if exclude_origen:
        where_parts.append("origen != ?")
        params.append(exclude_origen)
    where = ("WHERE " + " AND ".join(where_parts)) if where_parts else ""

    with support_db_connect() as conn:
        total_row = conn.execute(
            f"SELECT COUNT(*) AS total FROM support_tickets {where}", params
        ).fetchone()
        counts["total"] = total_row["total"] if total_row else 0

        for row in conn.execute(
            f"SELECT estado, COUNT(*) AS total FROM support_tickets {where} GROUP BY estado ORDER BY estado",
            params,
        ):
            counts["por_estado"][row["estado"]] = row["total"]

        for row in conn.execute(
            f"SELECT prioridad, COUNT(*) AS total FROM support_tickets {where} GROUP BY prioridad ORDER BY prioridad",
            params,
        ):
            counts["por_prioridad"][row["prioridad"]] = row["total"]

    return counts



# =====================
# R-049O - COLA OFFLINE Y REINTENTOS CENTRAL
# =====================

def get_pending_central_sync_tickets(limit=50):
    ensure_support_ticket_central_columns()
    ensure_support_db()

    with support_db_connect() as conn:
        rows = conn.execute(
            """
            SELECT
                id,
                fecha_apertura,
                fecha_actualizacion,
                cliente,
                contacto,
                email,
                telefono,
                canal,
                tipo,
                prioridad,
                servicio,
                descripcion,
                evidencia,
                estado,
                creado_por,
                origen,
                central_ticket_id,
                central_sync_status,
                central_sync_detail,
                central_sync_at
            FROM support_tickets
            WHERE
                COALESCE(central_ticket_id, '') = ''
                AND COALESCE(central_sync_status, '') = 'error'
            ORDER BY fecha_apertura ASC, id ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    tickets = [support_row_to_dict(row) for row in rows]
    return enrich_support_tickets_with_central(tickets)


def retry_support_ticket_to_central(ticket_id):
    ticket = get_support_ticket(ticket_id)
    ticket = enrich_support_ticket_with_central(ticket)

    if not ticket:
        return {
            "ok": False,
            "sent": False,
            "ticket_id": ticket_id,
            "detail": "Ticket local no encontrado",
        }

    if ticket.get("central_ticket_id"):
        return {
            "ok": True,
            "sent": False,
            "ticket_id": ticket_id,
            "central_ticket_id": ticket.get("central_ticket_id", ""),
            "detail": "Ticket ya sincronizado previamente",
        }

    central_result = send_support_ticket_to_central(ticket)

    if central_result.get("sent"):
        central_sync_status = "sent"
        central_log_result = "OK"
        central_log_detail = f"Reintento enviado a central: {central_result.get('central_ticket_id', '')}"
    elif central_result.get("skipped"):
        central_sync_status = "disabled"
        central_log_result = "OK"
        central_log_detail = central_result.get("detail", "Integración central desactivada")
    else:
        central_sync_status = "error"
        central_log_result = "ERROR"
        central_log_detail = central_result.get("detail", "Error desconocido")

    update_support_ticket_central_sync(
        ticket_id=ticket_id,
        central_ticket_id=central_result.get("central_ticket_id", ""),
        central_sync_status=central_sync_status,
        central_sync_detail=central_log_detail[:500],
    )

    return {
        "ok": central_result.get("sent", False),
        "sent": central_result.get("sent", False),
        "ticket_id": ticket_id,
        "central_ticket_id": central_result.get("central_ticket_id", ""),
        "status": central_sync_status,
        "log_result": central_log_result,
        "detail": central_log_detail,
    }


def retry_pending_central_sync_tickets(limit=50):
    pending = get_pending_central_sync_tickets(limit=limit)
    results = []

    for ticket in pending:
        results.append(retry_support_ticket_to_central(ticket.get("id")))

    return results


@app.post("/soporte/tickets/reintentar-central")
def soporte_retry_central_pending(request: Request):
    if not is_admin(request):
        return permission_redirect("Acceso reservado al equipo técnico Vigex.")

    if not is_local_internal_support_enabled():
        return local_internal_support_redirect()

    results = retry_pending_central_sync_tickets(limit=50)

    total = len(results)
    sent = sum(1 for item in results if item.get("sent"))
    errors = sum(1 for item in results if item.get("status") == "error")

    log_event(
        tipo="soporte",
        resultado="OK" if errors == 0 else "ERROR",
        usuario=request.session.get("user", "anon"),
        ip_origen=request.client.host if request.client else None,
        recurso="POST /soporte/tickets/reintentar-central",
        detalle=f"Reintentos central: total={total}, enviados={sent}, errores={errors}",
    )

    return RedirectResponse(
        url=f"/soporte/tickets?msg=Reintentos+central:+total+{total},+enviados+{sent},+errores+{errors}",
        status_code=303,
    )



# =====================
# R-049W-FIX1 - VISTA CLIENTE ESTADO TICKET
# =====================

def get_support_ticket_client_progress(ticket):
    estado = (ticket.get("estado") or "").strip()

    if estado in ("Cerrado", "Resuelto"):
        return {
            "label": "Finalizado",
            "percent": 100,
        }

    if estado in ("En curso", "En análisis"):
        return {
            "label": "En revisión por el equipo Vigex",
            "percent": 60,
        }

    if estado == "Pendiente cliente":
        return {
            "label": "Pendiente de información del cliente",
            "percent": 70,
        }

    return {
        "label": "Solicitud registrada",
        "percent": 25,
    }


@app.get("/soporte/estado/{ticket_id}")
def soporte_ticket_estado_cliente(request: Request, ticket_id: str):
    context = get_common_context(request)

    ticket = get_support_ticket(ticket_id)
    ticket = enrich_support_ticket_with_central(ticket)

    if not ticket:
        return RedirectResponse(
            url="/soporte?ok=0&msg=Ticket+no+encontrado",
            status_code=303,
        )

    context["ticket"] = ticket
    context["progress"] = get_support_ticket_client_progress(ticket)

    return templates.TemplateResponse(
        request,
        "soporte_ticket_estado_cliente.html",
        context,
    )

# =====================
# R-049W - PANEL VISUAL COLA SINCRONIZACION
# =====================

def get_central_sync_state(ticket):
    central_ticket_id = (ticket.get("central_ticket_id") or "").strip()
    status = (ticket.get("central_sync_status") or "").strip().lower()

    if central_ticket_id:
        return "sent"

    if status == "error":
        return "error"

    if status == "disabled":
        return "disabled"

    return "no_central"


def get_central_sync_label(state):
    labels = {
        "sent": "Enviado",
        "error": "Pendiente / error",
        "disabled": "Desactivado",
        "no_central": "Sin central",
    }

    return labels.get(state, "Sin central")


def build_central_sync_summary(tickets):
    summary = {
        "total": len(tickets or []),
        "sent": 0,
        "error": 0,
        "disabled": 0,
        "no_central": 0,
    }

    for ticket in tickets or []:
        state = get_central_sync_state(ticket)

        if state not in summary:
            state = "no_central"

        summary[state] += 1

    summary["pending"] = summary["error"]

    return summary


def filter_tickets_by_central_sync(tickets, sync_filter=""):
    sync_filter = (sync_filter or "").strip().lower()

    if sync_filter in ("", "all"):
        return tickets

    if sync_filter == "pending":
        sync_filter = "error"

    return [
        ticket
        for ticket in tickets
        if get_central_sync_state(ticket) == sync_filter
    ]


@app.get("/soporte/sincronizacion")
def soporte_sync_dashboard(request: Request, sync: str = ""):
    if not is_admin(request):
        return permission_redirect("Acceso reservado al equipo técnico Vigex.")

    if not is_local_internal_support_enabled():
        return local_internal_support_redirect()

    context = get_common_context(request)

    tickets_all = search_support_tickets(limit=300)
    summary = build_central_sync_summary(tickets_all)
    tickets = filter_tickets_by_central_sync(tickets_all, sync)

    context["tickets"] = tickets
    context["sync_summary"] = summary
    context["sync_filter"] = (sync or "all").strip().lower()
    context["sync_filters"] = [
        {"key": "all", "label": "Todos"},
        {"key": "sent", "label": "Enviados"},
        {"key": "pending", "label": "Pendientes / error"},
        {"key": "disabled", "label": "Desactivados"},
        {"key": "no_central", "label": "Sin central"},
    ]
    context["msg"] = request.query_params.get("msg")
    context["ok"] = request.query_params.get("ok")

    return templates.TemplateResponse(
        request,
        "soporte_sincronizacion.html",
        context,
    )


@app.post("/soporte/sincronizacion/reintentar-central")
def soporte_sync_retry_central_pending(request: Request):
    if not is_admin(request):
        return permission_redirect("Acceso reservado al equipo técnico Vigex.")

    if not is_local_internal_support_enabled():
        return local_internal_support_redirect()

    results = retry_pending_central_sync_tickets(limit=50)

    total = len(results)
    sent = sum(1 for item in results if item.get("sent"))
    errors = sum(1 for item in results if item.get("status") == "error")

    log_event(
        tipo="soporte",
        resultado="OK" if errors == 0 else "ERROR",
        usuario=request.session.get("user", "anon"),
        ip_origen=request.client.host if request.client else None,
        recurso="POST /soporte/sincronizacion/reintentar-central",
        detalle=f"Reintentos central desde panel sincronizacion: total={total}, enviados={sent}, errores={errors}",
    )

    return RedirectResponse(
        url=f"/soporte/sincronizacion?ok=1&msg=Reintentos+central:+total+{total},+enviados+{sent},+errores+{errors}",
        status_code=303,
    )

@app.get("/soporte/tickets")
def soporte_tickets_page(
    request: Request,
    estado: str = "",
    prioridad: str = "",
    tipo: str = "",
    q: str = "",
):
    if not is_admin(request):
        return permission_redirect("Acceso reservado al equipo técnico Vigex.")

    if not is_local_internal_support_enabled():
        return local_internal_support_redirect()

    context = get_common_context(request)

    # Excluir reportes internos (bug/sugerencia/pregunta) del listado de soporte — R-083-fix-6
    tickets = search_support_tickets(
        estado=estado,
        prioridad=prioridad,
        tipo=tipo,
        q=q,
        limit=100,
        exclude_origen="bug_report",
    )

    context["tickets"] = tickets
    context["counts"] = support_ticket_counts(exclude_origen="bug_report")
    context["support_statuses"] = SUPPORT_STATUSES
    context["support_priorities"] = SUPPORT_PRIORITIES
    context["support_types"] = SUPPORT_TYPES
    context["filters"] = {
        "estado": estado,
        "prioridad": prioridad,
        "tipo": tipo,
        "q": q,
    }
    context["modo_reportes"] = False

    context["central_pending_count"] = len(get_pending_central_sync_tickets(limit=200))
    context["central_sync_summary"] = build_central_sync_summary(tickets)

    return templates.TemplateResponse(request, "soporte_tickets.html", context)



# ─────────────────────────────────────────────────────────────────────────────
# R-083-fix-6 — Sección "Reportes" (Bug / Sugerencia / Pregunta del panel)
# Separada del listado de soporte al cliente.
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/soporte/reportes")
def soporte_reportes_page(
    request: Request,
    estado: str = "",
    prioridad: str = "",
    q: str = "",
):
    if not is_admin(request):
        return permission_redirect("Acceso reservado al equipo técnico Vigex.")

    if not is_local_internal_support_enabled():
        return local_internal_support_redirect()

    context = get_common_context(request)

    tickets = search_support_tickets(
        estado=estado,
        prioridad=prioridad,
        q=q,
        limit=200,
        origen="bug_report",
    )

    context["tickets"] = tickets
    context["counts"] = support_ticket_counts(origen="bug_report")
    context["support_statuses"] = SUPPORT_STATUSES
    context["support_priorities"] = SUPPORT_PRIORITIES
    context["support_types"] = SUPPORT_TYPES
    context["filters"] = {
        "estado":    estado,
        "prioridad": prioridad,
        "tipo":      "",
        "q":         q,
    }
    context["central_pending_count"] = 0
    context["central_sync_summary"] = None
    context["modo_reportes"] = True   # flag para que el template adapte título y botones

    return templates.TemplateResponse(request, "soporte_tickets.html", context)


# =====================
# R-049P - SINCRONIZACION ESTADO CENTRAL A LOCAL
# =====================

def get_central_ticket_status_url(central_ticket_id):
    base = (CENTRAL_SUPPORT_URL or "").strip().rstrip("/")

    if not base:
        return ""

    if base.endswith("/api/v1/support/tickets"):
        return f"{base}/{central_ticket_id}"

    if "/api/v1/support/tickets" in base:
        return f"{base.split('/api/v1/support/tickets')[0]}/api/v1/support/tickets/{central_ticket_id}"

    return f"{base}/api/v1/support/tickets/{central_ticket_id}"


def fetch_central_ticket_status(central_ticket_id):
    if not CENTRAL_SUPPORT_ENABLED:
        return {
            "ok": False,
            "detail": "Integración central desactivada",
        }

    if not central_ticket_id:
        return {
            "ok": False,
            "detail": "El ticket local no tiene central_ticket_id",
        }

    url = get_central_ticket_status_url(central_ticket_id)

    if not url:
        return {
            "ok": False,
            "detail": "No se pudo construir la URL de consulta central",
        }

    req = _support_urlrequest.Request(
        url,
        headers={
            "X-Vigex-Client-Token": CENTRAL_SUPPORT_TOKEN,
            "X-Vigex-Client-ID": CENTRAL_SUPPORT_CLIENT_ID,
        },
        method="GET",
    )

    try:
        with _support_urlrequest.urlopen(req, timeout=CENTRAL_SUPPORT_TIMEOUT) as response:
            raw = response.read().decode("utf-8", errors="replace")

            try:
                parsed = _support_json.loads(raw)
            except Exception:
                parsed = {}

            if not (200 <= response.status < 300):
                return {
                    "ok": False,
                    "status": response.status,
                    "detail": raw,
                }

            return {
                "ok": True,
                "status": response.status,
                "ticket": parsed.get("ticket", {}),
                "detail": raw,
            }

    except _support_urlerror.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        return {
            "ok": False,
            "status": e.code,
            "detail": raw,
        }

    except Exception as e:
        return {
            "ok": False,
            "status": 0,
            "detail": str(e),
        }


def map_central_status_to_local(central_estado):
    central_estado = (central_estado or "").strip()

    mapping = {
        "Nuevo": "Abierto",
        "En análisis": "En análisis",
        "Pendiente cliente": "Pendiente cliente",
        "En curso": "En curso",
        "Resuelto": "Resuelto",
        "Cerrado": "Cerrado",
    }

    return mapping.get(central_estado, central_estado)


def sync_support_ticket_from_central(ticket_id, usuario="central-sync"):
    ticket = get_support_ticket(ticket_id)
    ticket = enrich_support_ticket_with_central(ticket)

    if not ticket:
        return {
            "ok": False,
            "detail": "Ticket local no encontrado",
        }

    central_ticket_id = ticket.get("central_ticket_id", "")

    if not central_ticket_id:
        return {
            "ok": False,
            "detail": "El ticket local no tiene referencia central",
        }

    result = fetch_central_ticket_status(central_ticket_id)

    if not result.get("ok"):
        update_support_ticket_central_sync(
            ticket_id=ticket_id,
            central_ticket_id=central_ticket_id,
            central_sync_status=ticket.get("central_sync_status") or "sent",
            central_sync_detail=f"No se pudo consultar estado central: {result.get('detail', 'Error desconocido')}"[:500],
        )

        return {
            "ok": False,
            "detail": result.get("detail", "No se pudo consultar estado central"),
        }

    central_ticket = result.get("ticket", {})
    central_estado = central_ticket.get("estado", "")
    central_prioridad = central_ticket.get("prioridad", "")

    local_estado = map_central_status_to_local(central_estado)
    local_prioridad = central_prioridad

    ok, msg = update_support_ticket_status_priority(
        ticket_id=ticket_id,
        nuevo_estado=local_estado,
        nueva_prioridad=local_prioridad,
        usuario=usuario,
    )

    detail = (
        f"Sincronizado desde central {central_ticket_id}: "
        f"estado central={central_estado}, estado local={local_estado}, "
        f"prioridad={local_prioridad}"
    )

    update_support_ticket_central_sync(
        ticket_id=ticket_id,
        central_ticket_id=central_ticket_id,
        central_sync_status="sent",
        central_sync_detail=detail[:500],
    )

    return {
        "ok": ok,
        "detail": detail if ok else msg,
        "central_ticket_id": central_ticket_id,
        "central_estado": central_estado,
        "local_estado": local_estado,
        "central_prioridad": central_prioridad,
    }


@app.post("/soporte/tickets/{ticket_id}/sync-central")
def soporte_ticket_sync_central_status(request: Request, ticket_id: str):
    if not is_admin(request):
        return permission_redirect("Acceso reservado al equipo técnico Vigex.")

    if not is_local_internal_support_enabled():
        return local_internal_support_redirect()

    usuario = request.session.get("user", "anon")

    result = sync_support_ticket_from_central(ticket_id, usuario=usuario)

    log_event(
        tipo="soporte",
        resultado="OK" if result.get("ok") else "ERROR",
        usuario=usuario,
        ip_origen=request.client.host if request.client else None,
        recurso=f"POST /soporte/tickets/{ticket_id}/sync-central",
        detalle=result.get("detail", "")[:250],
    )

    if result.get("ok"):
        return RedirectResponse(
            url=f"/soporte/tickets/{ticket_id}?ok=1&msg=Sincronizado+desde+central",
            status_code=303,
        )

    return RedirectResponse(
        url=f"/soporte/tickets/{ticket_id}?ok=0&msg=No+se+pudo+sincronizar+desde+central",
        status_code=303,
    )

@app.get("/soporte/tickets/{ticket_id}")
def soporte_ticket_detail_page(request: Request, ticket_id: str):
    if not is_admin(request):
        return permission_redirect("Acceso reservado al equipo técnico Vigex.")

    if not is_local_internal_support_enabled():
        return local_internal_support_redirect()

    context = get_common_context(request)
    ticket = get_support_ticket(ticket_id)
    ticket = enrich_support_ticket_with_central(ticket)
    if not ticket:
        return RedirectResponse(
            url="/soporte/tickets?msg=Ticket+no+encontrado",
            status_code=303,
        )

    context["ticket"] = ticket
    context["support_statuses"] = SUPPORT_STATUSES
    context["support_priorities"] = SUPPORT_PRIORITIES
    history = get_support_ticket_history(ticket_id)
    context["history"] = history
    context["external_summary_text"] = render_support_external_summary(ticket, history)
    context["response_templates"] = get_support_response_templates()
    selected_template_key = request.query_params.get("plantilla", "")
    selected_template, selected_response_text = render_support_response_template(ticket, selected_template_key)
    context["selected_template_key"] = selected_template_key
    context["selected_template"] = selected_template
    context["selected_response_text"] = selected_response_text
    context["ok"] = request.query_params.get("ok")
    context["msg"] = request.query_params.get("msg")
    return templates.TemplateResponse(request, "soporte_ticket_detalle.html", context)

# =====================
# R-049D - ESTADOS Y PRIORIDADES TICKETS
# =====================

def ensure_support_history_table():
    ensure_support_db()

    with support_db_connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS support_ticket_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT NOT NULL,
                fecha TEXT NOT NULL,
                usuario TEXT NOT NULL,
                accion TEXT NOT NULL,
                valor_anterior TEXT,
                valor_nuevo TEXT,
                detalle TEXT
            )
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_support_history_ticket
            ON support_ticket_history (ticket_id)
            """
        )

        conn.commit()


def add_support_ticket_history(ticket_id, usuario, accion, valor_anterior="", valor_nuevo="", detalle=""):
    ensure_support_history_table()

    with support_db_connect() as conn:
        conn.execute(
            """
            INSERT INTO support_ticket_history (
                ticket_id,
                fecha,
                usuario,
                accion,
                valor_anterior,
                valor_nuevo,
                detalle
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ticket_id,
                support_now(),
                usuario,
                accion,
                valor_anterior,
                valor_nuevo,
                detalle,
            ),
        )
        conn.commit()


def get_support_ticket_history(ticket_id):
    ensure_support_history_table()

    with support_db_connect() as conn:
        rows = conn.execute(
            """
            SELECT
                id,
                ticket_id,
                fecha,
                usuario,
                accion,
                valor_anterior,
                valor_nuevo,
                detalle
            FROM support_ticket_history
            WHERE ticket_id = ?
            ORDER BY fecha DESC, id DESC
            """,
            (ticket_id,),
        ).fetchall()

    return [support_row_to_dict(row) for row in rows]


def update_support_ticket_status_priority(ticket_id, nuevo_estado, nueva_prioridad, usuario):
    ensure_support_db()

    ticket = get_support_ticket(ticket_id)

    ticket = enrich_support_ticket_with_central(ticket)
    if not ticket:
        return False, "Ticket no encontrado"

    nuevo_estado = (nuevo_estado or "").strip()
    nueva_prioridad = (nueva_prioridad or "").strip()

    if nuevo_estado not in SUPPORT_STATUSES:
        return False, "Estado no válido"

    if nueva_prioridad not in SUPPORT_PRIORITIES:
        return False, "Prioridad no válida"

    estado_anterior = ticket.get("estado", "")
    prioridad_anterior = ticket.get("prioridad", "")

    cambios = []

    if estado_anterior != nuevo_estado:
        cambios.append(f"estado: {estado_anterior} -> {nuevo_estado}")

    if prioridad_anterior != nueva_prioridad:
        cambios.append(f"prioridad: {prioridad_anterior} -> {nueva_prioridad}")

    if not cambios:
        return True, "Sin cambios"

    now = support_now()

    with support_db_connect() as conn:
        conn.execute(
            """
            UPDATE support_tickets
            SET
                estado = ?,
                prioridad = ?,
                fecha_actualizacion = ?
            WHERE id = ?
            """,
            (
                nuevo_estado,
                nueva_prioridad,
                now,
                ticket_id,
            ),
        )
        conn.commit()

    if estado_anterior != nuevo_estado:
        add_support_ticket_history(
            ticket_id=ticket_id,
            usuario=usuario,
            accion="Cambio de estado",
            valor_anterior=estado_anterior,
            valor_nuevo=nuevo_estado,
            detalle=f"Estado actualizado desde la vista interna",
        )

    if prioridad_anterior != nueva_prioridad:
        add_support_ticket_history(
            ticket_id=ticket_id,
            usuario=usuario,
            accion="Cambio de prioridad",
            valor_anterior=prioridad_anterior,
            valor_nuevo=nueva_prioridad,
            detalle=f"Prioridad actualizada desde la vista interna",
        )

    return True, "; ".join(cambios)


@app.post("/soporte/tickets/{ticket_id}/estado")
def soporte_ticket_update_status_priority(
    request: Request,
    ticket_id: str,
    estado: str = Form(...),
    prioridad: str = Form(...),
    nota: str = Form(""),
):
    if not is_admin(request):
        return permission_redirect("Acceso reservado al equipo técnico Vigex.")

    if not is_local_internal_support_enabled():
        return local_internal_support_redirect()

    usuario = request.session.get("user", "anon")

    # La nota es obligatoria para registrar un cambio de estado/prioridad — R-083-fix-8
    nota = (nota or "").strip()
    if not nota:
        return RedirectResponse(
            url=f"/soporte/tickets/{ticket_id}?ok=0&msg=Escribe+una+nota+antes+de+guardar",
            status_code=303,
        )

    ok, msg = update_support_ticket_status_priority(
        ticket_id=ticket_id,
        nuevo_estado=estado,
        nueva_prioridad=prioridad,
        usuario=usuario,
    )

    # Guardar la nota en el historial del ticket
    if ok and nota:
        add_support_ticket_history(
            ticket_id=ticket_id,
            usuario=usuario,
            accion="Nota / Respuesta",
            detalle=nota,
        )

    log_event(
        tipo="soporte",
        resultado="OK" if ok else "ERROR",
        usuario=usuario,
        ip_origen=request.client.host if request.client else None,
        recurso=f"POST /soporte/tickets/{ticket_id}/estado",
        detalle=msg,
    )

    if ok:
        return RedirectResponse(
            url=f"/soporte/tickets/{ticket_id}?ok=1&msg=Ticket+actualizado",
            status_code=303,
        )

    return RedirectResponse(
        url=f"/soporte/tickets/{ticket_id}?ok=0&msg=No+se+pudo+actualizar",
        status_code=303,
    )

# =====================
# R-049E - PLANTILLAS RESPUESTA SOPORTE
# =====================

SUPPORT_RESPONSE_TEMPLATES = [
    {
        "key": "recepcion",
        "titulo": "Confirmación de recepción",
        "uso": "Confirmar que la solicitud ha sido recibida.",
        "texto": """Hola {contacto},

Hemos recibido tu solicitud correctamente.

Referencia interna: {ticket_id}

La hemos registrado internamente y vamos a revisarla según la prioridad indicada.

Servicio afectado: {servicio}
Tipo de solicitud: {tipo}
Prioridad: {prioridad}

Te informaremos cuando tengamos un diagnóstico o si necesitamos más información.

Un saludo,
Equipo Vigex""",
    },
    {
        "key": "mas_informacion",
        "titulo": "Solicitud de más información",
        "uso": "Pedir datos adicionales para poder diagnosticar.",
        "texto": """Hola {contacto},

Para poder revisar la solicitud {ticket_id}, necesitamos algunos datos adicionales:

- Fecha y hora aproximada del problema.
- Mensaje de error, si aparece.
- Captura de pantalla, si es posible.
- Indicar si afecta a todos los usuarios o solo a uno.
- Confirmar si el problema continúa actualmente.

Con esa información podremos continuar el diagnóstico.

Un saludo,
Equipo Vigex""",
    },
    {
        "key": "analisis",
        "titulo": "Incidencia en análisis",
        "uso": "Informar de que el equipo Vigex está revisando el caso.",
        "texto": """Hola {contacto},

Estamos revisando la solicitud {ticket_id}.

El caso queda en análisis técnico. Estamos comprobando el estado del servicio afectado y revisando las evidencias disponibles.

Servicio afectado: {servicio}
Estado actual del ticket: {estado}

Te informaremos con el resultado o con el siguiente paso necesario.

Un saludo,
Equipo Vigex""",
    },
    {
        "key": "servicio_operativo",
        "titulo": "Servicio operativo",
        "uso": "Responder cuando el servicio funciona correctamente.",
        "texto": """Hola {contacto},

Hemos revisado el servicio indicado en la solicitud {ticket_id} y actualmente se encuentra operativo.

Las comprobaciones realizadas indican que no hay una caída activa del servicio.

Si el problema continúa desde vuestro equipo o red, indícanos por favor:

- Hora exacta del intento.
- Usuario afectado.
- Captura del error.
- Navegador utilizado.

Un saludo,
Equipo Vigex""",
    },
    {
        "key": "resuelto",
        "titulo": "Incidencia resuelta",
        "uso": "Comunicar el cierre correcto de una incidencia.",
        "texto": """Hola {contacto},

La solicitud {ticket_id} ha quedado resuelta.

Hemos aplicado las acciones necesarias y verificado que el servicio vuelve a funcionar correctamente.

Resumen:

- Servicio revisado: {servicio}
- Estado final: {estado}
- Validación final realizada.

Damos el ticket por cerrado. Si vuelve a ocurrir, puedes responder a este mismo hilo o abrir una nueva solicitud.

Un saludo,
Equipo Vigex""",
    },
    {
        "key": "restauracion",
        "titulo": "Restauración de backup",
        "uso": "Pedir confirmación antes de restaurar datos.",
        "texto": """Hola {contacto},

Hemos recibido la solicitud {ticket_id} relacionada con restauración.

Antes de ejecutar la restauración necesitamos confirmar:

- Base de datos o servicio afectado.
- Fecha aproximada a la que se desea restaurar.
- Motivo de la restauración.
- Confirmación de que entendéis que puede sobrescribir datos actuales.

No ejecutaremos la restauración hasta recibir confirmación.

Un saludo,
Equipo Vigex""",
    },
    {
        "key": "mantenimiento",
        "titulo": "Mantenimiento programado",
        "uso": "Avisar o coordinar una intervención planificada.",
        "texto": """Hola {contacto},

La solicitud {ticket_id} requiere una intervención planificada.

Para evitar impacto en el servicio, proponemos realizarla en una ventana de mantenimiento acordada.

Servicio afectado: {servicio}

Por favor, indícanos qué horario sería más adecuado para vuestra empresa.

Un saludo,
Equipo Vigex""",
    },
    {
        "key": "whatsapp",
        "titulo": "Respuesta breve WhatsApp",
        "uso": "Confirmación corta para canal rápido.",
        "texto": """Hola {contacto}, hemos recibido tu aviso.

Referencia interna: {ticket_id}

Lo registramos internamente y lo revisamos. Te informaremos por este canal o por email cuando tengamos una actualización.""",
    },
]


def get_support_response_templates():
    return SUPPORT_RESPONSE_TEMPLATES


def get_support_response_template(template_key):
    template_key = (template_key or "").strip()

    for template in SUPPORT_RESPONSE_TEMPLATES:
        if template["key"] == template_key:
            return template

    return None


def render_support_response_template(ticket, template_key):
    template = get_support_response_template(template_key)

    if not template:
        return None, ""

    values = {
        "ticket_id": ticket.get("id", ""),
        "cliente": ticket.get("cliente", ""),
        "contacto": ticket.get("contacto", ""),
        "email": ticket.get("email", ""),
        "servicio": ticket.get("servicio", ""),
        "tipo": ticket.get("tipo", ""),
        "prioridad": ticket.get("prioridad", ""),
        "estado": ticket.get("estado", ""),
    }

    try:
        text = template["texto"].format(**values)
    except Exception:
        text = template["texto"]

    return template, text

# =====================
# R-049F - RESUMEN JIRA ZAMMAD
# =====================

def format_support_history_for_external_summary(history):
    if not history:
        return "Sin historial interno registrado."

    lines = []

    for item in reversed(history):
        fecha = item.get("fecha", "")
        usuario = item.get("usuario", "")
        accion = item.get("accion", "")
        valor_anterior = item.get("valor_anterior", "") or "-"
        valor_nuevo = item.get("valor_nuevo", "") or "-"
        detalle = item.get("detalle", "") or ""

        line = f"- {fecha} | {usuario} | {accion}: {valor_anterior} -> {valor_nuevo}"
        if detalle:
            line += f" | {detalle}"

        lines.append(line)

    return "\n".join(lines)


def render_support_external_summary(ticket, history):
    history_text = format_support_history_for_external_summary(history)

    return f"""# Resumen técnico de ticket Vigex

## Identificación

Ticket interno: {ticket.get("id", "")}
Estado: {ticket.get("estado", "")}
Prioridad: {ticket.get("prioridad", "")}
Tipo: {ticket.get("tipo", "")}
Servicio afectado: {ticket.get("servicio", "")}

## Cliente

Empresa: {ticket.get("cliente", "")}
Contacto: {ticket.get("contacto", "")}
Email: {ticket.get("email", "")}
Teléfono: {ticket.get("telefono", "") or "-"}

## Fechas

Fecha apertura: {ticket.get("fecha_apertura", "")}
Última actualización: {ticket.get("fecha_actualizacion", "")}

## Canal y origen

Canal: {ticket.get("canal", "")}
Creado por: {ticket.get("creado_por", "")}
Origen: {ticket.get("origen", "")}

## Descripción

{ticket.get("descripcion", "")}

## Evidencia

{ticket.get("evidencia", "") or "Sin evidencia registrada."}

## Historial interno

{history_text}

## Próximo paso recomendado

Revisar el caso, confirmar diagnóstico y actualizar el estado del ticket en Vigex.

## Nota

Este resumen se ha generado desde Vigex para copiarlo en Jira, Zammad u otra herramienta interna de soporte.
"""


# =====================
# R-061 / Ruta 7.6 — Configuración desde el panel
# =====================
# Permite editar umbrales y parámetros operativos sin tocar config.env
# manualmente. Los cambios se aplican en memoria de forma inmediata y se
# persisten en config.env para sobrevivir reinicios.

# Metadatos de cada parámetro editable (label, tipo, rango, descripción)
_CONFIG_EDITABLE = {
    "NOTIF_DISK_THRESHOLD": {
        "label": "Umbral de disco (%)",
        "tipo": "int",
        "min": 50,
        "max": 99,
        "desc": "Porcentaje de uso de disco a partir del cual se envía alerta proactiva.",
        "unidad": "%",
    },
    "NOTIF_CHECK_INTERVAL": {
        "label": "Intervalo entre checks automáticos",
        "tipo": "int",
        "min": 60,
        "max": 86400,
        "desc": "Frecuencia en segundos con la que el panel comprueba disco, backup y servicios.",
        "unidad": "seg",
    },
    "NOTIF_COOLDOWN": {
        "label": "Silencio entre alertas iguales",
        "tipo": "int",
        "min": 300,
        "max": 86400,
        "desc": "Tiempo mínimo en segundos entre dos alertas del mismo tipo para evitar spam.",
        "unidad": "seg",
    },
}


def _update_config_env(updates: dict) -> bool:
    """Actualiza claves específicas en config.env preservando comentarios y orden.
    Escrita de forma atómica: fichero temporal + rename.
    Devuelve True si la escritura fue exitosa.
    """
    import shutil

    config_path = Path("config.env")
    if not config_path.exists():
        return False

    try:
        lines = config_path.read_text(encoding="utf-8").splitlines(keepends=True)
        pendientes = set(updates.keys())
        nuevas_lineas = []

        for linea in lines:
            stripped = linea.strip()
            reemplazada = False
            for key in list(pendientes):
                # Coincide si la línea empieza exactamente con KEY= (sin espacios intermedios)
                if stripped.startswith(f"{key}=") or stripped == key:
                    nuevas_lineas.append(f"{key}={updates[key]}\n")
                    pendientes.discard(key)
                    reemplazada = True
                    break
            if not reemplazada:
                nuevas_lineas.append(linea)

        # Claves no encontradas en el fichero: añadir al final
        for key in pendientes:
            nuevas_lineas.append(f"{key}={updates[key]}\n")

        # Escritura atómica
        tmp = config_path.with_suffix(".tmp")
        tmp.write_text("".join(nuevas_lineas), encoding="utf-8")
        shutil.move(str(tmp), str(config_path))
        return True
    except Exception:
        return False


@app.get("/configuracion")
def configuracion_panel(request: Request):
    """Página de configuración operativa del panel (solo admins). R-061"""
    if not is_admin(request):
        return permission_redirect("Solo el administrador puede acceder a la configuración del panel.")

    context = get_common_context(request)
    context["current_path"] = "/configuracion"
    context["config_actual"] = {
        "NOTIF_DISK_THRESHOLD": NOTIF_DISK_THRESHOLD,
        "NOTIF_CHECK_INTERVAL": NOTIF_CHECK_INTERVAL,
        "NOTIF_COOLDOWN": NOTIF_COOLDOWN,
    }
    context["config_meta"] = _CONFIG_EDITABLE
    context["notif_enabled"] = NOTIF_ENABLED
    context["smtp_host"]           = NOTIF_SMTP_HOST or ""
    context["smtp_port"]           = NOTIF_SMTP_PORT
    context["smtp_user"]           = NOTIF_SMTP_USER or ""
    context["smtp_pass_set"]       = bool(NOTIF_SMTP_PASS)   # no exponer la contraseña
    context["smtp_email_from"]     = NOTIF_EMAIL_FROM or ""
    context["smtp_email_to"]       = NOTIF_EMAIL_TO or ""
    context["telegram_ok"] = bool(os.getenv("TELEGRAM_BOT_TOKEN", "").strip())
    context["ssh_key"] = SSH_KEY_PATH
    context["ssh_timeout"] = SSH_TIMEOUT
    context["auto_logout_minutes"] = AUTO_LOGOUT_MINUTES
    return templates.TemplateResponse(request, "configuracion.html", context)


@app.post("/configuracion")
async def configuracion_panel_save(request: Request):
    """Guarda parámetros operativos editables en memoria y en config.env. R-061"""
    if not is_admin(request):
        return JSONResponse({"ok": False, "msg": "Acceso denegado."}, status_code=403)

    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"ok": False, "msg": "Datos no válidos."}, status_code=400)

    global NOTIF_DISK_THRESHOLD, NOTIF_CHECK_INTERVAL, NOTIF_COOLDOWN

    updates: dict[str, str] = {}
    errores: list[str] = []

    for key, meta in _CONFIG_EDITABLE.items():
        if key not in data:
            continue
        try:
            val = int(data[key])
        except (ValueError, TypeError):
            errores.append(f"'{meta['label']}': valor no es un número entero")
            continue

        if val < meta["min"] or val > meta["max"]:
            errores.append(
                f"'{meta['label']}': debe estar entre {meta['min']} y {meta['max']} {meta['unidad']}"
            )
            continue

        updates[key] = str(val)

    if errores:
        return JSONResponse(
            {"ok": False, "msg": "Errores de validación: " + "; ".join(errores)},
            status_code=400,
        )

    if not updates:
        return JSONResponse({"ok": False, "msg": "No se recibieron cambios."}, status_code=400)

    # Aplicar en memoria (efecto inmediato, sin reinicio)
    if "NOTIF_DISK_THRESHOLD" in updates:
        NOTIF_DISK_THRESHOLD = int(updates["NOTIF_DISK_THRESHOLD"])
    if "NOTIF_CHECK_INTERVAL" in updates:
        NOTIF_CHECK_INTERVAL = int(updates["NOTIF_CHECK_INTERVAL"])
    if "NOTIF_COOLDOWN" in updates:
        NOTIF_COOLDOWN = int(updates["NOTIF_COOLDOWN"])

    # Persistir en config.env para sobrevivir reinicios
    written = _update_config_env(updates)

    usuario = request.session.get("user", "anon")
    log_event(
        tipo="configuracion",
        resultado="OK",
        usuario=usuario,
        ip_origen=request.client.host if request.client else None,
        recurso="POST /configuracion",
        detalle=f"Claves actualizadas: {', '.join(updates.keys())}",
    )

    if written:
        msg = "Configuración guardada y activa. Los nuevos valores ya están en efecto."
    else:
        msg = "Valores aplicados en memoria. No se pudo escribir config.env (los cambios se perderán al reiniciar)."

    return JSONResponse({"ok": True, "msg": msg})


# ─────────────────────────────────────────────────────────────────────────────
# R-061-bis — Configuración SMTP desde el panel (sin editar config.env)
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/configuracion/smtp")
async def configuracion_smtp_save(request: Request):
    """Guarda la configuración SMTP en config.env y recarga las variables globales. R-061-bis"""
    if not is_admin(request):
        return JSONResponse({"ok": False, "msg": "Acceso denegado."}, status_code=403)

    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"ok": False, "msg": "Datos no válidos."}, status_code=400)

    global NOTIF_SMTP_HOST, NOTIF_SMTP_PORT, NOTIF_SMTP_USER, NOTIF_SMTP_PASS
    global NOTIF_EMAIL_FROM, NOTIF_EMAIL_TO

    host      = str(data.get("smtp_host", "")).strip()
    port_raw  = data.get("smtp_port", 587)
    user_smtp = str(data.get("smtp_user", "")).strip()
    password  = str(data.get("smtp_pass", "")).strip()
    email_from = str(data.get("email_from", "")).strip()
    email_to   = str(data.get("email_to", "")).strip()

    # Validar puerto
    try:
        port = int(port_raw)
        if port < 1 or port > 65535:
            raise ValueError
    except (ValueError, TypeError):
        return JSONResponse({"ok": False, "msg": "Puerto SMTP inválido (1–65535)."}, status_code=400)

    # Construir diccionario de cambios (no sobreescribir la contraseña si se envía vacía)
    updates: dict[str, str] = {
        "NOTIF_SMTP_HOST": host,
        "NOTIF_SMTP_PORT": str(port),
        "NOTIF_SMTP_USER": user_smtp,
        "NOTIF_EMAIL_FROM": email_from,
        "NOTIF_EMAIL_TO": email_to,
    }
    if password:
        updates["NOTIF_SMTP_PASS"] = password

    # Persistir en config.env
    written = _update_config_env(updates)

    # Recargar en memoria (efecto inmediato)
    NOTIF_SMTP_HOST  = host
    NOTIF_SMTP_PORT  = port
    NOTIF_SMTP_USER  = user_smtp
    NOTIF_EMAIL_FROM = email_from
    NOTIF_EMAIL_TO   = email_to
    if password:
        NOTIF_SMTP_PASS = password

    usuario = request.session.get("user", "anon")
    log_event(
        tipo="configuracion",
        resultado="OK",
        usuario=usuario,
        ip_origen=request.client.host if request.client else None,
        recurso="POST /configuracion/smtp",
        detalle=f"SMTP actualizado: host={host} puerto={port} usuario={user_smtp}",
    )

    if written:
        msg = "Configuración SMTP guardada. Activa para nuevos envíos."
    else:
        msg = "SMTP actualizado en memoria. No se pudo persistir en config.env."

    return JSONResponse({"ok": True, "msg": msg})


# ─────────────────────────────────────────────────────────────────────────────
# Guardar tiempo de auto-logout por inactividad (R-083-fix-9)
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/configuracion/auto-logout")
async def configuracion_auto_logout_save(request: Request):
    """Guarda el tiempo de auto-logout por inactividad en config.env. R-083-fix-9"""
    global AUTO_LOGOUT_MINUTES

    if not is_admin(request):
        return JSONResponse({"ok": False, "msg": "Sin permisos."}, status_code=403)

    try:
        data = await request.json()
        minutos = int(data.get("minutos", 60))
    except Exception:
        return JSONResponse({"ok": False, "msg": "Valor inválido."}, status_code=400)

    if minutos < 0 or minutos > 1440:
        return JSONResponse({"ok": False, "msg": "El valor debe estar entre 0 y 1440 minutos."}, status_code=400)

    AUTO_LOGOUT_MINUTES = minutos
    written = _update_config_env({"VIGEX_AUTO_LOGOUT_MINUTES": str(minutos)})

    ip = request.client.host if request.client else None
    usuario = request.session.get("user", "anon")
    log_event(
        tipo="CONFIGURACION",
        resultado="OK",
        usuario=usuario,
        ip_origen=ip,
        recurso="POST /configuracion/auto-logout",
        detalle=f"Auto-logout por inactividad: {minutos} min (0=desactivado)",
    )

    msg = f"Auto-logout configurado a {minutos} minuto(s)." if minutos > 0 else "Auto-logout desactivado."
    return JSONResponse({"ok": True, "msg": msg})


# =====================
# R-062 / Ruta 7.7 — Informes periódicos configurables
# =====================
# Genera y envía informes de estado (disco, backups, servicios, alertas)
# por email y/o Telegram, con frecuencia configurable desde el panel.

_REPORTS_CONFIG_PATH = Path("data/reports_config.json")
_REPORTS_LOCK        = threading.Lock()
_REPORTS_HIST_MAX    = 20

_FRECUENCIAS_SEG: dict[str, int] = {
    "diario":  86400,
    "semanal": 604800,
    "mensual": 2592000,
}

_SECCIONES_VALIDAS = {"backups", "disco", "servicios", "alertas"}

_REPORTS_CONFIG_DEFAULT: dict[str, Any] = {
    "enabled":      False,
    "frecuencia":   "semanal",
    "canal":        "email",
    "secciones":    ["backups", "disco", "servicios", "alertas"],
    "ultimo_envio": None,
    "historial":    [],
}


def _load_reports_config() -> dict[str, Any]:
    """Carga la configuración de informes desde JSON; devuelve defaults si no existe."""
    with _REPORTS_LOCK:
        if _REPORTS_CONFIG_PATH.exists():
            try:
                data = json.loads(_REPORTS_CONFIG_PATH.read_text(encoding="utf-8"))
                cfg = dict(_REPORTS_CONFIG_DEFAULT)
                cfg.update(data)
                return cfg
            except Exception:
                pass
        return dict(_REPORTS_CONFIG_DEFAULT)


def _save_reports_config(cfg: dict[str, Any]) -> None:
    """Persiste la configuración de informes en JSON."""
    with _REPORTS_LOCK:
        _REPORTS_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        _REPORTS_CONFIG_PATH.write_text(
            json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8"
        )


def _recopilar_datos_informe(secciones: list[str]) -> dict[str, Any]:
    """Recopila datos de cada sección activa para el informe."""
    datos: dict[str, Any] = {
        "fecha":              datetime.now().strftime("%Y-%m-%d %H:%M"),
        "servidor_backups":   SERVIDOR_BACKUPS,
        "servidor_servicios": SERVIDOR_SERVICIOS,
    }

    if "disco" in secciones:
        try:
            r = ssh_run(SERVIDOR_BACKUPS, "df", ["-h", "/"])
            info = _parse_df_output(r["stdout"]) if r.get("ok") else {}
            datos["disco"] = info if info.get("available") else None
        except Exception:
            datos["disco"] = None

    if "backups" in secciones:
        try:
            datos["backups"] = cargar_historial_backups(limit=5) or []
        except Exception:
            datos["backups"] = []

    if "servicios" in secciones:
        try:
            result = ssh_run(SERVIDOR_SERVICIOS, SCRIPT_SERVICIOS, ["list"])
            lista: list[dict[str, str]] = []
            for linea in result.get("text", "").split("\n"):
                if "|" in linea:
                    nombre, estado = linea.split("|", 1)
                    lista.append({"nombre": nombre.strip(), "estado": estado.strip()})
            datos["servicios"] = lista
        except Exception:
            datos["servicios"] = []

    if "alertas" in secciones:
        datos["alertas"] = list(_proactivo_estado.get("alert_log", []))[-10:]

    return datos


def _informe_html(datos: dict[str, Any]) -> str:
    """Genera el HTML del informe periódico."""
    bloques = ""

    # Disco
    if "disco" in datos:
        disco = datos["disco"]
        if disco:
            pct   = disco.get("percent", 0)
            color = "#b91c1c" if pct >= NOTIF_DISK_THRESHOLD else "#065f46"
            bloques += (
                f"<h2 style='color:#1e1b4b;font-size:15px;margin:20px 0 6px;'>💾 Disco</h2>"
                f"<p style='color:#374151;font-size:14px;margin:0;'>"
                f"Uso: <strong style='color:{color};'>{pct}%</strong>"
                f" ({disco.get('used','?')} de {disco.get('total','?')})"
                f" — Disponible: {disco.get('available','?')}</p>"
            )
        else:
            bloques += "<h2 style='color:#1e1b4b;font-size:15px;margin:20px 0 6px;'>💾 Disco</h2><p style='color:#9ca3af;font-size:14px;'>Sin datos (servidor no accesible).</p>"

    # Backups
    if "backups" in datos:
        backups = datos["backups"]
        if backups:
            filas = ""
            for b in backups[:5]:
                s     = (b.get("status") or b.get("result") or "OK").upper()
                color = "#b91c1c" if s not in ("OK", "SUCCESS", "0", "") else "#065f46"
                filas += (
                    f"<tr><td style='padding:4px 8px;font-size:13px;'>{(b.get('date',''))[:16]}</td>"
                    f"<td style='padding:4px 8px;font-size:13px;'>{b.get('tipo_label') or b.get('type','—')}</td>"
                    f"<td style='padding:4px 8px;font-size:13px;color:{color};font-weight:700;'>{s}</td></tr>"
                )
            bloques += (
                f"<h2 style='color:#1e1b4b;font-size:15px;margin:20px 0 6px;'>📦 Últimas copias de seguridad</h2>"
                f"<table style='border-collapse:collapse;width:100%;'>"
                f"<tr style='background:#f3f4f6;'>"
                f"<th style='padding:4px 8px;font-size:12px;text-align:left;'>Fecha</th>"
                f"<th style='padding:4px 8px;font-size:12px;text-align:left;'>Tipo</th>"
                f"<th style='padding:4px 8px;font-size:12px;text-align:left;'>Estado</th></tr>"
                f"{filas}</table>"
            )
        else:
            bloques += "<h2 style='color:#1e1b4b;font-size:15px;margin:20px 0 6px;'>📦 Copias de seguridad</h2><p style='color:#9ca3af;font-size:14px;'>Sin historial disponible.</p>"

    # Servicios
    if "servicios" in datos:
        servicios = datos["servicios"]
        total   = len(servicios)
        activos = sum(1 for s in servicios if s["estado"] == "active")
        color   = "#b91c1c" if activos < total and total > 0 else "#065f46"
        bloques += (
            f"<h2 style='color:#1e1b4b;font-size:15px;margin:20px 0 6px;'>⚙️ Servicios</h2>"
            f"<p style='color:{color};font-size:14px;font-weight:700;margin:0 0 4px;'>"
            f"{activos}/{total} activos</p>"
        )
        if total > 0 and activos < total:
            inact = ", ".join(s["nombre"] for s in servicios if s["estado"] != "active")
            bloques += f"<p style='color:#b91c1c;font-size:13px;margin:0;'>Inactivos: {inact}</p>"
        elif total == 0:
            bloques += "<p style='color:#9ca3af;font-size:14px;'>Sin datos (servidor no accesible).</p>"

    # Alertas
    if "alertas" in datos:
        alertas = datos["alertas"]
        if alertas:
            filas = "".join(
                f"<tr><td style='padding:4px 8px;font-size:13px;'>{a.get('ts','')}</td>"
                f"<td style='padding:4px 8px;font-size:13px;'>{a.get('tipo','—')}</td></tr>"
                for a in reversed(alertas[-5:])
            )
            bloques += (
                f"<h2 style='color:#1e1b4b;font-size:15px;margin:20px 0 6px;'>🔔 Últimas alertas enviadas</h2>"
                f"<table style='border-collapse:collapse;width:100%;'>"
                f"<tr style='background:#f3f4f6;'>"
                f"<th style='padding:4px 8px;font-size:12px;text-align:left;'>Fecha</th>"
                f"<th style='padding:4px 8px;font-size:12px;text-align:left;'>Tipo</th></tr>"
                f"{filas}</table>"
            )
        else:
            bloques += "<h2 style='color:#1e1b4b;font-size:15px;margin:20px 0 6px;'>🔔 Alertas</h2><p style='color:#9ca3af;font-size:14px;'>Sin alertas registradas en este período.</p>"

    return f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8">
<style>
  body{{font-family:-apple-system,sans-serif;background:#f3f4f6;margin:0;padding:24px;}}
  .card{{background:#fff;border-radius:14px;padding:28px 32px;max-width:600px;margin:0 auto;}}
  .hdr{{border-bottom:2px solid #4f46e5;padding-bottom:12px;margin-bottom:4px;}}
  h1{{color:#1e1b4b;font-size:20px;margin:0 0 4px;}}
  .sub{{color:#6b7280;font-size:13px;}}
  .ftr{{color:#9ca3af;font-size:11px;margin-top:20px;border-top:1px solid #e5e7eb;padding-top:12px;}}
</style></head>
<body><div class="card">
  <div class="hdr">
    <h1>📊 Informe de estado Vigex</h1>
    <span class="sub">Generado: {datos['fecha']} — Servidor: {datos['servidor_backups']}</span>
  </div>
  {bloques}
  <div class="ftr">Vigex · Informe periódico automático · No responder a este correo.</div>
</div></body></html>"""


def _informe_telegram_texto(datos: dict[str, Any]) -> str:
    """Genera el texto del informe para Telegram."""
    lineas = [f"📊 <b>Informe Vigex — {datos['fecha']}</b>\n"]

    if "disco" in datos:
        disco = datos["disco"]
        if disco:
            pct   = disco.get("percent", 0)
            emoji = "🔴" if pct >= NOTIF_DISK_THRESHOLD else "🟢"
            lineas.append(f"{emoji} <b>Disco:</b> {pct}% ({disco.get('used','?')} / {disco.get('total','?')})")
        else:
            lineas.append("⚪ <b>Disco:</b> sin datos")

    if "backups" in datos:
        backups = datos["backups"]
        if backups:
            last  = backups[0]
            s     = (last.get("status") or "OK").upper()
            emoji = "🟢" if s in ("OK", "SUCCESS", "0", "") else "🔴"
            lineas.append(f"{emoji} <b>Último backup:</b> {s} · {(last.get('date',''))[:16]}")
        else:
            lineas.append("⚪ <b>Backups:</b> sin historial")

    if "servicios" in datos:
        servicios = datos["servicios"]
        total   = len(servicios)
        activos = sum(1 for s in servicios if s["estado"] == "active")
        emoji   = "🟢" if activos == total and total > 0 else ("⚪" if total == 0 else "🔴")
        lineas.append(f"{emoji} <b>Servicios:</b> {activos}/{total} activos")

    if "alertas" in datos:
        lineas.append(f"🔔 <b>Alertas recientes:</b> {len(datos['alertas'])}")

    return "\n".join(lineas)


def _enviar_informe(cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    """Genera y envía el informe por el canal configurado. Actualiza historial."""
    if cfg is None:
        cfg = _load_reports_config()

    secciones = cfg.get("secciones") or list(_SECCIONES_VALIDAS)
    canal     = cfg.get("canal", "email")

    datos    = _recopilar_datos_informe(secciones)
    html_str = _informe_html(datos)
    tg_text  = _informe_telegram_texto(datos)

    ok_email = False
    ok_tg    = False

    if canal in ("email", "ambos"):
        ok_email = _send_email_alert("Informe de estado del servidor", html_str)

    if canal in ("telegram", "ambos"):
        default = get_default_recipient("telegram")
        if default:
            r    = send_telegram_message(tg_text, default["destination"])
            ok_tg = bool(r.get("ok"))

    ok          = ok_email or ok_tg
    canales_ok  = (["email"] if ok_email else []) + (["telegram"] if ok_tg else [])
    ts_ahora    = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cfg["ultimo_envio"] = ts_ahora
    historial = list(cfg.get("historial") or [])
    historial.append({"ts": ts_ahora, "ok": ok, "canal": ", ".join(canales_ok) or canal})
    cfg["historial"] = historial[-_REPORTS_HIST_MAX:]
    _save_reports_config(cfg)

    return {
        "ok":    ok,
        "msg":   f"Enviado por {', '.join(canales_ok)}" if ok
                 else "No se pudo enviar (verifica configuración de email/Telegram)",
        "canal": canales_ok,
    }


def _reports_worker() -> None:
    """Hilo daemon que comprueba si corresponde enviar un informe periódico."""
    _time_mod.sleep(120)   # espera inicial al arranque
    while True:
        try:
            cfg = _load_reports_config()
            if cfg.get("enabled"):
                frecuencia = cfg.get("frecuencia", "semanal")
                intervalo  = _FRECUENCIAS_SEG.get(frecuencia, 604800)
                ultimo     = cfg.get("ultimo_envio")
                if ultimo:
                    try:
                        ultimo_ts = datetime.strptime(ultimo, "%Y-%m-%d %H:%M:%S").timestamp()
                    except Exception:
                        ultimo_ts = 0.0
                    elapsed = _time_mod.time() - ultimo_ts
                else:
                    elapsed = float("inf")

                if elapsed >= intervalo:
                    _enviar_informe(cfg)
        except Exception:
            pass
        _time_mod.sleep(1800)   # comprueba cada 30 min


@app.get("/informes")
def informes_page(request: Request):
    """Página de informes periódicos configurables (solo admins). R-062"""
    if not is_admin(request):
        return permission_redirect("Solo el administrador puede acceder a los informes periódicos.")

    cfg = _load_reports_config()
    ctx = get_common_context(request)
    ctx["current_path"]      = "/informes"
    ctx["cfg"]               = cfg
    ctx["telegram_ok"]       = bool(os.getenv("TELEGRAM_BOT_TOKEN", "").strip())
    ctx["email_ok"]          = bool(NOTIF_EMAIL_TO and NOTIF_SMTP_HOST)
    ctx["secciones_validas"] = sorted(_SECCIONES_VALIDAS)

    # Calcular tiempo hasta el próximo envío
    proximo_en = "—"
    if cfg.get("enabled") and cfg.get("ultimo_envio"):
        try:
            intervalo  = _FRECUENCIAS_SEG.get(cfg.get("frecuencia", "semanal"), 604800)
            ultimo_ts  = datetime.strptime(cfg["ultimo_envio"], "%Y-%m-%d %H:%M:%S").timestamp()
            restante   = max(0, intervalo - (_time_mod.time() - ultimo_ts))
            if restante > 3600:
                proximo_en = f"{int(restante // 3600)} h"
            elif restante > 60:
                proximo_en = f"{int(restante // 60)} min"
            else:
                proximo_en = "menos de 1 min"
        except Exception:
            pass
    ctx["proximo_en"] = proximo_en

    return templates.TemplateResponse(request, "informes.html", ctx)


@app.post("/informes/config")
async def informes_config_save(request: Request):
    """Guarda la configuración de informes periódicos. R-062"""
    if not is_admin(request):
        return JSONResponse({"ok": False, "msg": "Acceso denegado."}, status_code=403)

    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"ok": False, "msg": "Datos no válidos."}, status_code=400)

    cfg = _load_reports_config()
    cfg["enabled"] = bool(data.get("enabled", False))

    frecuencia = str(data.get("frecuencia", "semanal"))
    if frecuencia not in _FRECUENCIAS_SEG:
        return JSONResponse({"ok": False, "msg": "Frecuencia no válida."}, status_code=400)
    cfg["frecuencia"] = frecuencia

    canal = str(data.get("canal", "email"))
    if canal not in ("email", "telegram", "ambos"):
        return JSONResponse({"ok": False, "msg": "Canal no válido."}, status_code=400)
    cfg["canal"] = canal

    secciones = [s for s in (data.get("secciones") or []) if s in _SECCIONES_VALIDAS]
    cfg["secciones"] = secciones if secciones else list(_SECCIONES_VALIDAS)

    _save_reports_config(cfg)

    usuario = request.session.get("user", "anon")
    log_event(
        tipo="informes",
        resultado="OK",
        usuario=usuario,
        ip_origen=request.client.host if request.client else None,
        recurso="POST /informes/config",
        detalle=f"enabled={cfg['enabled']} freq={frecuencia} canal={canal}",
    )
    return JSONResponse({"ok": True, "msg": "Configuración de informes guardada."})


@app.post("/informes/enviar")
def informes_enviar(request: Request):
    """Lanza un envío de informe manual inmediato (solo admins). R-062"""
    if not is_admin(request):
        return JSONResponse({"ok": False, "msg": "Acceso denegado."}, status_code=403)
    try:
        result = _enviar_informe()
        usuario = request.session.get("user", "anon")
        log_event(
            tipo="informes",
            resultado="OK" if result["ok"] else "ERROR",
            usuario=usuario,
            ip_origen=request.client.host if request.client else None,
            recurso="POST /informes/enviar",
            detalle=result["msg"],
        )
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"ok": False, "msg": str(e)}, status_code=500)


# =====================
# R-063 / Ruta 7.8 — Reporte de bugs desde el panel
# =====================
# Botón "Reportar problema" accesible desde cualquier página del panel.
# Crea un ticket de soporte con contexto del sistema adjunto automáticamente.

_REPORT_TIPOS_MAP = {
    # tipos propios — aparecen en sección "Reportes", NO en tickets de soporte
    "bug":        ("Bug",        "Alta",  "Panel Vigex"),
    "sugerencia": ("Sugerencia", "Baja",  "Panel Vigex"),
    "pregunta":   ("Pregunta",   "Media", "Panel Vigex"),
}


@app.post("/reportar-problema")
async def reportar_problema(request: Request):
    """Crea un ticket de soporte con contexto del sistema. R-063
    Accesible a cualquier usuario autenticado (no solo admins).
    """
    if not request.session.get("user"):
        return JSONResponse({"ok": False, "msg": "Sesión no activa."}, status_code=401)

    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"ok": False, "msg": "Datos no válidos."}, status_code=400)

    tipo_raw   = str(data.get("tipo", "bug")).lower().strip()
    descripcion = str(data.get("descripcion", "")).strip()
    url_pagina  = str(data.get("url_pagina", "—")).strip()

    if not descripcion:
        return JSONResponse({"ok": False, "msg": "La descripción no puede estar vacía."}, status_code=400)

    if len(descripcion) > 2000:
        return JSONResponse({"ok": False, "msg": "Descripción demasiado larga (máx. 2000 caracteres)."}, status_code=400)

    tipo_ticket, prioridad, servicio = _REPORT_TIPOS_MAP.get(tipo_raw, ("Incidencia", "Media", "Panel Vigex"))

    usuario   = request.session.get("user", "anon")
    ahora     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Contexto del sistema recogido en el momento del reporte
    ctx_lineas = [
        f"Página: {url_pagina}",
        f"Usuario: {usuario}",
        f"Fecha: {ahora}",
    ]
    # Disco (si hay datos en memoria de la última comprobación)
    disco_check = _proactivo_estado.get("checks", {}).get("disk", {})
    if disco_check.get("last_value"):
        ctx_lineas.append(f"Disco: {disco_check['last_value']}")
    # Alertas recientes
    n_alertas = len(_proactivo_estado.get("alert_log", []))
    ctx_lineas.append(f"Alertas proactivas en sesión: {n_alertas}")

    descripcion_completa = (
        f"[Reporte enviado desde el panel — {tipo_ticket}]\n\n"
        f"{descripcion}\n\n"
        f"--- Contexto del sistema ---\n"
        + "\n".join(ctx_lineas)
    )

    ticket_id = next_support_ticket_id()
    ticket = {
        "id":            ticket_id,
        "fecha_apertura": ahora,
        "cliente":        "Uso interno Vigex",
        "contacto":       usuario,
        "email":          "",
        "telefono":       "",
        "canal":          "Reporte de panel",
        "tipo":           tipo_ticket,
        "prioridad":      prioridad,
        "servicio":       servicio,
        "descripcion":    descripcion_completa,
        "evidencia":      "",
        "estado":         "Abierto",
        "creado_por":     usuario,
        "origen":         "bug_report",
    }

    try:
        save_support_ticket(ticket)
    except Exception as e:
        return JSONResponse({"ok": False, "msg": f"Error al crear el ticket: {e}"}, status_code=500)

    # Enviar a Vigex Central (si está habilitado) — R-083-fix-2
    _central_result = send_support_ticket_to_central(ticket)
    if not _central_result.get("sent") and not _central_result.get("skipped"):
        log_event(
            tipo="bug_report",
            resultado="WARN",
            usuario=usuario,
            ip_origen=request.client.host if request.client else None,
            recurso="POST /reportar-problema",
            detalle=f"ticket={ticket_id} — fallo push Central: {_central_result.get('detail', '')}",
        )

    # Notificar por email a soporte@vigex.es (silencioso si SMTP no configurado)
    _send_email_bugreport(ticket_id, tipo_raw, descripcion_completa, usuario)

    log_event(
        tipo="bug_report",
        resultado="OK",
        usuario=usuario,
        ip_origen=request.client.host if request.client else None,
        recurso="POST /reportar-problema",
        detalle=f"ticket={ticket_id} tipo={tipo_raw} central_sent={_central_result.get('sent', False)}",
    )

    return JSONResponse({
        "ok":        True,
        "ticket_id": ticket_id,
        "msg":       f"Reporte enviado. Referencia: {ticket_id}",
    })


# =====================
# R-064 / Ruta 7.9 — Integridad y consistencia de copias
# =====================
# Comprueba la salud de las copias de seguridad y de las tablas de la BD:
#  - Analiza history.tsv: edad, estado OK/ERROR, presencia de SHA256
#  - Lee checksums.sha256 para contar cuántos ficheros tienen checksum
#  - SHOW TABLE STATUS sobre la BD de logs para detectar posibles corrupciones
# Todo sin nuevos comandos SSH: reutiliza cat (allowlist ampliada) y pymysql.

def _extraer_sha256_de_notas(notas: str) -> str | None:
    """Extrae sha256=XXXX del campo de notas de history.tsv."""
    for parte in notas.split(";"):
        if parte.startswith("sha256="):
            valor = parte[7:].strip()
            return valor if len(valor) == 64 else None
    return None


def _extraer_size_de_notas(notas: str) -> int | None:
    """Extrae size=NNNN (bytes) del campo de notas de history.tsv."""
    for parte in notas.split(";"):
        if parte.startswith("size="):
            try:
                return int(parte[5:])
            except ValueError:
                return None
    return None


def _analizar_salud_copias() -> dict[str, Any]:
    """Recopila todos los indicadores de salud de copias y BD. R-064"""
    ahora = datetime.now()
    resultado: dict[str, Any] = {
        "ts":               ahora.strftime("%Y-%m-%d %H:%M:%S"),
        "backups":          [],
        "checksums_total":  0,
        "checksums_ok":     0,
        "db_tables":        [],
        "db_error":         None,
        "ssh_error":        None,
        "resumen":          {},
    }

    # ── 1. Historial de copias ─────────────────────────────────────────────
    try:
        historia = cargar_historial_backups(limit=30)
        filas: list[dict[str, Any]] = []
        sha_presentes = 0
        errores = 0
        ultima_fecha: str | None = None

        for item in historia:
            estado = (item.get("status") or item.get("result") or "OK").upper()
            ok     = estado in ("OK", "SUCCESS", "0", "")
            notas  = item.get("notes", "") or ""
            sha    = _extraer_sha256_de_notas(notas)
            size_b = _extraer_size_de_notas(notas)
            size_s = ""
            if size_b is not None:
                if size_b >= 1_048_576:
                    size_s = f"{size_b / 1_048_576:.1f} MB"
                elif size_b >= 1024:
                    size_s = f"{size_b / 1024:.0f} KB"
                else:
                    size_s = f"{size_b} B"
            if ok:
                if sha:
                    sha_presentes += 1
            else:
                errores += 1
            fecha = item.get("date") or item.get("start_time") or ""
            if fecha and not ultima_fecha:
                ultima_fecha = fecha[:16]

            filas.append({
                "id":        item.get("id", "—"),
                "fecha":     fecha[:16] if fecha else "—",
                "tipo":      item.get("tipo_label", item.get("type", "—")),
                "db":        item.get("db", "—"),
                "estado":    estado if ok else estado,
                "ok":        ok,
                "sha_ok":    bool(sha),
                "sha_corto": sha[:8] + "…" if sha else "—",
                "size":      size_s or "—",
            })

        resultado["backups"]        = filas
        resultado["checksums_ok"]   = sha_presentes
        resultado["checksums_total"] = len(filas)
        resultado["ultima_fecha"]   = ultima_fecha

        # Resumen de salud
        total = len(filas)
        sin_sha = total - sha_presentes
        resultado["resumen"] = {
            "total":     total,
            "errores":   errores,
            "sin_sha":   sin_sha,
            "ultima":    ultima_fecha,
        }
    except Exception as e:
        resultado["ssh_error"] = str(e)

    # ── 2. Checksums.sha256 (total de ficheros con checksum registrado) ────
    try:
        r_cs = ssh_run(SERVIDOR_BACKUPS, "cat", ["/home/vigex/backups/.vigex/checksums.sha256"])
        if r_cs.get("ok") and r_cs.get("stdout", "").strip():
            lineas_cs = [l for l in r_cs["stdout"].splitlines() if l.strip() and not l.startswith("#")]
            resultado["checksums_total_archivo"] = len(lineas_cs)
        else:
            resultado["checksums_total_archivo"] = 0
    except Exception:
        resultado["checksums_total_archivo"] = None

    # ── 3. Integridad de tablas de la BD de logs (pymysql) ─────────────────
    try:
        conn = pymysql.connect(
            host=LOGS_DB_HOST,
            user=LOGS_DB_USER,
            password=LOGS_DB_PASS,
            database=LOGS_DB_NAME,
            connect_timeout=4,
            cursorclass=pymysql.cursors.DictCursor,
        )
        with conn.cursor() as cur:
            cur.execute("SHOW TABLE STATUS")
            tablas = cur.fetchall()
        conn.close()
        resultado["db_tables"] = [
            {
                "nombre":     t.get("Name", "?"),
                "filas":      t.get("Rows", 0),
                "size_mb":    round((int(t.get("Data_length") or 0) + int(t.get("Index_length") or 0)) / 1_048_576, 2),
                "comentario": t.get("Comment", "") or "",
                "ok":         (t.get("Comment") or "") not in ("crashed", "repair required", "repair recommended"),
            }
            for t in tablas
        ]
    except Exception as e:
        resultado["db_error"] = str(e)

    return resultado


@app.get("/copias/salud")
def copias_salud_page(request: Request):
    """Página de integridad y salud de copias de seguridad. R-064"""
    if not has_permission(request, "backups"):
        return permission_redirect()

    ctx = get_common_context(request)
    ctx["current_path"] = "/copias/salud"
    ctx["datos"]        = _analizar_salud_copias()
    return templates.TemplateResponse(request, "copias_salud.html", ctx)


@app.get("/api/copias/salud")
def copias_salud_api(request: Request):
    """API JSON de salud de copias (para refresco asíncrono). R-064"""
    if not has_permission(request, "backups"):
        return JSONResponse({"error": "sin permiso"}, status_code=403)
    return JSONResponse(_analizar_salud_copias())


# =============================================================================
# R-070 / Ruta 8.6 — FAQ / IA de triage
# R-085 / Ruta 12.1 — IA básica mejorada: más entradas, sinónimos, puntuación mejorada
# =============================================================================

# Mapa de sinónimos: cada clave se normaliza a su forma canónica antes de puntuar.
_FAQ_SINONIMOS: dict[str, str] = {
    # copias/backups
    "backups": "backup", "copias": "backup", "copia": "backup", "respaldo": "backup",
    "respaldos": "backup", "bkp": "backup",
    # fallos
    "falló": "fallo", "fallado": "fallo", "falla": "fallo", "fallas": "fallo",
    "error": "fallo", "errores": "fallo",
    # disco
    "almacenamiento": "disco", "espacio": "disco", "partición": "disco", "particion": "disco",
    "volumen": "disco",
    # servicios
    "servicio": "servicio", "servicios": "servicio", "proceso": "servicio",
    "demonio": "servicio", "daemon": "servicio",
    # contraseña
    "password": "contraseña", "clave": "contraseña", "credencial": "contraseña",
    "credenciales": "contraseña", "acceso": "contraseña",
    # actualizar
    "actualización": "actualizar", "actualizacion": "actualizar",
    "update": "actualizar", "upgrade": "actualizar", "versión": "actualizar",
    "version": "actualizar",
    # alertas/notificaciones
    "notificación": "alerta", "notificacion": "alerta", "notificaciones": "alerta",
    "aviso": "alerta", "avisos": "alerta",
    # restaurar
    "restore": "restaurar", "recuperar": "restaurar", "restablecer": "restaurar",
    "recuperación": "restaurar", "recuperacion": "restaurar",
    # conexión SSH
    "conexión": "conexion", "conectar": "conexion", "conectarse": "conexion",
    # log/logs
    "logs": "log", "registro": "log", "registros": "log", "journalctl": "log",
    # monitoreo
    "monitor": "monitoreo", "monitoring": "monitoreo", "métricas": "monitoreo",
    "metricas": "monitoreo",
    # HTTPS / certificado
    "tls": "certificado", "ssl": "certificado", "https": "certificado",
    "cert": "certificado",
}

# Palabras vacías que no aportan al score
_FAQ_STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del", "al",
    "en", "con", "por", "para", "que", "qué", "cómo", "como", "hay", "no",
    "si", "se", "me", "te", "le", "es", "son", "está", "estan", "están",
    "a", "y", "o", "e", "i", "u", "mi", "su", "tu", "sus",
}


def _normalizar_palabras(texto: str) -> list[str]:
    """Tokeniza, elimina stopwords y aplica sinónimos."""
    palabras = texto.lower().strip().split()
    resultado = []
    for p in palabras:
        p = p.strip("¿?¡!.,;:()")
        if not p or p in _FAQ_STOPWORDS:
            continue
        p = _FAQ_SINONIMOS.get(p, p)
        resultado.append(p)
    return resultado


_FAQ_ENTRIES: list[dict] = [
    {
        "id": (
            "vigex-que-es\n"
        ),
        "pregunta": (
            "¿Qué es Vigex y para qué sirve?\n"
        ),
        "respuesta": (
            "Vigex es un **panel de gestión de servidores Linux** diseñado para pequeñas y medianas empresas (PyMEs). Es una solución auto-hospedada (self-hosted) que centraliza en una única interfaz web todas las tareas críticas: copias de seguridad, restauración, gestión de servicios systemd, logs, alertas, monitoreo y soporte técnico con tickets. No necesitas contratar servicios en la nube: Vigex se instala en tus propios servidores y tú mantienes el control total de tus datos. Está desarrollado en Python con FastAPI, servido con Uvicorn y expuesto a través de un proxy nginx con HTTPS. El panel es accesible desde cualquier navegador moderno.\n"
        ),
        "palabras_clave": ["vigex", "que es", "para que", "panel", "gestión", "servidores", "pyme", "producto"],
    },
    {
        "id": (
            "vigex-a-quien-va-dirigido\n"
        ),
        "pregunta": (
            "¿A quién va dirigido Vigex? ¿Qué tipo de empresa lo usa?\n"
        ),
        "respuesta": (
            "Vigex está diseñado específicamente para **PyMEs** que tienen uno o varios servidores Linux propios o en VPS y necesitan gestionarlos de forma centralizada sin depender de un equipo técnico grande. Es ideal para: empresas de 1 a 50 empleados que externalizan su IT, autónomos técnicos que gestionan servidores de varios clientes, empresas con servidores físicos en local (on-premise), y negocios que manejan datos sensibles y prefieren no subirlos a la nube pública. No requiere conocimientos avanzados de Linux para el uso diario del panel, aunque sí se necesita un técnico para la instalación inicial.\n"
        ),
        "palabras_clave": ["dirigido", "empresa", "pyme", "cliente", "uso", "perfil", "quien", "tamaño"],
    },
    {
        "id": (
            "vigex-version-actual\n"
        ),
        "pregunta": (
            "¿Cuál es la versión actual de Vigex y qué incluye?\n"
        ),
        "respuesta": (
            "La versión actual de Vigex es **v1.0-rc1** (Release Candidate 1), correspondiente a la Fase 6 del proyecto (primera fase de ventas). Esta versión incluye todas las funcionalidades core: backups automatizados, restauración con verificación SHA256, gestión de servicios systemd, logs centralizados en MariaDB, alertas por Telegram y email, monitoreo con Grafana/Cacti, informes automáticos, terminal web, soporte con tickets, Vigex Central Support para gestión multicliente, e Inteligencia Artificial integrada (Asistente IA con RAG). Puedes ver la versión instalada en el footer del panel o ejecutando en el servidor: `head -5 /opt/vigex/api/main.py`.\n"
        ),
        "palabras_clave": ["versión", "version", "actual", "rc1", "fase", "instalada", "numero", "incluye"],
    },
    {
        "id": (
            "vigex-self-hosted\n"
        ),
        "pregunta": (
            "¿Vigex está en la nube o es self-hosted? ¿Mis datos son privados?\n"
        ),
        "respuesta": (
            "Vigex es **100% self-hosted**: se instala y ejecuta en tus propios servidores Linux. Tus datos (backups, logs, configuración, tickets) nunca salen de tus máquinas. No hay suscripción mensual a ningún servicio en la nube para las funciones core. La única excepción opcional es el **Asistente IA**: si eliges un proveedor externo (Groq, Gemini, OpenAI, Anthropic), las consultas al chat van a esa API. Puedes usar Ollama en local para el IA sin ningún coste ni dato externo. La instalación se hace con scripts bash: `sudo bash deploy/api/install_vigex_api.sh`.\n"
        ),
        "palabras_clave": ["self-hosted", "nube", "cloud", "datos", "privado", "privacidad", "seguridad", "propio"],
    },
    {
        "id": (
            "vigex-modulos\n"
        ),
        "pregunta": (
            "¿Qué módulos o secciones tiene el panel de Vigex?\n"
        ),
        "respuesta": (
            "El panel tiene los siguientes módulos accesibles desde el menú lateral:\n"
            "\n"
            "• **Dashboard** — resumen del estado: disco, servicios activos, último backup.\n"
            "• **Copias** — historial de backups, lanzar copia manual, verificar integridad.\n"
            "• **Restauración** — restaurar desde cualquier copia con verificación SHA256 previa.\n"
            "• **Servicios** — ver y controlar servicios systemd del servidor remoto.\n"
            "• **Logs** — consulta de logs centralizados desde la base de datos MariaDB.\n"
            "• **Alertas** — umbrales y canales de notificación (Telegram y/o email).\n"
            "• **Monitoreo** — integración con Grafana o Cacti para gráficas en tiempo real.\n"
            "• **Informes** — generación y envío automático de informes operacionales.\n"
            "• **Terminal** — terminal web con comandos SSH controlados al servidor.\n"
            "• **Soporte** — sistema de tickets de soporte técnico con estado y seguimiento.\n"
            "• **Asistente IA** — chat inteligente con RAG sobre documentación Vigex.\n"
            "• **Admin** — gestión de usuarios, permisos y configuración (solo administrador).\n"
        ),
        "palabras_clave": ["módulos", "secciones", "menu", "panel", "funciones", "dashboard", "partes", "copias", "logs"],
    },
    {
        "id": (
            "vigex-precio-planes\n"
        ),
        "pregunta": (
            "¿Cuánto cuesta Vigex? ¿Tiene planes o licencia?\n"
        ),
        "respuesta": (
            "Vigex es un producto comercial self-hosted. Al ser auto-hospedado, pagas la licencia una sola vez (o con mantenimiento anual opcional) y lo instalas en tus propios servidores sin coste mensual adicional por el software. Los planes se adaptan al tamaño de empresa y número de servidores. Contacta con el equipo para un presupuesto personalizado.\n"
            "\n"
            "Respecto al **Asistente IA**, los costes aproximados por proveedor son:\n"
            "• **Ollama (local)** — 0€, sin envío de datos a terceros.\n"
            "• **Groq** — capa gratuita generosa (~100 req/día gratis), luego ~0,06€/M tokens.\n"
            "• **Gemini 2.0 Flash** — ~0,22€/M tokens de entrada, muy económico.\n"
            "• **OpenAI gpt-4o-mini** — ~0,15€/M tokens de entrada.\n"
            "• **Anthropic claude-3-haiku** — ~0,25€/M tokens de entrada.\n"
            "Para una PyME con uso moderado del asistente, el coste mensual en IA suele ser inferior a 1-2€.\n"
        ),
        "palabras_clave": ["precio", "coste", "licencia", "pagar", "gratuito", "gratis", "planes", "cuanto"],
    },
    {
        "id": (
            "vigex-requisitos-hardware\n"
        ),
        "pregunta": (
            "¿Qué requisitos de hardware necesita el servidor para instalar Vigex?\n"
        ),
        "respuesta": (
            "Los requisitos dependen del perfil de despliegue:\n"
            "\n"
            "**Lite / todo en uno:**\n"
            "• CPU: 2 núcleos mínimo (4 recomendado)\n"
            "• RAM: 2 GB mínimo (4 GB recomendado)\n"
            "• Disco: 20 GB + espacio para backups\n"
            "\n"
            "**Standard / 2 servidores:**\n"
            "• Panel+backups: 2 vCPU, 2 GB RAM, 10 GB + almacenamiento backups\n"
            "• BD+logs: 2 vCPU, 2 GB RAM, 20 GB disco\n"
            "\n"
            "**Pro / 3 servidores:**\n"
            "• Panel: 2 vCPU, 2 GB RAM, 10 GB disco\n"
            "• BD+logs: 2 vCPU, 4 GB RAM, 50 GB disco\n"
            "• Backups: 2 vCPU, 2 GB RAM, capacidad según volumen de datos\n"
            "\n"
            "Si instalas el Asistente IA con **Ollama en local**, necesitas al menos 6 GB RAM adicionales para el modelo LLM (llama3.2:3b ocupa ~3 GB, mistral ~5 GB).\n"
        ),
        "palabras_clave": ["requisitos", "hardware", "ram", "cpu", "disco", "servidor", "mínimo", "recursos"],
    },
    {
        "id": (
            "vigex-so-compatible\n"
        ),
        "pregunta": (
            "¿En qué sistemas operativos funciona Vigex?\n"
        ),
        "respuesta": (
            "Vigex está diseñado y probado para **Ubuntu 22.04 LTS** en los servidores donde se instala. También debería funcionar en Ubuntu 20.04 y Debian 11/12, aunque no están oficialmente soportados. Los scripts de instalación asumen `apt` como gestor de paquetes y `systemd` como gestor de servicios.\n"
            "\n"
            "El **panel web** es compatible con cualquier navegador moderno (Chrome, Firefox, Edge, Safari) desde cualquier sistema operativo: Windows, Mac o Linux. Las herramientas de validación y desarrollo (PowerShell) corren en Windows.\n"
        ),
        "palabras_clave": ["sistema operativo", "ubuntu", "debian", "linux", "compatible", "so", "navegador", "windows"],
    },
    {
        "id": (
            "instalacion-pasos\n"
        ),
        "pregunta": (
            "¿Cómo se instala Vigex paso a paso?\n"
        ),
        "respuesta": (
            "Instalación general (perfil Standard recomendado):\n"
            "\n"
            "1. Clona el repositorio o descarga el paquete de instalación.\n"
            "2. Selecciona el perfil: `bash scripts/generar_config_perfil.sh` y elige `standard`.\n"
            "3. En el servidor del panel, ejecuta como root:\n"
            "   `sudo bash deploy/api/install_vigex_api.sh`\n"
            "   El instalador pide las IPs de los servidores, genera claves SSH y crea el servicio systemd.\n"
            "4. En el servidor de BD (si perfil dual/pro):\n"
            "   `sudo bash deploy/db/install_vigex_db.sh`\n"
            "5. En el servidor de backups:\n"
            "   `sudo bash deploy/backup-services/instalar_backup_services.sh`\n"
            "6. Instala el proxy HTTPS:\n"
            "   `sudo bash deploy/proxy/install_vigex_proxy.sh`\n"
            "\n"
            "El panel queda disponible en `https://IP_SERVIDOR`. Entra con el usuario `admin` y la contraseña que indicaste durante la instalación.\n"
        ),
        "palabras_clave": ["instalar", "instalación", "pasos", "script", "desplegar", "setup", "comenzar", "bash"],
    },
    {
        "id": (
            "perfiles-despliegue\n"
        ),
        "pregunta": (
            "¿Qué perfiles de despliegue existen en Vigex?\n"
        ),
        "respuesta": (
            "Vigex ofrece cuatro perfiles que determinan cuántos servidores se usan:\n"
            "\n"
            "**Lite / Single** — todo en un servidor. Ideal para pruebas o empresas muy pequeñas. Usa `127.0.0.1` para servicios locales. Requiere copia de backup a ubicación externa.\n"
            "\n"
            "**Standard / Dual** — 2 servidores: panel+backups y BD+logs separados. Recomendado para PyMEs. Es el perfil más habitual.\n"
            "\n"
            "**Pro / Distribuido** — 3 servidores: panel, BD+logs y backups por separado. Máxima separación de responsabilidades y mayor resiliencia ante fallos.\n"
            "\n"
            "**Custom** — el instalador pregunta host por host para configuraciones no estándar.\n"
            "\n"
            "El perfil se configura con `VIGEX_PROFILE` en `config.env`. Las plantillas están en `config/perfiles/`.\n"
        ),
        "palabras_clave": ["perfil", "despliegue", "lite", "standard", "pro", "dual", "distribuido", "servidores", "topologia"],
    },
    {
        "id": (
            "config-env-variables\n"
        ),
        "pregunta": (
            "¿Qué es config.env y cuáles son las variables más importantes?\n"
        ),
        "respuesta": (
            "`config.env` es el **fichero de configuración principal** de Vigex, ubicado en `/opt/vigex/api/config.env`. Contiene todas las variables de entorno del panel. Nunca se sube al repositorio git. El instalador lo genera desde `config.env.example`.\n"
            "\n"
            "Variables clave:\n"
            "• `SECRET_KEY` — clave secreta para cifrado de sesiones (auto-generada en instalación).\n"
            "• `ADMIN_USER` / `ADMIN_PASSWORD` — credenciales admin (password como hash bcrypt).\n"
            "• `SSH_USER`, `SERVICIOS_HOST`, `BACKUPS_HOST` — conexión SSH remota.\n"
            "• `VIGEX_SSH_ALLOWED_HOSTS` — lista blanca de IPs SSH permitidas.\n"
            "• `LOGS_DB_HOST/NAME/USER/PASS` — conexión a BD de logs MariaDB.\n"
            "• `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` — alertas Telegram.\n"
            "• `NOTIF_SMTP_*` — SMTP para alertas y informes por email.\n"
            "• `VIGEX_RAG_*` — Asistente IA (proveedor, modelo, clave API).\n"
            "• `CENTRAL_SUPPORT_*` — conexión a Vigex Central Support.\n"
            "\n"
            "Para editar: `nano /opt/vigex/api/config.env` y `systemctl restart vigex-api`.\n"
        ),
        "palabras_clave": ["config.env", "configuración", "variables", "entorno", "fichero", "settings", "secreto"],
    },
    {
        "id": (
            "primer-acceso\n"
        ),
        "pregunta": (
            "¿Cómo accedo por primera vez al panel tras la instalación?\n"
        ),
        "respuesta": (
            "Tras la instalación, el panel está en `https://IP_DEL_SERVIDOR` (puerto 443 con proxy) o en `http://IP:8000` directamente. El navegador puede mostrar advertencia de certificado autofirmado — haz clic en 'Avanzado' → 'Continuar' para aceptarlo.\n"
            "\n"
            "Credenciales de acceso:\n"
            "• **Usuario**: valor de `ADMIN_USER` en config.env (por defecto `admin`).\n"
            "• **Contraseña**: la que elegiste durante la instalación.\n"
            "\n"
            "Si olvidaste la contraseña, accede al servidor por SSH y edita el hash bcrypt en `config.env`. Genera un nuevo hash con:\n"
            "`python3 -c \"from passlib.context import CryptContext; print(CryptContext(['bcrypt']).hash('nueva_clave'))\"`\n"
            "Copia el resultado en la línea `ADMIN_PASSWORD=` y reinicia el servicio.\n"
        ),
        "palabras_clave": ["primer acceso", "login", "entrar", "acceder", "primera vez", "instalación", "https", "contraseña"],
    },
    {
        "id": (
            "actualizar-vigex\n"
        ),
        "pregunta": (
            "¿Cómo actualizo Vigex a una nueva versión?\n"
        ),
        "respuesta": (
            "Desde el servidor Linux, ejecuta como root:\n"
            "`sudo bash /ruta/al/repo/deploy/api/update_vigex_api.sh`\n"
            "\n"
            "El script preserva `config.env`, las claves SSH, los datos y la base de datos. Antes de actualizar es recomendable:\n"
            "1. Hacer una copia de seguridad manual desde el panel (Copias → Nueva copia).\n"
            "2. Anotar la versión actual: `head -5 /opt/vigex/api/main.py`.\n"
            "3. Revisar el CHANGELOG en `docs/ROADMAP.md` para cambios incompatibles.\n"
            "\n"
            "Desde Windows puedes usar: `tools\windows\instalar_vigex_windows.ps1` y seleccionar la opción 2 (Actualizar). Si el servicio falla después, revisa los logs con `journalctl -u vigex-api -n 50`.\n"
        ),
        "palabras_clave": ["actualizar", "update", "nueva", "version", "upgrade", "actualización"],
    },
    {
        "id": (
            "backup-fallo\n"
        ),
        "pregunta": (
            "¿Qué hago si una copia de seguridad falló?\n"
        ),
        "respuesta": (
            "Ve a **Copias** en el menú lateral y revisa el historial. El color rojo indica error. Posibles causas y soluciones:\n"
            "\n"
            "• **Servidor de backups apagado**: comprueba que la máquina está accesible.\n"
            "• **Sin espacio en disco**: `df -h` en el servidor de backups.\n"
            "• **Fallo SSH**: prueba `sudo -u vigex ssh -i /opt/vigex/api/.ssh/id_rsa_vigex vigex@IP_BACKUPS hostname`.\n"
            "• **Error en el script**: revisa `journalctl -u vigex-api -n 100` en el panel.\n"
            "\n"
            "Para lanzar una copia manual: botón **Nueva copia** en la sección Copias. Si el error persiste, abre un ticket en Soporte con el mensaje de error completo.\n"
        ),
        "palabras_clave": ["backup", "copia", "fallo", "error", "rojo", "historial", "fallida"],
    },
    {
        "id": (
            "backup-tipos\n"
        ),
        "pregunta": (
            "¿Qué tipos de copia de seguridad hace Vigex?\n"
        ),
        "respuesta": (
            "Vigex realiza los siguientes tipos de backup:\n"
            "\n"
            "• **Copia de base de datos (MySQL/MariaDB)**: dump completo de la BD de logs usando `backups_api.sh` en el servidor remoto, ejecutado vía SSH desde el panel. El fichero resultante se comprime y guarda en `BACKUP_OUTPUT_DIR`.\n"
            "\n"
            "• **Copia de ficheros**: posible mediante extensión de `backups_api.sh` con rsync o tar. Configurable según las necesidades de cada instalación.\n"
            "\n"
            "• **Sincronización externa**: el script `sync_external_backup.sh` puede copiar los backups locales a un almacenamiento externo (NAS, servidor remoto) para mayor seguridad (estrategia 3-2-1).\n"
            "\n"
            "Todos los backups incluyen verificación SHA256 para garantizar la integridad. La retención configurable (variable `BACKUP_RETENTION_KEEP`) elimina automáticamente las copias más antiguas al superar el límite.\n"
        ),
        "palabras_clave": ["tipos", "backup", "copia", "bd", "base de datos", "ficheros", "rsync", "tar", "externo"],
    },
    {
        "id": (
            "backup-programar\n"
        ),
        "pregunta": (
            "¿Cómo programo las copias de seguridad automáticas?\n"
        ),
        "respuesta": (
            "Las copias automáticas se programan mediante **cron** en el servidor del panel. El instalador puede configurar una tarea cron por defecto. Para verla o modificarla:\n"
            "\n"
            "`crontab -l -u vigex`  — ver tareas actuales del usuario vigex.\n"
            "`crontab -e -u vigex`  — editar el cron.\n"
            "\n"
            "Ejemplo de cron para backup diario a las 2:00 AM:\n"
            "`0 2 * * * /opt/vigex/api/scripts/run_backup.sh >> /var/log/vigex/backup.log 2>&1`\n"
            "\n"
            "También puedes lanzar copias manuales desde el panel en cualquier momento: **Copias → Nueva copia**. El historial con fecha, estado e integridad queda registrado en la pantalla de Copias.\n"
        ),
        "palabras_clave": ["programar", "cron", "automático", "automatico", "diario", "semanal", "horario", "backup"],
    },
    {
        "id": (
            "backup-retencion\n"
        ),
        "pregunta": (
            "¿Cuántas copias de seguridad se guardan? ¿Cómo funciona la retención?\n"
        ),
        "respuesta": (
            "La retención de backups se controla con la variable `BACKUP_RETENTION_KEEP` en `config.env`. Su valor por defecto es **10 copias**. Cuando se supera ese número, la copia más antigua se elimina automáticamente.\n"
            "\n"
            "Para cambiar la retención:\n"
            "1. Edita `config.env`: `nano /opt/vigex/api/config.env`\n"
            "2. Modifica: `BACKUP_RETENTION_KEEP=30` (por ejemplo, para 30 copias)\n"
            "3. Reinicia: `systemctl restart vigex-api`\n"
            "\n"
            "También puedes eliminar copias antiguas manualmente desde la pantalla **Copias** del panel, seleccionando la copia y pulsando el botón de eliminar. Se recomienda guardar al menos 7 copias diarias + 4 semanales para una buena política de recuperación.\n"
        ),
        "palabras_clave": ["retención", "retencion", "cuantas", "guardar", "eliminar", "antiguas", "limite", "keep"],
    },
    {
        "id": (
            "backup-integridad\n"
        ),
        "pregunta": (
            "¿Cómo verifica Vigex la integridad de las copias de seguridad?\n"
        ),
        "respuesta": (
            "Vigex calcula y almacena un **checksum SHA256** de cada copia de seguridad en el momento de su creación. Puedes verificar la integridad en cualquier momento desde:\n"
            "\n"
            "**Copias → Integridad** — muestra el estado de verificación de cada backup. Un check verde indica que el fichero no ha sido modificado ni corrompido. Un check rojo indica discrepancia en el hash (posible corrupción).\n"
            "\n"
            "Vigex verifica automáticamente el checksum antes de iniciar cualquier restauración. Si el hash no coincide, la restauración se bloquea para evitar restaurar datos corruptos. Para regenerar el checksum de una copia (si se movió el fichero), usa el botón 'Recalcular hash' en la pantalla de integridad.\n"
        ),
        "palabras_clave": ["integridad", "sha256", "checksum", "hash", "verificar", "corrupto", "validar"],
    },
    {
        "id": (
            "backup-externo-sync\n"
        ),
        "pregunta": (
            "¿Puedo sincronizar backups a un servidor o NAS externo?\n"
        ),
        "respuesta": (
            "Sí. Vigex incluye el script `sync_external_backup.sh` en `deploy/backup-services/package/` para sincronizar copias a un destino externo (NAS, servidor de almacenamiento, S3, etc.).\n"
            "\n"
            "Configuración típica:\n"
            "1. El script usa `rsync` vía SSH para copiar los backups locales al destino externo.\n"
            "2. Se ejecuta periódicamente mediante cron después de cada copia.\n"
            "3. Las variables de conexión (host, usuario, ruta destino) se configuran en el script o en `config.env`.\n"
            "\n"
            "Esto implementa la estrategia de backup **3-2-1**: 3 copias, en 2 medios diferentes, con 1 copia fuera del sitio. Es especialmente importante en el perfil Lite donde el almacenamiento es local. Para configurarlo consulta la guía en `docs/guias/guia_backup_externo.md`.\n"
        ),
        "palabras_clave": ["externo", "nas", "sync", "sincronizar", "rsync", "s3", "offsite", "3-2-1"],
    },
    {
        "id": (
            "disco-lleno\n"
        ),
        "pregunta": (
            "El disco está al 90% o más. ¿Qué hago?\n"
        ),
        "respuesta": (
            "Ve a **Monitoreo** para ver el detalle de uso por partición. Las causas más comunes son: copias de seguridad acumuladas (borra las antiguas desde la pantalla Copias), logs sin rotar (`logrotate -f /etc/logrotate.conf`) o el directorio `/var/log`. También puedes usar `df -h` y `du -sh /*` para identificar qué ocupa más espacio.\n"
            "\n"
            "Acciones inmediatas:\n"
            "• **Backups antiguos**: Copias → seleccionar copias antiguas → Eliminar.\n"
            "• **Logs del sistema**: `sudo journalctl --vacuum-size=500M`.\n"
            "• **Reducir retención**: `BACKUP_RETENTION_KEEP=5` en config.env.\n"
            "Si el disco supera el umbral configurado en `NOTIF_DISK_THRESHOLD` (por defecto 80%), Vigex envía una alerta automática por Telegram y/o email.\n"
        ),
        "palabras_clave": ["disco", "espacio", "lleno", "90", "80", "uso", "df", "capacidad"],
    },
    {
        "id": (
            "restaurar-backup\n"
        ),
        "pregunta": (
            "¿Cómo restauro una copia de seguridad?\n"
        ),
        "respuesta": (
            "Ve a **Copias** (o al módulo **Restauración**) y selecciona la copia que quieres restaurar. Pulsa 'Restaurar' y confirma el proceso.\n"
            "\n"
            "Vigex ejecutará estos pasos automáticamente:\n"
            "1. Verificación del checksum SHA256 de la copia.\n"
            "2. Ejecución remota de `restore_api.sh` en el servidor de backups vía SSH.\n"
            "3. Restauración de la base de datos en el destino configurado (`RESTORE_TARGET_DB` en config.env, por defecto `vigex_logs_restore_test`).\n"
            "4. Notificación al finalizar con el resultado.\n"
            "\n"
            "Si el proceso falla, revisa **Copias → Integridad** para verificar que la copia tiene checksum válido. Para una restauración manual de la BD: `mysql -h IP_DB -u vigex_restore -p nombre_bd < fichero_backup.sql`.\n"
        ),
        "palabras_clave": ["restaurar", "restore", "recuperar", "backup", "restablecer", "sha256", "bd"],
    },
    {
        "id": (
            "recuperacion-desastre-dro\n"
        ),
        "pregunta": (
            "¿Qué es el DRO y cómo funciona la recuperación ante desastres?\n"
        ),
        "respuesta": (
            "El **DRO (Disaster Recovery Operation)** es el procedimiento de recuperación ante desastres totales de Vigex. Está disponible en el panel en el módulo **Recuperación**.\n"
            "\n"
            "El DRO cubre los escenarios más graves:\n"
            "• Pérdida total del servidor del panel.\n"
            "• Corrupción completa de la base de datos.\n"
            "• Fallo simultáneo de múltiples componentes.\n"
            "\n"
            "El proceso de DRO guiado en el panel:\n"
            "1. Selecciona el punto de recuperación (copia de seguridad objetivo).\n"
            "2. Vigex verifica la integridad de la copia (SHA256).\n"
            "3. Se restaura la BD en el servidor de BD.\n"
            "4. Se verifica la coherencia de los datos restaurados.\n"
            "5. El panel informa del estado final con un resumen.\n"
            "\n"
            "Para desastres totales donde el propio panel está caído, consulta el procedimiento manual en `docs/guias/guia_disaster_recovery.md`.\n"
        ),
        "palabras_clave": ["dro", "desastre", "recuperación", "disaster", "recovery", "total", "fallo", "catastrofe"],
    },
    {
        "id": (
            "restauracion-test\n"
        ),
        "pregunta": (
            "¿Puedo probar una restauración sin afectar la producción?\n"
        ),
        "respuesta": (
            "Sí. Vigex restaura por defecto en una **base de datos de test**, no en producción. La variable `RESTORE_TARGET_DB` en `config.env` define el destino de restauración (por defecto: `vigex_logs_restore_test`). Esto permite verificar que los datos son correctos antes de tomar cualquier decisión.\n"
            "\n"
            "Para hacer una prueba de restauración:\n"
            "1. Ve a **Copias** → selecciona una copia reciente.\n"
            "2. Pulsa 'Restaurar' — se restaurará en la BD de test.\n"
            "3. Verifica los datos restaurados con el panel de verificación.\n"
            "4. Si todo es correcto y necesitas promover a producción, hazlo manualmente con acceso SSH al servidor de BD.\n"
            "\n"
            "Se recomienda hacer una prueba de restauración mensual para garantizar que las copias son válidas y el proceso funciona correctamente.\n"
        ),
        "palabras_clave": ["prueba", "test", "restauración", "producción", "verificar", "probar", "sandbox"],
    },
    {
        "id": (
            "backup-no-llega\n"
        ),
        "pregunta": (
            "No aparecen copias en el historial aunque el cron está configurado.\n"
        ),
        "respuesta": (
            "Si el cron está activo pero no aparecen copias:\n"
            "\n"
            "1. **Comprueba que el cron se ejecuta**: `grep CRON /var/log/syslog | tail -20`\n"
            "2. **Verifica logs del script de backup**: revisa el fichero de log definido en el cron.\n"
            "3. **Comprueba la conexión SSH al servidor de backups**:\n"
            "   `sudo -u vigex ssh -i /opt/vigex/api/.ssh/id_rsa_vigex vigex@IP_BACKUPS hostname`\n"
            "4. **Espacio en disco del servidor de backups**: `df -h` — si está lleno, el script falla silenciosamente.\n"
            "5. **Usuario y permisos**: el usuario `vigex` debe tener permiso de escritura en `BACKUP_OUTPUT_DIR`.\n"
            "6. Revisa el log del panel: `journalctl -u vigex-api -n 100`\n"
            "\n"
            "Si todo parece correcto, lanza una copia manual desde el panel para ver el error exacto.\n"
        ),
        "palabras_clave": ["cron", "historial", "no aparece", "backup", "vacio", "automatico", "falla"],
    },
    {
        "id": (
            "servicio-caido\n"
        ),
        "pregunta": (
            "Un servicio aparece como caído. ¿Cómo lo reinicio?\n"
        ),
        "respuesta": (
            "Ve a **Servicios** en el menú lateral. Pulsa el botón de reinicio junto al servicio afectado. Si no responde, usa la Terminal integrada para ejecutar:\n"
            "`systemctl restart <nombre-servicio>`\n"
            "\n"
            "Para diagnosticar por qué cayó:\n"
            "`journalctl -u <nombre-servicio> -n 50 --no-pager`\n"
            "\n"
            "Si el servicio falla repetidamente:\n"
            "• Comprueba el estado completo: `systemctl status <nombre-servicio>`\n"
            "• Busca errores en los logs del propio servicio (normalmente en `/var/log/`).\n"
            "• Verifica que el binario o script que lanza el servicio existe y tiene permisos.\n"
            "• Comprueba si hay conflictos de puertos: `ss -tlnp | grep PUERTO`\n"
            "\n"
            "Vigex envía una alerta automática si un servicio monitoreado cae y no se recupera en el tiempo configurado.\n"
        ),
        "palabras_clave": ["servicio", "caído", "caido", "reiniciar", "parado", "stopped", "failed", "systemctl"],
    },
    {
        "id": (
            "servicios-gestion\n"
        ),
        "pregunta": (
            "¿Qué servicios puedo gestionar desde el panel de Vigex?\n"
        ),
        "respuesta": (
            "Desde el módulo **Servicios** puedes ver y controlar todos los servicios systemd del servidor remoto (el servidor de servicios configurado en `SERVICIOS_HOST`). Las acciones disponibles son:\n"
            "\n"
            "• **Ver estado** — activo, inactivo, fallido, estado completo systemd.\n"
            "• **Iniciar** — `systemctl start <servicio>`.\n"
            "• **Detener** — `systemctl stop <servicio>`.\n"
            "• **Reiniciar** — `systemctl restart <servicio>`.\n"
            "• **Habilitar/deshabilitar** — activar o desactivar el inicio automático.\n"
            "\n"
            "Todos los comandos se ejecutan vía SSH seguro usando `servicios_api.sh` en el servidor remoto, que está en la lista blanca de comandos permitidos. No se puede ejecutar ningún comando arbitrario — hay una lista estricta de servicios y acciones permitidas por razones de seguridad.\n"
        ),
        "palabras_clave": ["servicios", "systemctl", "gestionar", "start", "stop", "restart", "estado"],
    },
    {
        "id": (
            "agregar-servicio-monitoreo\n"
        ),
        "pregunta": (
            "¿Cómo añado un servicio para que Vigex lo monitoree y alerte?\n"
        ),
        "respuesta": (
            "Para añadir un servicio al monitoreo de alertas:\n"
            "\n"
            "1. Ve a **Alertas** en el menú lateral.\n"
            "2. Busca la sección 'Servicios monitoreados'.\n"
            "3. Añade el nombre del servicio systemd (ej: `nginx`, `mysql`, `php8.1-fpm`).\n"
            "4. Configura el umbral de tiempo de caída antes de alertar.\n"
            "5. Activa la alerta para ese servicio.\n"
            "\n"
            "Vigex comprobará periódicamente (cada `NOTIF_CHECK_INTERVAL` segundos, por defecto 15 minutos) el estado del servicio y enviará alerta por Telegram y/o email si lo detecta caído. El cooldown evita spam de alertas (configurable con `NOTIF_COOLDOWN`, por defecto 4 horas).\n"
        ),
        "palabras_clave": ["añadir servicio", "monitoreo", "alertas", "vigilar", "notificación", "servicio"],
    },
    {
        "id": (
            "logs-vacios\n"
        ),
        "pregunta": (
            "Los logs aparecen vacíos o no se actualizan.\n"
        ),
        "respuesta": (
            "Los logs se leen de la base de datos MariaDB en el servidor de logs. Comprueba:\n"
            "\n"
            "1. **Conexión a la BD**: desde el servidor del panel:\n"
            "   `mysql -h IP_DB -u vigex_logs -p vigex_logs`\n"
            "   Si falla, hay un problema de red o credenciales.\n"
            "2. **Variables correctas en config.env**: `LOGS_DB_HOST`, `LOGS_DB_NAME`, `LOGS_DB_USER`, `LOGS_DB_PASS`.\n"
            "3. **Servicio MariaDB activo** en el servidor de BD:\n"
            "   `systemctl status mariadb` (o `mysql`).\n"
            "4. **Que los logs se están escribiendo**: la aplicación que genera logs debe estar configurada para escribir en la BD `vigex_logs` con origen `LOGS_ORIGIN`.\n"
            "5. **Filtros activos**: comprueba que no tienes filtros de fecha o severidad aplicados en la pantalla de Logs que oculten entradas.\n"
        ),
        "palabras_clave": ["log", "logs", "vacío", "vacios", "db", "base de datos", "mariadb", "mysql", "actualizar"],
    },
    {
        "id": (
            "logs-buscar-filtrar\n"
        ),
        "pregunta": (
            "¿Cómo busco o filtro los logs en el panel?\n"
        ),
        "respuesta": (
            "La pantalla **Logs** ofrece varios filtros para encontrar entradas específicas:\n"
            "\n"
            "• **Rango de fechas** — filtra por fecha inicio y fecha fin.\n"
            "• **Nivel de severidad** — INFO, WARNING, ERROR, CRITICAL.\n"
            "• **Origen** — filtra por aplicación o servicio que generó el log (coincide con `LOGS_ORIGIN` configurado en cada fuente).\n"
            "• **Búsqueda de texto** — busca en el mensaje del log.\n"
            "\n"
            "Los resultados se muestran paginados (50 entradas por página). Puedes exportar los logs filtrados a CSV desde el botón 'Exportar' para análisis externo. Los logs se almacenan en la tabla `logs` de la base de datos `vigex_logs` en el servidor de BD.\n"
        ),
        "palabras_clave": ["buscar", "filtrar", "logs", "nivel", "severidad", "fecha", "origen", "exportar"],
    },
    {
        "id": (
            "logs-base-datos-mariadb\n"
        ),
        "pregunta": (
            "¿Qué base de datos usa Vigex para los logs? ¿Cómo se configura?\n"
        ),
        "respuesta": (
            "Vigex usa **MariaDB** (compatible con MySQL) como base de datos centralizada para logs. El instalador `deploy/db/install_vigex_db.sh` crea la BD, el usuario y los permisos necesarios automáticamente.\n"
            "\n"
            "Estructura principal:\n"
            "• **BD**: `vigex_logs` (configurable con `LOGS_DB_NAME`).\n"
            "• **Usuario lectura**: `vigex_logs` (solo SELECT desde el panel).\n"
            "• **Usuario backup**: `vigex_backup` (solo SELECT para dumps).\n"
            "• **Usuario restore**: `vigex_restore` (permiso de escritura para restauración).\n"
            "\n"
            "Variables de conexión en `config.env`:\n"
            "• `LOGS_DB_HOST` — IP del servidor de BD.\n"
            "• `LOGS_DB_NAME` — nombre de la base de datos.\n"
            "• `LOGS_DB_USER` / `LOGS_DB_PASS` — credenciales de acceso.\n"
            "\n"
            "El panel accede a la BD directamente con `pymysql` (no por SSH).\n"
        ),
        "palabras_clave": ["mariadb", "mysql", "base de datos", "bd", "logs", "instalar", "usuario", "configurar"],
    },
    {
        "id": (
            "logs-retencion-bd\n"
        ),
        "pregunta": (
            "¿Los logs se borran automáticamente? ¿Cuánto tiempo se guardan?\n"
        ),
        "respuesta": (
            "Por defecto Vigex no tiene un TTL (tiempo de vida) automático para los logs — se acumulan en la BD MariaDB indefinidamente. Si quieres implementar una política de retención de logs, tienes dos opciones:\n"
            "\n"
            "1. **Rotación manual con SQL**: conecta a la BD y elimina logs antiguos:\n"
            "   `DELETE FROM logs WHERE fecha < DATE_SUB(NOW(), INTERVAL 90 DAY);`\n"
            "2. **Evento MySQL automático**: crea un evento programado en MariaDB:\n"
            "   `CREATE EVENT limpiar_logs ON SCHEDULE EVERY 1 DAY DO DELETE FROM logs WHERE fecha < DATE_SUB(NOW(), INTERVAL 90 DAY);`\n"
            "\n"
            "Ten en cuenta que cuantos más logs acumules, más lenta será la consulta desde el panel. Para BDs con muchos registros, añade un índice a la columna `fecha`:\n"
            "`CREATE INDEX idx_fecha ON logs(fecha);`\n"
        ),
        "palabras_clave": ["retención", "logs", "borrar", "limpiar", "tiempo", "antiguo", "ttl", "mariadb"],
    },
    {
        "id": (
            "alerta-telegram\n"
        ),
        "pregunta": (
            "No recibo alertas por Telegram. ¿Cómo lo configuro?\n"
        ),
        "respuesta": (
            "Pasos para configurar Telegram:\n"
            "\n"
            "1. Crea un bot con `@BotFather` en Telegram → `/newbot` → copia el token.\n"
            "2. Envía un mensaje al bot y obtén tu chat ID:\n"
            "   `https://api.telegram.org/bot<TOKEN>/getUpdates`\n"
            "   Busca `\"chat\":{\"id\":XXXXXXX}` en la respuesta.\n"
            "3. Edita `config.env` en el servidor:\n"
            "   `nano /opt/vigex/api/config.env`\n"
            "   Configura: `TELEGRAM_BOT_TOKEN=tu_token` y `TELEGRAM_CHAT_ID=tu_chat_id`.\n"
            "4. Activa las notificaciones: `NOTIF_ENABLED=true`.\n"
            "5. Reinicia: `systemctl restart vigex-api`.\n"
            "6. Prueba desde el panel: **Alertas → Probar alertas Telegram**.\n"
            "\n"
            "Si sigue sin llegar, comprueba que el bot no está bloqueado y que el token y chat ID son correctos (el chat ID puede ser negativo para grupos).\n"
        ),
        "palabras_clave": ["telegram", "alerta", "notificación", "bot", "token", "chatid", "configurar"],
    },
    {
        "id": (
            "alerta-email\n"
        ),
        "pregunta": (
            "No recibo alertas por email. ¿Cómo lo configuro?\n"
        ),
        "respuesta": (
            "Configura el SMTP en `config.env`:\n"
            "\n"
            "```\n"
            "NOTIF_ENABLED=true\n"
            "NOTIF_EMAIL_TO=destino@tuempresa.com\n"
            "NOTIF_EMAIL_FROM=vigex@tuempresa.com\n"
            "NOTIF_SMTP_HOST=smtp.gmail.com\n"
            "NOTIF_SMTP_PORT=587\n"
            "NOTIF_SMTP_USER=vigex@gmail.com\n"
            "NOTIF_SMTP_PASS=CONTRASEÑA_DE_APLICACION\n"
            "```\n"
            "\n"
            "**Para Gmail**: activa la verificación en dos pasos → 'Contraseñas de aplicación' → genera una contraseña exclusiva para Vigex (no uses tu contraseña normal).\n"
            "\n"
            "**Para otros proveedores**: consulta la configuración SMTP específica (Outlook usa smtp-mail.outlook.com:587, Yahoo usa smtp.mail.yahoo.com:587).\n"
            "\n"
            "Prueba el envío desde: **Alertas → Probar alertas → Email**. Reinicia el servicio tras cualquier cambio en config.env.\n"
        ),
        "palabras_clave": ["email", "correo", "smtp", "gmail", "alerta", "notificación", "envío", "configurar"],
    },
    {
        "id": (
            "alertas-tipos\n"
        ),
        "pregunta": (
            "¿Qué tipos de alertas envía Vigex automáticamente?\n"
        ),
        "respuesta": (
            "Vigex incluye un sistema de alertas proactivas (`NOTIF_ENABLED=true`) que envía notificaciones automáticas ante estos eventos:\n"
            "\n"
            "• **Disco casi lleno** — cuando el uso supera `NOTIF_DISK_THRESHOLD` (por defecto 80%).\n"
            "• **Servicio caído** — cuando un servicio monitoreado pasa a estado `failed` o `inactive`.\n"
            "• **Backup fallido** — cuando una copia de seguridad programada falla.\n"
            "• **Backup no realizado** — cuando pasan más de X horas sin copia exitosa.\n"
            "• **Alto uso de CPU o RAM** — si se configura el umbral correspondiente.\n"
            "• **Certificado SSL próximo a expirar** — aviso con 30 y 7 días de antelación.\n"
            "\n"
            "Todas las alertas respetan el **cooldown** (`NOTIF_COOLDOWN`, por defecto 4 horas) para evitar spam. Los canales disponibles son Telegram y/o email, configurables con `ALERTS_DEFAULT_CHANNEL`.\n"
        ),
        "palabras_clave": ["tipos", "alertas", "disco", "servicio", "backup", "cpu", "ram", "ssl", "automático"],
    },
    {
        "id": (
            "alertas-cooldown\n"
        ),
        "pregunta": (
            "Recibo demasiadas alertas repetidas. ¿Cómo reduzco la frecuencia?\n"
        ),
        "respuesta": (
            "El sistema de alertas tiene un mecanismo de **cooldown** para evitar spam. Configura en `config.env`:\n"
            "\n"
            "• `NOTIF_COOLDOWN` — segundos mínimos entre dos alertas del mismo tipo. Por defecto 14400 (4 horas). Aumenta este valor para recibir menos alertas.\n"
            "  Ejemplo: `NOTIF_COOLDOWN=86400` = máximo 1 alerta por tipo al día.\n"
            "\n"
            "• `NOTIF_CHECK_INTERVAL` — segundos entre comprobaciones automáticas. Por defecto 900 (15 minutos). Auméntalo para reducir la frecuencia de checks.\n"
            "\n"
            "• `NOTIF_DISK_THRESHOLD` — porcentaje de disco a partir del cual se alerta. Por defecto 80. Si recibes muchas alertas de disco, súbelo a 90 o 95.\n"
            "\n"
            "Reinicia el servicio tras modificar: `systemctl restart vigex-api`.\n"
        ),
        "palabras_clave": ["cooldown", "spam", "muchas alertas", "frecuencia", "repetidas", "intervalo", "reducir"],
    },
    {
        "id": (
            "monitoreo-grafica\n"
        ),
        "pregunta": (
            "El gráfico de monitoreo no carga o está vacío.\n"
        ),
        "respuesta": (
            "La sección **Monitoreo** integra Grafana o Cacti para gráficas en tiempo real. Si aparece vacía o no carga:\n"
            "\n"
            "1. **Comprueba la URL configurada**: `GRAFANA_URL` o `CACTI_URL` en `config.env`.\n"
            "2. **Verifica que Grafana está activo**: `systemctl status grafana-server`.\n"
            "3. **Problema de CORS o autenticación**: Grafana debe permitir embedding (desactiva la protección de embebido en Grafana: `allow_embedding = true` en `/etc/grafana/grafana.ini`).\n"
            "4. **Sin monitoreo externo instalado**: la sección muestra un mensaje informativo si no hay URL configurada. El dashboard principal siempre muestra disco y servicios básicos sin necesidad de Grafana.\n"
            "\n"
            "Para instalar Grafana en el servidor de BD:\n"
            "`sudo apt install -y grafana && sudo systemctl enable --now grafana-server`\n"
        ),
        "palabras_clave": ["monitoreo", "gráfica", "grafico", "grafana", "cacti", "vacío", "carga", "embedding"],
    },
    {
        "id": (
            "monitoreo-dashboard\n"
        ),
        "pregunta": (
            "¿Qué información muestra el dashboard principal de Vigex?\n"
        ),
        "respuesta": (
            "El **Dashboard** (página principal del panel) muestra un resumen en tiempo real:\n"
            "\n"
            "• **Estado del disco** — uso porcentual de la partición principal (barra de progreso con alerta visual si supera el 80%).\n"
            "• **Servicios activos** — número de servicios systemd activos vs total monitoreados.\n"
            "• **Último backup** — fecha y estado de la copia de seguridad más reciente.\n"
            "• **Alertas recientes** — últimas alertas enviadas.\n"
            "• **Estado de la conexión SSH** — indica si el servidor remoto es accesible.\n"
            "• **Versión del panel** — versión instalada de Vigex.\n"
            "\n"
            "Los datos del dashboard se actualizan automáticamente cada 30 segundos (refresh automático en la página). El código de color del estado: verde = todo OK, amarillo = advertencia, rojo = crítico.\n"
        ),
        "palabras_clave": ["dashboard", "inicio", "pantalla principal", "resumen", "estado", "disco", "servicios"],
    },
    {
        "id": (
            "ssh-fallo-conexion\n"
        ),
        "pregunta": (
            "El panel no puede conectarse al servidor de backups por SSH.\n"
        ),
        "respuesta": (
            "Pasos de diagnóstico:\n"
            "\n"
            "1. **Servidor accesible en red**: `ping IP_BACKUPS` desde el servidor del panel.\n"
            "2. **Usuario `vigex` existe** en el servidor remoto: `id vigex`.\n"
            "3. **Clave pública instalada**: la clave en `/opt/vigex/api/.ssh/id_rsa_vigex.pub` debe estar en `~vigex/.ssh/authorized_keys` del servidor remoto.\n"
            "4. **Test manual de SSH**:\n"
            "   `sudo -u vigex ssh -i /opt/vigex/api/.ssh/id_rsa_vigex -o StrictHostKeyChecking=yes vigex@IP_BACKUPS hostname`\n"
            "5. **IP en la lista blanca**: `VIGEX_SSH_ALLOWED_HOSTS` en config.env debe incluir la IP del servidor de backups.\n"
            "6. **known_hosts**: si cambió la IP del servidor, regenera el known_hosts con:\n"
            "   `sudo bash deploy/api/install_vigex_api.sh --regenerate-keys`\n"
            "\n"
            "El log del panel muestra el error exacto: `journalctl -u vigex-api -n 50`.\n"
        ),
        "palabras_clave": ["ssh", "conexión", "backups", "remoto", "authorized_keys", "id_rsa", "fallo"],
    },
    {
        "id": (
            "seguridad-ssh-modelo\n"
        ),
        "pregunta": (
            "¿Cómo funciona el modelo de seguridad SSH de Vigex?\n"
        ),
        "respuesta": (
            "Vigex implementa SSH endurecido con varias capas de seguridad:\n"
            "\n"
            "• **Clave dedicada ed25519**: generada durante la instalación en `/opt/vigex/api/.ssh/id_rsa_vigex` (a pesar del nombre, es ed25519 por defecto).\n"
            "• **BatchMode=yes**: nunca pide contraseñas interactivas — falla limpiamente si no hay clave válida.\n"
            "• **StrictHostKeyChecking=yes**: solo conecta a hosts cuya huella fingerprint está en el fichero `known_hosts` dedicado (`VIGEX_SSH_KNOWN_HOSTS`).\n"
            "• **Lista blanca de hosts** (`VIGEX_SSH_ALLOWED_HOSTS`): el panel solo puede conectarse por SSH a IPs explícitamente permitidas.\n"
            "• **Lista blanca de comandos**: solo se pueden ejecutar los scripts específicos (`servicios_api.sh`, `backups_api.sh`, `restore_api.sh`) y comandos muy acotados (`cat`, `crontab -l`, `hostname && date`). No es posible ejecutar comandos arbitrarios — esto se valida en la función `validate_ssh_run()`.\n"
        ),
        "palabras_clave": ["ssh", "seguridad", "ed25519", "clave", "hardened", "stricthostkey", "whitelist", "modelo"],
    },
    {
        "id": (
            "seguridad-contrasenas\n"
        ),
        "pregunta": (
            "¿Cómo se almacenan las contraseñas en Vigex? ¿Son seguras?\n"
        ),
        "respuesta": (
            "Las contraseñas de usuarios del panel se almacenan como **hashes bcrypt** usando la librería `passlib`. bcrypt es el estándar actual de la industria para hashing de contraseñas: es resistente a ataques de fuerza bruta por su coste computacional configurable (factor de trabajo).\n"
            "\n"
            "• La contraseña nunca se almacena en texto plano — solo el hash.\n"
            "• El hash incluye un salt aleatorio, evitando ataques de rainbow table.\n"
            "• Vigex incluye compatibilidad temporal con texto plano para migración de usuarios legacy, pero se recomienda migrar todas las cuentas a bcrypt.\n"
            "\n"
            "Para cambiar la contraseña de admin:\n"
            "`python3 -c \"from passlib.context import CryptContext; print(CryptContext(['bcrypt']).hash('nueva_clave'))\"`\n"
            "Pega el resultado en `ADMIN_PASSWORD=` en `config.env` y reinicia.\n"
        ),
        "palabras_clave": ["contraseña", "password", "bcrypt", "hash", "seguridad", "almacenar", "passlib"],
    },
    {
        "id": (
            "seguridad-fuerza-bruta\n"
        ),
        "pregunta": (
            "¿Vigex tiene protección contra ataques de fuerza bruta al login?\n"
        ),
        "respuesta": (
            "Sí. Vigex incluye protección anti fuerza bruta en el formulario de login:\n"
            "\n"
            "• `VIGEX_LOGIN_MAX_ATTEMPTS` — número máximo de intentos fallidos antes de bloqueo (por defecto 5 intentos).\n"
            "• `VIGEX_LOGIN_WINDOW_SECONDS` — ventana de tiempo en segundos para los intentos (por defecto 900 segundos = 15 minutos).\n"
            "\n"
            "Si se superan los intentos permitidos, la IP queda bloqueada durante la ventana de tiempo. Todos los intentos de login se registran en `auth_logs.json` (`/opt/vigex/api/auth_logs.json`) con IP, usuario y timestamp.\n"
            "\n"
            "Adicionalmente, el proxy nginx puede configurarse con rate limiting para una capa adicional de protección antes de que las peticiones lleguen al panel.\n"
        ),
        "palabras_clave": ["fuerza bruta", "brute force", "login", "bloqueo", "intentos", "seguridad", "ataque"],
    },
    {
        "id": (
            "seguridad-sesiones\n"
        ),
        "pregunta": (
            "¿Cuánto dura la sesión en el panel? ¿Se puede configurar el auto-logout?\n"
        ),
        "respuesta": (
            "La duración de sesión se controla con estas variables en `config.env`:\n"
            "\n"
            "• `VIGEX_SESSION_MAX_AGE` — duración máxima de la sesión en segundos. Por defecto 28800 (8 horas). Al expirar, el usuario debe volver a hacer login.\n"
            "\n"
            "• `VIGEX_AUTO_LOGOUT_MINUTES` — minutos de inactividad antes del auto-logout. Por defecto 60. Configurable también desde el panel en **Admin → Configuración**. Pon `0` para desactivar el auto-logout por inactividad.\n"
            "\n"
            "• `VIGEX_SESSION_HTTPS_ONLY` — activa la cookie de sesión solo por HTTPS. Recomendado `true` cuando el proxy sirve HTTPS real (dominio con certbot).\n"
            "\n"
            "Las sesiones usan cookies firmadas con `SECRET_KEY`. Si cambias `SECRET_KEY`, todas las sesiones activas se invalidan y los usuarios deben volver a entrar.\n"
        ),
        "palabras_clave": ["sesión", "session", "auto-logout", "tiempo", "duración", "inactividad", "cookie"],
    },
    {
        "id": (
            "certificado-https\n"
        ),
        "pregunta": (
            "El navegador advierte de certificado no válido o conexión no segura.\n"
        ),
        "respuesta": (
            "Si usas el certificado autofirmado que instala Vigex por defecto, el navegador mostrará una advertencia. Es normal y seguro si conoces el servidor. Para tener HTTPS real con certificado válido de Let's Encrypt:\n"
            "\n"
            "1. Asegúrate de tener un dominio apuntando a la IP del servidor.\n"
            "2. Instala certbot: `sudo apt install certbot python3-certbot-nginx`\n"
            "3. Obtén el certificado: `sudo certbot --nginx -d TU_DOMINIO`\n"
            "4. Certbot configura nginx automáticamente y renueva el certificado antes de su expiración.\n"
            "5. Activa en config.env: `VIGEX_SESSION_HTTPS_ONLY=true`\n"
            "6. Reinicia el panel: `systemctl restart vigex-api`\n"
            "\n"
            "Ver guía completa en `docs/guias/guia_dominio_email.md`.\n"
        ),
        "palabras_clave": ["certificado", "https", "ssl", "tls", "seguro", "advertencia", "certbot", "letsencrypt"],
    },
    {
        "id": (
            "nuevo-usuario\n"
        ),
        "pregunta": (
            "¿Cómo añado un usuario al panel?\n"
        ),
        "respuesta": (
            "Ve a **Admin → Usuarios** (solo disponible para el administrador). Pulsa 'Añadir usuario' e introduce:\n"
            "\n"
            "• **Nombre de usuario** — identificador de login (sin espacios).\n"
            "• **Contraseña** — se guarda como hash bcrypt automáticamente.\n"
            "• **Permisos** — selecciona los módulos a los que tendrá acceso:\n"
            "  - `backups` — acceso a Copias y Restauración.\n"
            "  - `logs` — acceso a la sección de Logs.\n"
            "  - `servicios` — acceso a gestión de Servicios.\n"
            "  - `alertas` — acceso a configuración de Alertas.\n"
            "  - `terminal` — acceso a la Terminal web (⚠️ otorgar con precaución).\n"
            "\n"
            "El nuevo usuario puede entrar de inmediato en `/login`. Los usuarios no-admin no pueden acceder a la sección **Admin**.\n"
        ),
        "palabras_clave": ["usuario", "user", "añadir", "nuevo", "acceso", "permisos", "admin", "crear"],
    },
    {
        "id": (
            "permisos-modulos\n"
        ),
        "pregunta": (
            "¿Qué permisos de módulo existen y qué puede hacer cada uno?\n"
        ),
        "respuesta": (
            "Vigex tiene un sistema de permisos por módulo. Los permisos disponibles son:\n"
            "\n"
            "• **`logs`** — puede ver y filtrar logs centralizados. Sin acceso a backups ni servicios.\n"
            "• **`backups`** — puede ver el historial de copias, lanzar copias manuales y verificar integridad. También accede a la pantalla de Restauración.\n"
            "• **`servicios`** — puede ver estado de servicios, iniciarlos, detenerlos y reiniciarlos en el servidor remoto.\n"
            "• **`alertas`** — puede configurar umbrales, canales de notificación y probar el envío de alertas.\n"
            "• **`terminal`** — accede a la Terminal web para ejecutar comandos SSH controlados. **Otorgar solo a usuarios de confianza.**\n"
            "\n"
            "El usuario administrador tiene acceso completo a todos los módulos más la sección Admin (gestión de usuarios y configuración del sistema).\n"
        ),
        "palabras_clave": ["permisos", "módulos", "roles", "acceso", "logs", "backups", "servicios", "terminal"],
    },
    {
        "id": (
            "password-admin\n"
        ),
        "pregunta": (
            "Olvidé la contraseña del administrador. ¿Cómo la cambio?\n"
        ),
        "respuesta": (
            "Accede al servidor por SSH y edita `config.env`:\n"
            "`nano /opt/vigex/api/config.env`\n"
            "\n"
            "Genera un nuevo hash bcrypt con Python:\n"
            "`python3 -c \"from passlib.context import CryptContext; print(CryptContext(['bcrypt']).hash('nueva_contraseña'))\"`\n"
            "\n"
            "Copia el hash resultante (comienza por `$2b$12$...`) y pégalo en la línea:\n"
            "`ADMIN_PASSWORD=$2b$12$...`\n"
            "\n"
            "Guarda el fichero y reinicia el servicio:\n"
            "`systemctl restart vigex-api`\n"
            "\n"
            "A partir de ese momento podrás entrar con la nueva contraseña. Si no tienes acceso SSH al servidor, contacta con el administrador del sistema o con el soporte de Vigex para recuperar el acceso.\n"
        ),
        "palabras_clave": ["contraseña", "password", "olvide", "admin", "acceso", "login", "bcrypt", "cambiar"],
    },
    {
        "id": (
            "informe-no-llega\n"
        ),
        "pregunta": (
            "El informe automático no llega por email.\n"
        ),
        "respuesta": (
            "Comprueba en **Informes** del panel:\n"
            "\n"
            "1. Que hay un perfil de informe configurado y activo.\n"
            "2. Que la frecuencia (diario/semanal/mensual) y la hora de envío son correctas.\n"
            "3. Que el email del perfil es el correcto.\n"
            "4. Que la configuración SMTP en `config.env` es válida — prueba con **Alertas → Probar alertas → Email**.\n"
            "5. Revisa si el email llegó a la carpeta de spam.\n"
            "\n"
            "Puedes enviar un informe manual con el botón **'Enviar ahora'** para comprobar que la entrega funciona. Los informes se generan como Markdown y se envían como texto formateado. Las copias generadas se guardan en `reports/` en el servidor del panel.\n"
        ),
        "palabras_clave": ["informe", "reporte", "email", "correo", "automático", "llega", "envío", "programado"],
    },
    {
        "id": (
            "informes-contenido\n"
        ),
        "pregunta": (
            "¿Qué incluyen los informes automáticos de Vigex?\n"
        ),
        "respuesta": (
            "Los **informes automáticos** de Vigex son resúmenes operacionales que incluyen:\n"
            "\n"
            "• **Resumen de backups** — número de copias realizadas, estado de cada una, espacio utilizado y tendencia de crecimiento.\n"
            "• **Estado de servicios** — servicios monitoreados, incidencias y tiempo de caída.\n"
            "• **Uso de disco** — evolución del espacio en disco durante el período.\n"
            "• **Alertas enviadas** — listado de alertas generadas en el período con su causa.\n"
            "• **Logs críticos** — resumen de entradas de log con severidad ERROR o CRITICAL.\n"
            "• **Tickets de soporte** — tickets abiertos, resueltos y tiempo medio de respuesta.\n"
            "\n"
            "Los informes se pueden configurar con frecuencia **diaria, semanal o mensual** y se envían automáticamente al email configurado en el perfil de informe.\n"
        ),
        "palabras_clave": ["informe", "contenido", "que incluye", "semanal", "mensual", "resumen", "operacional"],
    },
    {
        "id": (
            "soporte-tickets\n"
        ),
        "pregunta": (
            "¿Cómo funciona el sistema de tickets de soporte?\n"
        ),
        "respuesta": (
            "El módulo **Soporte** de Vigex es un sistema de tickets integrado en el panel. Funciona así:\n"
            "\n"
            "1. **Crear ticket**: desde **Soporte → Nuevo ticket** describe el problema, su prioridad y el módulo afectado.\n"
            "2. **Ticket local**: el ticket se guarda en la base de datos SQLite local del panel.\n"
            "3. **Envío a Central Support** (si está configurado): el ticket se envía automáticamente al servidor Vigex Central del proveedor de IT, que gestiona los tickets de todos sus clientes desde un único panel.\n"
            "4. **Seguimiento**: puedes ver el estado del ticket (Abierto, En progreso, Resuelto, Cerrado) y añadir comentarios.\n"
            "5. **Sincronización**: los cambios de estado realizados en Central Support se sincronizan de vuelta al panel del cliente automáticamente.\n"
            "\n"
            "Si Central Support no está configurado, los tickets son solo locales y los gestiona el propio administrador del panel.\n"
        ),
        "palabras_clave": ["tickets", "soporte", "incidencia", "problema", "ayuda", "abrir ticket", "estado"],
    },
    {
        "id": (
            "soporte-offline-retry\n"
        ),
        "pregunta": (
            "¿Qué pasa si el servidor Central Support no está disponible?\n"
        ),
        "respuesta": (
            "Vigex tiene un mecanismo de **cola offline y reintentos** para garantizar que ningún ticket se pierda aunque Central Support no esté disponible:\n"
            "\n"
            "1. Si el envío al Central falla, el ticket se marca como 'pendiente de envío' en la BD local.\n"
            "2. Un timer systemd (`vigex-central-retry.timer`) ejecuta periódicamente el script `scripts/retry_central_pending.py`, que reintenta enviar los tickets pendientes.\n"
            "3. Una vez Central Support vuelve a estar accesible, los tickets en cola se envían automáticamente en orden.\n"
            "\n"
            "Puedes ver los tickets pendientes de envío en **Soporte → Pendientes de sincronización**. El timer se instala con `deploy/api/install_central_retry_timer.sh`.\n"
        ),
        "palabras_clave": ["offline", "central support", "falla", "cola", "retry", "reintentos", "pendiente"],
    },
    {
        "id": (
            "soporte-prioridades\n"
        ),
        "pregunta": (
            "¿Cuáles son los niveles de prioridad de los tickets de soporte?\n"
        ),
        "respuesta": (
            "Los tickets de soporte en Vigex tienen cuatro niveles de prioridad:\n"
            "\n"
            "• **Baja** — consultas generales, dudas de uso, mejoras sugeridas. Tiempo de respuesta objetivo: 72 horas.\n"
            "• **Normal** — problemas que afectan parcialmente al funcionamiento. Tiempo de respuesta objetivo: 24 horas.\n"
            "• **Alta** — problemas que impiden el uso de una funcionalidad importante. Tiempo de respuesta objetivo: 8 horas.\n"
            "• **Crítica** — el panel está caído, los backups no funcionan o hay pérdida de datos. Tiempo de respuesta objetivo: 2 horas.\n"
            "\n"
            "Para emergencias críticas fuera del horario habitual, usa el canal de contacto urgente indicado en el contrato de soporte.\n"
        ),
        "palabras_clave": ["prioridad", "urgente", "critico", "ticket", "soporte", "sla", "tiempo respuesta"],
    },
    {
        "id": (
            "central-support-que-es\n"
        ),
        "pregunta": (
            "¿Qué es Vigex Central Support y para qué sirve?\n"
        ),
        "respuesta": (
            "**Vigex Central Support** es un componente separado diseñado para proveedores de IT y MSPs (Managed Service Providers) que gestionan Vigex en instalaciones de múltiples clientes. Es un panel centralizado que:\n"
            "\n"
            "• Recibe tickets de soporte de todos los paneles Vigex de sus clientes.\n"
            "• Muestra el estado de salud global de todas las instalaciones (heartbeat).\n"
            "• Permite gestionar el ciclo de vida de tickets: asignar, responder, escalar.\n"
            "• Proporciona un log de auditoría de todas las acciones administrativas.\n"
            "• Gestiona tokens de autenticación por cliente (rotación, revocación).\n"
            "\n"
            "Se instala por separado en `deploy/central-support/`, corre en el puerto 8010 con el servicio systemd `vigex-central`, y usa SQLite como base de datos. Es completamente independiente del panel cliente.\n"
        ),
        "palabras_clave": ["central support", "central", "multicliente", "msp", "proveedor", "tickets", "agregador"],
    },
    {
        "id": (
            "central-support-configurar\n"
        ),
        "pregunta": (
            "¿Cómo conecto el panel de Vigex a un servidor Central Support?\n"
        ),
        "respuesta": (
            "Para conectar el panel cliente a un Central Support:\n"
            "\n"
            "1. En el servidor Central Support, ve a **Clientes → Registrar nuevo cliente** e introduce el ID y nombre de la empresa.\n"
            "2. Central genera un token único. **Cópialo ahora** — no se vuelve a mostrar.\n"
            "3. En el servidor del panel cliente, edita `config.env`:\n"
            "   ```\n"
            "   CENTRAL_SUPPORT_ENABLED=true\n"
            "   CENTRAL_SUPPORT_URL=https://IP_CENTRAL:8010\n"
            "   CENTRAL_SUPPORT_CLIENT_ID=id-del-cliente\n"
            "   CENTRAL_SUPPORT_TOKEN=token-generado\n"
            "   CENTRAL_HEARTBEAT_INTERVAL=300\n"
            "   ```\n"
            "4. Reinicia el panel: `systemctl restart vigex-api`.\n"
            "\n"
            "El panel empezará a enviar heartbeats cada 5 minutos y a sincronizar tickets con el Central Support.\n"
        ),
        "palabras_clave": ["central support", "conectar", "configurar", "token", "heartbeat", "cliente"],
    },
    {
        "id": (
            "central-support-heartbeat\n"
        ),
        "pregunta": (
            "¿Qué es el heartbeat de Vigex Central y cómo funciona?\n"
        ),
        "respuesta": (
            "El **heartbeat** es una señal periódica que el panel cliente envía al servidor Central Support para indicar que está activo y funcionando correctamente.\n"
            "\n"
            "• Se envía cada `CENTRAL_HEARTBEAT_INTERVAL` segundos (por defecto 300 = 5 min).\n"
            "• Incluye información básica: versión, estado de servicios críticos, uso de disco.\n"
            "• Si Central no recibe heartbeat en >10 minutos, marca la instalación como 'Sin contacto' en el panel de salud global.\n"
            "• En el Central Support, la pantalla **Salud global** muestra el estado de todas las instalaciones: verde (OK), amarillo (advertencia reciente), rojo (sin contacto).\n"
            "\n"
            "Para desactivar el heartbeat sin desactivar el resto del soporte central:\n"
            "`CENTRAL_HEARTBEAT_INTERVAL=0` en config.env.\n"
        ),
        "palabras_clave": ["heartbeat", "latido", "central", "activo", "salud", "health", "estado", "contacto"],
    },
    {
        "id": (
            "asistente-ia-que-es\n"
        ),
        "pregunta": (
            "¿Qué es el Asistente IA de Vigex y cómo funciona?\n"
        ),
        "respuesta": (
            "El **Asistente IA** es un chat inteligente integrado en el panel que te ayuda a resolver dudas sobre Vigex, diagnosticar problemas y guiarte en tareas de administración. Usa tecnología **RAG (Retrieval-Augmented Generation)**:\n"
            "\n"
            "1. Tu pregunta se compara con una base de conocimiento interna de Vigex.\n"
            "2. Se recuperan los fragmentos más relevantes de la documentación.\n"
            "3. Esos fragmentos se envían junto a tu pregunta a un modelo de lenguaje (LLM).\n"
            "4. El LLM genera una respuesta contextualizada y precisa.\n"
            "\n"
            "El asistente mantiene el **historial de la conversación** durante la sesión (se limpia al recargar la página o con el botón 'Nueva conversación'). Soporta formato Markdown en las respuestas (negrita, listas, código).\n"
        ),
        "palabras_clave": ["asistente", "ia", "chat", "rag", "inteligencia artificial", "bot", "ayuda", "preguntas"],
    },
    {
        "id": (
            "asistente-proveedores\n"
        ),
        "pregunta": (
            "¿Qué proveedores de IA soporta el Asistente y cuál es el recomendado?\n"
        ),
        "respuesta": (
            "El Asistente IA soporta cinco proveedores de LLM, configurados en `config.env` con `VIGEX_RAG_LLM_PROVIDER`:\n"
            "\n"
            "• **`ollama`** (local, por defecto) — modelo LLM corriendo en tu propio servidor. Sin coste, sin envío de datos externos. Requiere Ollama instalado y modelo descargado.\n"
            "• **`groq`** — Groq API (llama-3.3-70b). Capa gratuita generosa, muy rápido. Recomendado para empezar con cloud.\n"
            "• **`gemini`** — Google Gemini 2.0 Flash. ~0,22€/M tokens, muy económico y potente.\n"
            "• **`openai`** — OpenAI GPT-4o-mini. ~0,15€/M tokens, gran calidad.\n"
            "• **`anthropic`** — Anthropic Claude 3 Haiku. ~0,25€/M tokens.\n"
            "\n"
            "**Recomendación**: Groq para entornos cloud (rápido y gratuito en la mayoría de casos), Ollama para máxima privacidad. Para uso intensivo, Gemini o OpenAI ofrecen el mejor equilibrio calidad/precio.\n"
        ),
        "palabras_clave": ["proveedores", "ollama", "groq", "gemini", "openai", "anthropic", "ia", "modelo", "proveedor"],
    },
    {
        "id": (
            "asistente-configurar-groq\n"
        ),
        "pregunta": (
            "¿Cómo configuro el Asistente IA con Groq?\n"
        ),
        "respuesta": (
            "Groq ofrece una capa gratuita generosa y es el proveedor más rápido disponible. Pasos para configurarlo:\n"
            "\n"
            "1. Crea una cuenta en `console.groq.com` y genera una API Key.\n"
            "2. Edita `config.env` en el servidor:\n"
            "   ```\n"
            "   VIGEX_RAG_LLM_PROVIDER=groq\n"
            "   GROQ_API_KEY=gsk_tu_clave_aqui\n"
            "   VIGEX_RAG_GROQ_MODEL=llama-3.3-70b-versatile\n"
            "   ```\n"
            "3. Reinicia el panel: `systemctl restart vigex-api`\n"
            "4. Entra al Asistente IA — verás el badge 'Groq' en la esquina.\n"
            "\n"
            "La clave gratuita permite unas 100 peticiones/día aproximadamente, lo que es más que suficiente para uso normal de soporte. El modelo llama-3.3-70b da respuestas de alta calidad en <3 segundos.\n"
        ),
        "palabras_clave": ["groq", "configurar", "api key", "llama", "rápido", "gratis", "asistente"],
    },
    {
        "id": (
            "asistente-configurar-ollama\n"
        ),
        "pregunta": (
            "¿Cómo configuro el Asistente IA con Ollama (modelo local)?\n"
        ),
        "respuesta": (
            "Ollama permite ejecutar el modelo LLM en tu propio servidor, sin coste y sin enviar datos a terceros. Requisito: mínimo 4 GB RAM libre (6 GB recomendado).\n"
            "\n"
            "Pasos:\n"
            "1. Instala Ollama en el servidor del panel:\n"
            "   `curl -fsSL https://ollama.com/install.sh | sh`\n"
            "2. Descarga el modelo (elige según RAM disponible):\n"
            "   - 3 GB RAM: `ollama pull llama3.2:3b`\n"
            "   - 5 GB RAM: `ollama pull mistral`\n"
            "   - 8 GB RAM: `ollama pull llama3.1:8b`\n"
            "3. Configura en `config.env`:\n"
            "   ```\n"
            "   VIGEX_RAG_LLM_PROVIDER=ollama\n"
            "   VIGEX_RAG_OLLAMA_URL=http://localhost:11434\n"
            "   VIGEX_RAG_OLLAMA_MODEL=llama3.2:3b\n"
            "   ```\n"
            "4. Reinicia: `systemctl restart vigex-api`\n"
            "\n"
            "⚠️ Con CPU (sin GPU), cada respuesta puede tardar 30-180 segundos según el modelo. Para respuestas rápidas con privacidad, combina Ollama para la BD de conocimiento local + Groq para la generación.\n"
        ),
        "palabras_clave": ["ollama", "local", "offline", "instalar", "modelo", "mistral", "llama", "ram"],
    },
    {
        "id": (
            "asistente-slow\n"
        ),
        "pregunta": (
            "El Asistente IA tarda mucho en responder. ¿Por qué?\n"
        ),
        "respuesta": (
            "La velocidad de respuesta depende del proveedor configurado:\n"
            "\n"
            "• **Ollama con CPU** — puede tardar 30-180 segundos. Es normal si no hay GPU. Solución: cambia a Groq o Gemini para respuestas instantáneas.\n"
            "• **Ollama con GPU** — <10 segundos. Si tienes GPU, actívala: Ollama la usa automáticamente.\n"
            "• **Groq** — normalmente <3 segundos. Si tarda más, puede ser rate limiting.\n"
            "• **Gemini / OpenAI / Anthropic** — 2-10 segundos según la carga del proveedor.\n"
            "\n"
            "El timeout configurado es de 300 segundos para Ollama y 30 segundos para APIs cloud. Si ves 'Tiempo de espera agotado', aumenta el timeout en `config.env` o cambia de proveedor. Para uso en producción con tiempo de respuesta crítico, **Groq es la opción más rápida** actualmente.\n"
        ),
        "palabras_clave": ["lento", "tarda", "timeout", "lentitud", "respuesta", "asistente", "ollama", "velocidad"],
    },
    {
        "id": (
            "asistente-historial\n"
        ),
        "pregunta": (
            "¿El Asistente IA recuerda conversaciones anteriores?\n"
        ),
        "respuesta": (
            "El Asistente IA mantiene el **historial de la conversación actual** en la sesión del navegador (sessionStorage), no en el servidor. Esto significa:\n"
            "\n"
            "• ✅ Dentro de la misma sesión/pestaña, el asistente recuerda los últimos 6 turnos (12 mensajes: 6 de usuario + 6 de asistente).\n"
            "• ❌ Si recargas la página, abres una nueva pestaña o cierras el navegador, el historial se pierde.\n"
            "• El botón **'Nueva conversación'** limpia el historial intencionalmente.\n"
            "\n"
            "Esta decisión de diseño es deliberada: no se almacenan conversaciones en el servidor para proteger la privacidad. Las conversaciones nunca se guardan en ningún fichero ni base de datos del panel.\n"
        ),
        "palabras_clave": ["historial", "memoria", "recuerda", "conversación", "sesión", "privacidad", "limpiar"],
    },
    {
        "id": (
            "terminal-uso\n"
        ),
        "pregunta": (
            "¿Cómo funciona la Terminal integrada de Vigex?\n"
        ),
        "respuesta": (
            "La **Terminal** de Vigex es una terminal web que permite ejecutar comandos en el servidor remoto mediante SSH seguro. Está disponible para usuarios con el permiso `terminal` activado.\n"
            "\n"
            "Características:\n"
            "• Ejecuta comandos en tiempo real en el servidor configurado (`SERVICIOS_HOST`).\n"
            "• Usa el mismo mecanismo SSH seguro que el resto del panel (clave ed25519, BatchMode, StrictHostKeyChecking).\n"
            "• Los comandos disponibles están limitados a una lista blanca — no es una shell arbitraria por razones de seguridad.\n"
            "• El historial de comandos ejecutados queda registrado en el log de auditoría.\n"
            "\n"
            "⚠️ **Seguridad**: otorga el permiso `terminal` solo a usuarios de confianza. Aunque los comandos están limitados, la Terminal da más poder de acción que el resto de módulos.\n"
        ),
        "palabras_clave": ["terminal", "consola", "comandos", "ssh", "web", "ejecutar", "shell"],
    },
    {
        "id": (
            "panel-no-arranca\n"
        ),
        "pregunta": (
            "El panel no arranca o aparece un error 500.\n"
        ),
        "respuesta": (
            "Pasos de diagnóstico:\n"
            "\n"
            "1. `systemctl status vigex-api` — comprueba si el servicio está activo.\n"
            "2. `journalctl -u vigex-api -n 100 --no-pager` — busca el error concreto.\n"
            "3. Comprueba que `config.env` existe y tiene `SECRET_KEY` y `ADMIN_PASSWORD`:\n"
            "   `ls -la /opt/vigex/api/config.env`\n"
            "4. `df -h /opt/vigex` — verifica que no esté el disco lleno.\n"
            "5. `python3 -c \"import fastapi, uvicorn, pymysql\"` — verifica dependencias.\n"
            "6. Si el problema es de importación de Python, reinstala dependencias:\n"
            "   `cd /opt/vigex/api && ./venv/bin/pip install -r requirements.txt`\n"
            "\n"
            "Si el error persiste, abre un ticket en el módulo de soporte con el texto completo del error de `journalctl`.\n"
        ),
        "palabras_clave": ["panel", "arrancar", "500", "error", "caído", "blanco", "fallo", "inicio", "systemctl"],
    },
    {
        "id": (
            "error-500-interno\n"
        ),
        "pregunta": (
            "Aparece un error 500 en una página específica del panel.\n"
        ),
        "respuesta": (
            "Un error 500 en una página concreta (no en todo el panel) suele indicar un problema de conectividad con un servicio remoto. Diagnóstico según la página:\n"
            "\n"
            "• **Error 500 en Copias o Restauración** → problema SSH con el servidor de backups. Prueba la conexión SSH manualmente.\n"
            "• **Error 500 en Logs** → problema de conexión con la BD MariaDB. Comprueba variables `LOGS_DB_*` en config.env.\n"
            "• **Error 500 en Servicios** → problema SSH con `SERVICIOS_HOST`. Verifica que el host está accesible.\n"
            "• **Error 500 en Monitoreo** → URL de Grafana/Cacti incorrecta o servicio caído.\n"
            "\n"
            "Revisa los logs del panel para el error exacto:\n"
            "`journalctl -u vigex-api -n 50 --no-pager`\n"
        ),
        "palabras_clave": ["500", "error interno", "página", "fallo", "specific", "roto", "interno"],
    },
    {
        "id": (
            "vigex-version-check\n"
        ),
        "pregunta": (
            "¿Cómo sé qué versión de Vigex tengo instalada?\n"
        ),
        "respuesta": (
            "La versión aparece en el **footer del panel** (parte inferior del dashboard). También puedes verla en el servidor:\n"
            "\n"
            "`head -5 /opt/vigex/api/main.py`\n"
            "\n"
            "o buscando en config.env:\n"
            "`grep VIGEX_VERSION /opt/vigex/api/config.env`\n"
            "\n"
            "La versión actual del producto es **v1.0-rc1**. Para comparar con la última versión disponible, consulta el fichero `docs/ROADMAP.md` del repositorio o la página oficial de Vigex.\n"
        ),
        "palabras_clave": ["versión", "version", "instalada", "vigex", "actual", "numero", "comprobar"],
    },
    {
        "id": (
            "servicio-vigex-reiniciar\n"
        ),
        "pregunta": (
            "¿Cómo reinicio el servicio de Vigex en el servidor?\n"
        ),
        "respuesta": (
            "El panel Vigex corre como servicio systemd `vigex-api`. Comandos de gestión:\n"
            "\n"
            "• **Reiniciar** (tras cambios en config.env): `systemctl restart vigex-api`\n"
            "• **Ver estado**: `systemctl status vigex-api`\n"
            "• **Ver logs en tiempo real**: `journalctl -u vigex-api -f`\n"
            "• **Detener**: `systemctl stop vigex-api`\n"
            "• **Iniciar**: `systemctl start vigex-api`\n"
            "• **Habilitar arranque automático**: `systemctl enable vigex-api`\n"
            "\n"
            "El servicio tiene `Restart=always` y `RestartSec=3`, por lo que si Uvicorn cae por cualquier motivo, systemd lo levanta automáticamente a los 3 segundos. El panel Central Support usa el servicio `vigex-central` con los mismos comandos.\n"
        ),
        "palabras_clave": ["reiniciar", "restart", "servicio", "systemd", "vigex-api", "uvicorn", "parar", "iniciar"],
    },
    {
        "id": (
            "debug-logs-panel\n"
        ),
        "pregunta": (
            "¿Cómo veo los logs del propio panel de Vigex para diagnosticar problemas?\n"
        ),
        "respuesta": (
            "Los logs del panel Vigex se gestionan con systemd journal. Comandos útiles:\n"
            "\n"
            "• **Últimas 100 líneas**: `journalctl -u vigex-api -n 100 --no-pager`\n"
            "• **En tiempo real**: `journalctl -u vigex-api -f`\n"
            "• **Logs de hoy**: `journalctl -u vigex-api --since today`\n"
            "• **Logs con nivel de error**: `journalctl -u vigex-api -p err`\n"
            "• **Logs del último arranque**: `journalctl -u vigex-api -b`\n"
            "\n"
            "Para el servicio Central Support: sustituye `vigex-api` por `vigex-central`.\n"
            "\n"
            "Si necesitas más detalle, puedes aumentar el nivel de log de Uvicorn añadiendo `--log-level debug` al ExecStart del servicio systemd (edita `/etc/systemd/system/vigex-api.service` y recarga con `systemctl daemon-reload && systemctl restart vigex-api`).\n"
        ),
        "palabras_clave": ["logs", "journal", "journalctl", "diagnóstico", "debug", "error", "panel", "ver"],
    },
    {
        "id": (
            "bd-instalar\n"
        ),
        "pregunta": (
            "¿Cómo se instala y configura la base de datos de Vigex?\n"
        ),
        "respuesta": (
            "La base de datos de logs usa **MariaDB**. La instalación se hace con el script incluido en el repositorio:\n"
            "\n"
            "`sudo bash deploy/db/install_vigex_db.sh`\n"
            "\n"
            "El script realiza automáticamente:\n"
            "• Instalación de MariaDB si no está presente.\n"
            "• Creación de la base de datos `vigex_logs`.\n"
            "• Creación de usuarios con los permisos mínimos necesarios:\n"
            "  - `vigex_logs` (solo SELECT para el panel).\n"
            "  - `vigex_backup` (solo SELECT para dumps de backup).\n"
            "  - `vigex_restore` (escritura para restauración).\n"
            "• Creación de la tabla `logs` con los índices necesarios.\n"
            "• Configuración del firewall para permitir acceso solo desde la IP del panel.\n"
            "\n"
            "La IP del servidor de BD se configura en `LOGS_DB_HOST` en `config.env` del panel.\n"
        ),
        "palabras_clave": ["base de datos", "mariadb", "mysql", "instalar", "bd", "logs", "script"],
    },
    {
        "id": (
            "bd-backup-mysql\n"
        ),
        "pregunta": (
            "¿Cómo se hace el backup de la base de datos MariaDB?\n"
        ),
        "respuesta": (
            "El backup de MariaDB se realiza mediante `mysqldump` ejecutado remotamente por el script `backups_api.sh` en el servidor de backups. El proceso:\n"
            "\n"
            "1. El panel envía la petición de backup al servidor de backups vía SSH.\n"
            "2. `backups_api.sh` ejecuta:\n"
            "   `mysqldump -h IP_DB -u vigex_backup -p vigex_logs > backup_TIMESTAMP.sql`\n"
            "3. El fichero SQL se comprime con gzip.\n"
            "4. Se calcula el SHA256 del archivo comprimido.\n"
            "5. El registro del backup (ruta, fecha, tamaño, hash) se guarda en la BD de Vigex.\n"
            "\n"
            "Configuración en `config.env`:\n"
            "• `BACKUP_DB_HOST` — IP del servidor de BD.\n"
            "• `BACKUP_DB_NAME` / `BACKUP_DB_USER` / `BACKUP_DB_PASS` — acceso a la BD.\n"
            "• `BACKUP_OUTPUT_DIR` — directorio donde se guardan los dumps.\n"
            "• `BACKUP_RETENTION_KEEP` — número de copias a mantener.\n"
        ),
        "palabras_clave": ["backup", "mariadb", "mysqldump", "bd", "base de datos", "dump", "sql"],
    },
    {
        "id": (
            "proxy-nginx\n"
        ),
        "pregunta": (
            "¿Cómo funciona el proxy nginx de Vigex?\n"
        ),
        "respuesta": (
            "Vigex incluye un instalador de proxy nginx (`deploy/proxy/install_vigex_proxy.sh`) que configura nginx como reverse proxy delante de Uvicorn:\n"
            "\n"
            "• nginx escucha en el puerto 443 (HTTPS) y 80 (redirige a HTTPS).\n"
            "• Las peticiones HTTPS se pasan al Uvicorn local en el puerto 8000.\n"
            "• nginx gestiona la terminación TLS (certificado SSL).\n"
            "• El certificado autofirmado se genera automáticamente durante la instalación.\n"
            "• Para certificado válido con Let's Encrypt, instala certbot después:\n"
            "  `sudo certbot --nginx -d tu-dominio.com`\n"
            "\n"
            "El fichero de configuración de nginx está en:\n"
            "`/etc/nginx/sites-available/vigex`\n"
            "\n"
            "Para aplicar cambios en nginx: `sudo nginx -t && sudo systemctl reload nginx`\n"
        ),
        "palabras_clave": ["nginx", "proxy", "reverse proxy", "https", "puerto", "443", "80", "uvicorn"],
    },
    {
        "id": (
            "dominio-personalizado\n"
        ),
        "pregunta": (
            "¿Puedo acceder a Vigex con un dominio personalizado?\n"
        ),
        "respuesta": (
            "Sí. Para acceder con un dominio (ej: `vigex.tuempresa.com`):\n"
            "\n"
            "1. Apunta el dominio a la IP del servidor en tu proveedor DNS (registro A: `vigex.tuempresa.com → IP_SERVIDOR`).\n"
            "2. Espera la propagación DNS (5-30 minutos).\n"
            "3. Instala certbot para HTTPS real:\n"
            "   `sudo apt install certbot python3-certbot-nginx`\n"
            "   `sudo certbot --nginx -d vigex.tuempresa.com`\n"
            "4. Certbot modifica nginx automáticamente y añade renovación automática.\n"
            "5. Activa HTTPS estricto en `config.env`:\n"
            "   `VIGEX_SESSION_HTTPS_ONLY=true`\n"
            "6. Reinicia: `systemctl restart vigex-api`\n"
            "\n"
            "A partir de este momento puedes acceder a `https://vigex.tuempresa.com` con certificado válido y sin advertencia del navegador.\n"
        ),
        "palabras_clave": ["dominio", "dns", "subdominio", "personalizado", "https", "certbot", "letsencrypt", "acceso"],
    },
    {
        "id": (
            "integracion-jira\n"
        ),
        "pregunta": (
            "¿Cómo integro Vigex con Jira Service Management?\n"
        ),
        "respuesta": (
            "Vigex puede enviar tickets de soporte automáticamente a **Jira Service Management** (o cualquier sistema de tickets compatible con webhooks JSON) cuando se crean tickets en el panel.\n"
            "\n"
            "Configuración en `config.env`:\n"
            "```\n"
            "JIRA_WEBHOOK_URL=https://tu-instancia.atlassian.net/rest/webhooks/1.0/webhook/ID\n"
            "JIRA_WEBHOOK_TIMEOUT=5\n"
            "```\n"
            "\n"
            "Cuando dejas `JIRA_WEBHOOK_URL` en blanco, la integración está desactivada. El webhook envía un POST con JSON que incluye: ID del ticket, título, descripción, prioridad, módulo afectado y fecha de creación. Es compatible con cualquier herramienta que acepte webhooks: GitHub Issues, GitLab, Trello, Notion, Zapier, etc. Reinicia el panel tras configurar.\n"
        ),
        "palabras_clave": ["jira", "webhook", "integración", "tickets", "service management", "github", "zapier"],
    },
    {
        "id": (
            "uso-diario-recomendaciones\n"
        ),
        "pregunta": (
            "¿Qué tareas debo revisar diariamente en el panel de Vigex?\n"
        ),
        "respuesta": (
            "Checklist de revisión diaria recomendada:\n"
            "\n"
            "✅ **Dashboard** — comprueba que el estado general es verde.\n"
            "✅ **Copias** — verifica que la última copia automática fue exitosa (color verde).\n"
            "✅ **Servicios** — asegúrate de que todos los servicios críticos están activos.\n"
            "✅ **Alertas** — revisa si hay alertas no atendidas.\n"
            "✅ **Disco** — comprueba que el uso no supera el 80%.\n"
            "\n"
            "Tareas semanales recomendadas:\n"
            "📋 Revisar los **Logs** en busca de errores o patrones inusuales.\n"
            "📋 Revisar el **Informe semanal** cuando llegue por email.\n"
            "📋 Verificar la integridad de los backups con **Copias → Integridad**.\n"
            "\n"
            "Tareas mensuales:\n"
            "🔄 Probar una restauración en entorno de test.\n"
            "🔄 Revisar y limpiar backups muy antiguos si el espacio es limitado.\n"
        ),
        "palabras_clave": ["diario", "checklist", "revisar", "tareas", "rutina", "diariamente", "semanal"],
    },
    {
        "id": (
            "login-sesion-expira\n"
        ),
        "pregunta": (
            "La sesión expira constantemente y tengo que volver a hacer login.\n"
        ),
        "respuesta": (
            "Si la sesión expira demasiado rápido, ajusta estos valores en `config.env`:\n"
            "\n"
            "• `VIGEX_SESSION_MAX_AGE=28800` — duración máxima (segundos). Por defecto 8 horas. Auméntalo si necesitas sesiones más largas (ej: 43200 = 12 horas, 86400 = 24 horas).\n"
            "\n"
            "• `VIGEX_AUTO_LOGOUT_MINUTES=60` — minutos de inactividad antes del logout. Auméntalo o ponlo a `0` para desactivar el auto-logout por inactividad.\n"
            "\n"
            "También puede ocurrir que la sesión expire si:\n"
            "• Cambias `SECRET_KEY` en config.env (invalida todas las sesiones activas).\n"
            "• Reinicias el servicio vigex-api (las sesiones en memoria se pierden).\n"
            "\n"
            "Reinicia el servicio tras modificar: `systemctl restart vigex-api`.\n"
        ),
        "palabras_clave": ["sesión", "expira", "logout", "login", "volver", "tiempo", "desconectar"],
    },
    {
        "id": (
            "dos-paneles-misma-cuenta\n"
        ),
        "pregunta": (
            "¿Puedo abrir el panel en varios navegadores o pestañas a la vez?\n"
        ),
        "respuesta": (
            "Sí. Vigex soporta varias sesiones simultáneas. Puedes:\n"
            "\n"
            "• Abrir el panel en diferentes pestañas del mismo navegador con la misma sesión.\n"
            "• Abrir el panel en diferentes navegadores o dispositivos con sesiones independientes.\n"
            "• Tener múltiples usuarios conectados simultáneamente (cada uno con su sesión).\n"
            "\n"
            "No hay límite técnico de sesiones simultáneas por usuario. Si usas una sesión en varios dispositivos y cierras sesión en uno, los demás siguen activos hasta que expiren por tiempo de inactividad o se haga logout explícito.\n"
            "\n"
            "Para cerrar todas las sesiones activas de un usuario, cambia su contraseña desde **Admin → Usuarios** — esto invalida todas las sesiones existentes.\n"
        ),
        "palabras_clave": ["varias pestañas", "múltiples", "sesiones", "simultáneo", "navegador", "dispositivos"],
    },
    {
        "id": (
            "modo-oscuro\n"
        ),
        "pregunta": (
            "¿El panel tiene modo oscuro?\n"
        ),
        "respuesta": (
            "Sí. El panel de Vigex incluye **modo oscuro** que puedes activar con el botón de luna/sol en la cabecera del panel (esquina superior derecha). La preferencia se guarda en `localStorage` del navegador, por lo que persiste entre recargas de página. También respeta automáticamente la preferencia del sistema operativo si no has seleccionado manualmente un tema.\n"
            "\n"
            "El modo oscuro está disponible en todas las secciones del panel, incluyendo el Asistente IA, Copias, Logs, Servicios, etc. El panel Central Support también incluye modo oscuro independiente.\n"
        ),
        "palabras_clave": ["modo oscuro", "dark mode", "tema", "oscuro", "claro", "apariencia", "luna"],
    },
    {
        "id": (
            "exportar-datos\n"
        ),
        "pregunta": (
            "¿Puedo exportar datos del panel (logs, backups, informes)?\n"
        ),
        "respuesta": (
            "Vigex ofrece varias opciones de exportación:\n"
            "\n"
            "• **Logs** — exporta logs filtrados a CSV desde la pantalla de Logs (botón 'Exportar CSV').\n"
            "• **Informes** — los informes generados se guardan como Markdown en el servidor (`/opt/vigex/api/reports/`) y se envían por email en formato texto.\n"
            "• **Lista de backups** — exporta el historial de copias a CSV desde la pantalla de Copias.\n"
            "• **Tickets de soporte** — los tickets se pueden exportar desde el módulo de Soporte en formato CSV para análisis externo.\n"
            "\n"
            "Para exportación masiva de datos o integraciones con BI (Power BI, Grafana, etc.), puedes acceder directamente a la BD MariaDB con el usuario de solo lectura `vigex_logs` desde herramientas externas.\n"
        ),
        "palabras_clave": ["exportar", "csv", "datos", "descargar", "logs", "informes", "backup", "historial"],
    },
    {
        "id": (
            "ip-servidor-cambio\n"
        ),
        "pregunta": (
            "Cambié la IP de un servidor. ¿Qué tengo que actualizar en Vigex?\n"
        ),
        "respuesta": (
            "Si cambia la IP de alguno de los servidores gestionados por Vigex:\n"
            "\n"
            "1. **Edita `config.env`** en el servidor del panel:\n"
            "   - Actualiza `SERVICIOS_HOST`, `BACKUPS_HOST` o `LOGS_DB_HOST` según corresponda.\n"
            "   - Actualiza `VIGEX_SSH_ALLOWED_HOSTS` con la nueva IP.\n"
            "\n"
            "2. **Actualiza el known_hosts SSH**: la clave host del servidor puede haber cambiado.\n"
            "   Elimina la entrada antigua: `ssh-keygen -R IP_ANTIGUA -f /opt/vigex/api/.ssh/known_hosts_vigex`\n"
            "   Añade la nueva: `sudo -u vigex ssh-keyscan -H IP_NUEVA >> /opt/vigex/api/.ssh/known_hosts_vigex`\n"
            "\n"
            "3. **Si cambió el servidor de BD**: actualiza también el firewall en el servidor de BD para permitir conexiones desde la nueva IP del panel.\n"
            "\n"
            "4. **Reinicia el panel**: `systemctl restart vigex-api`\n"
            "\n"
            "5. **Prueba la conexión** lanzando una copia manual y verificando los logs.\n"
        ),
        "palabras_clave": ["ip", "cambio", "servidor", "mover", "actualizar", "known_hosts", "ip nueva"],
    },
    {
        "id": (
            "acceso-externo-red\n"
        ),
        "pregunta": (
            "¿Puedo acceder al panel de Vigex desde fuera de la red local?\n"
        ),
        "respuesta": (
            "Sí, pero con precauciones de seguridad. El panel escucha en el puerto 443 (HTTPS) a través de nginx. Para acceso externo:\n"
            "\n"
            "**Opción A — Acceso directo (menos recomendado)**:\n"
            "• Abre el puerto 443 en el firewall del servidor y en el router.\n"
            "• Configura un dominio con certbot para HTTPS válido.\n"
            "• Asegúrate de tener anti-fuerza bruta activado.\n"
            "\n"
            "**Opción B — VPN (recomendado)**:\n"
            "• Instala WireGuard o OpenVPN en el servidor.\n"
            "• Accede al panel solo a través de la VPN.\n"
            "• El panel no queda expuesto a internet directamente.\n"
            "\n"
            "**Opción C — Túnel SSH**:\n"
            "• `ssh -L 8000:localhost:8000 usuario@IP_SERVIDOR`\n"
            "• Accede a `http://localhost:8000` en tu navegador local.\n"
            "\n"
            "La opción VPN es la más segura para entornos empresariales.\n"
        ),
        "palabras_clave": ["acceso externo", "remoto", "internet", "vpn", "firewall", "red", "fuera", "exterior"],
    },
    {
        "id": (
            "desinstalar-vigex\n"
        ),
        "pregunta": (
            "¿Cómo desinstalo Vigex completamente de un servidor?\n"
        ),
        "respuesta": (
            "Para desinstalar Vigex completamente:\n"
            "\n"
            "1. **Detén y elimina el servicio systemd**:\n"
            "   `systemctl stop vigex-api && systemctl disable vigex-api`\n"
            "   `rm /etc/systemd/system/vigex-api.service`\n"
            "   `systemctl daemon-reload`\n"
            "\n"
            "2. **Elimina los ficheros del panel**:\n"
            "   `rm -rf /opt/vigex/api`\n"
            "\n"
            "3. **Elimina el proxy nginx** (si lo instalaste con Vigex):\n"
            "   `rm /etc/nginx/sites-enabled/vigex /etc/nginx/sites-available/vigex`\n"
            "   `systemctl reload nginx`\n"
            "\n"
            "4. **Elimina la BD** (si quieres borrar los logs):\n"
            "   `mysql -u root -e \"DROP DATABASE vigex_logs;\"`\n"
            "\n"
            "El script de desinstalación incluido en el repositorio automatiza estos pasos:\n"
            "`sudo bash deploy/api/uninstall_vigex_api.sh`\n"
        ),
        "palabras_clave": ["desinstalar", "eliminar", "borrar", "quitar", "uninstall", "limpiar", "completo"],
    },
]


def _buscar_faq(query: str, contexto_url: str = "") -> list[dict]:
    """Busca entradas FAQ por palabras clave (R-085: algoritmo mejorado).

    Mejoras sobre R-070:
    - Normalización de sinónimos antes de puntuar
    - Eliminación de stopwords
    - Bonus por coincidencia de la frase completa (2 pts extra)
    - Bonus por coincidencia de palabra exacta en palabra_clave (3 pts)
    - Descuento parcial para palabras cortas (< 3 chars)
    - contexto_url: boost de 1 pto si la URL actual tiene relación con la entrada
    """
    if not query:
        return _FAQ_ENTRIES

    # Normalizar query
    palabras_norm = _normalizar_palabras(query)
    q_norm = " ".join(palabras_norm)

    if not palabras_norm:
        return _FAQ_ENTRIES

    resultados = []

    for entry in _FAQ_ENTRIES:
        puntos = 0

        # Texto plano de búsqueda (normalizado)
        texto_full = (
            entry["pregunta"].lower()
            + " "
            + entry["respuesta"].lower()
            + " "
            + " ".join(entry["palabras_clave"])
        )
        texto_norm_palabras = _normalizar_palabras(texto_full)
        texto_norm_str = " ".join(texto_norm_palabras)
        kws_norm = [_FAQ_SINONIMOS.get(k, k) for k in entry["palabras_clave"]]

        for p in palabras_norm:
            if len(p) < 2:
                continue
            if p in texto_norm_str:
                puntos += 1
            if p in kws_norm:
                puntos += 3  # coincidencia exacta en keyword = mayor peso

        # Bonus si la frase completa aparece en el texto
        if len(q_norm) > 4 and q_norm in texto_norm_str:
            puntos += 2

        # Boost por contexto de página actual (10.4 / R-085)
        if contexto_url:
            url_l = contexto_url.lower()
            entry_id = entry["id"]
            if (("backup" in url_l or "copi" in url_l) and "backup" in entry_id):
                puntos += 1
            elif ("servicio" in url_l and "servicio" in entry_id):
                puntos += 1
            elif ("log" in url_l and "log" in entry_id):
                puntos += 1
            elif ("alerta" in url_l and "alerta" in entry_id):
                puntos += 1

        if puntos > 0:
            resultados.append({"puntos": puntos, "entry": entry})

    resultados.sort(key=lambda x: x["puntos"], reverse=True)
    return [r["entry"] for r in resultados]


@app.get("/soporte/faq")
def soporte_faq(request: Request, q: str = "", desde: str = ""):
    """Redirige al nuevo Asistente IA (R-090). Mantenemos la ruta por compatibilidad."""
    return RedirectResponse(url="/asistente", status_code=301)


@app.get("/api/soporte/faq")
def api_soporte_faq(request: Request, q: str = "", desde: str = ""):
    """API FAQ legacy — devuelve resultados en JSON para compatibilidad. R-070 / R-085"""
    if not is_authenticated(request):
        return JSONResponse({"error": "no autenticado"}, status_code=401)
    resultados = _buscar_faq(q, contexto_url=desde)
    return JSONResponse({"resultados": resultados, "total": len(resultados)})


# =============================================================================
# R-090 — Asistente IA con RAG
# Fase 1: Ollama local + búsqueda semántica sobre FAQ (sin deps extra)
# Fase 2: VIGEX_RAG_LLM_PROVIDER=anthropic para subir de calidad
# =============================================================================

# R-090-sec: rate limiter en memoria — {username: [timestamps]}
# Se limpia automáticamente en cada comprobación (sliding window).
_rag_rate_buckets: dict[str, list[float]] = {}

def _rag_check_rate_limit(username: str) -> bool:
    """Devuelve True si el usuario está DENTRO del límite (puede continuar).
    Devuelve False si ha superado RAG_RATE_LIMIT_REQS en RAG_RATE_LIMIT_WINDOW segundos.
    """
    import time as _time
    now = _time.monotonic()
    window_start = now - RAG_RATE_LIMIT_WINDOW
    bucket = _rag_rate_buckets.get(username, [])
    # Descartar timestamps fuera de la ventana
    bucket = [t for t in bucket if t > window_start]
    if len(bucket) >= RAG_RATE_LIMIT_REQS:
        _rag_rate_buckets[username] = bucket
        return False
    bucket.append(now)
    _rag_rate_buckets[username] = bucket
    return True

_RAG_SYSTEM_PROMPT = (
    "Eres el asistente técnico de Vigex, un panel de gestión de servidores Linux para PYMEs. "
    "Ayudas con backups, logs, servicios, alertas, monitoreo y recuperación ante desastres. "
    "Responde SIEMPRE en español, de forma clara y concisa. "
    "Usa listas con guion y bloques de código cuando mejore la comprensión. "
    "Si la documentación proporcionada no cubre la pregunta, dilo con honestidad "
    "y sugiere abrir un ticket de soporte desde el menú lateral. "
    "Nunca inventes comandos ni rutas que no aparezcan en la documentación."
)


def _rag_build_context(query: str) -> str:
    """Recupera los fragmentos más relevantes del conocimiento usando el buscador FAQ."""
    entradas = _buscar_faq(query)[:RAG_TOP_K]
    if not entradas:
        return ""
    partes = []
    for e in entradas:
        partes.append(f"P: {e.get('pregunta', '')}\nR: {e.get('respuesta', '')}")
    return "\n\n---\n\n".join(partes)


def _rag_call_ollama(system: str, messages: list[dict]) -> str:
    """Llama al LLM local vía Ollama API (urllib stdlib, sin dependencias extra)."""
    import urllib.request
    import urllib.error

    payload = json.dumps({
        "model": RAG_OLLAMA_MODEL,
        "messages": [{"role": "system", "content": system}] + messages,
        "stream": False,
        "options": {
            "num_predict": RAG_MAX_TOKENS,
            "temperature": 0.25,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
        },
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{RAG_OLLAMA_URL}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:  # R-090: CPU inference puede tardar >2 min
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("message", {}).get("content", "Sin respuesta del modelo.")
    except urllib.error.URLError:
        return (
            "⚠️ No se pudo conectar con Ollama. "
            f"Asegúrate de que el servicio está corriendo en `{RAG_OLLAMA_URL}`: "
            "`ollama serve` · Para instalar Ollama: https://ollama.com"
        )
    except Exception as exc:
        return f"⚠️ Error al llamar al modelo local: {exc}"


def _rag_call_anthropic(system: str, messages: list[dict]) -> str:
    """Llama a Claude API. Requiere: pip install anthropic + ANTHROPIC_API_KEY."""
    if not RAG_ANTHROPIC_KEY:
        return "⚠️ ANTHROPIC_API_KEY no configurada en config.env."
    try:
        import anthropic as _sdk  # type: ignore
        client = _sdk.Anthropic(api_key=RAG_ANTHROPIC_KEY)
        response = client.messages.create(
            model=RAG_ANTHROPIC_MODEL,
            max_tokens=RAG_MAX_TOKENS,
            system=system,
            messages=messages,
        )
        return response.content[0].text
    except ImportError:
        return "⚠️ Paquete `anthropic` no instalado. Ejecuta: `pip install anthropic`"
    except Exception as exc:
        return f"⚠️ Error al llamar a Claude API: {exc}"


def _rag_call_gemini(system: str, messages: list[dict]) -> str:
    """Llama a Gemini API (urllib stdlib, sin dependencias extra). R-090."""
    if not RAG_GEMINI_KEY:
        return "⚠️ GOOGLE_API_KEY no configurada en config.env."
    import urllib.request, urllib.error

    # Gemini usa formato propio: system_instruction + contents con roles user/model
    contents = []
    for m in messages:
        role = "model" if m["role"] == "assistant" else "user"
        contents.append({"role": role, "parts": [{"text": m["content"]}]})

    payload = json.dumps({
        "system_instruction": {"parts": [{"text": system}]},
        "contents": contents,
        "generationConfig": {
            "maxOutputTokens": RAG_MAX_TOKENS,
            "temperature": 0.25,
            "topP": 0.9,
        },
    }).encode("utf-8")

    # Las keys AQ.* (formato nuevo de AI Studio) usan Bearer auth.
    # Las keys AIzaSy* (formato clásico) usan ?key= en la URL.
    # Probamos Bearer primero; si falla 401/403 reintentamos con ?key=.
    base_url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
                f"{RAG_GEMINI_MODEL}:generateContent")

    def _try(url: str, extra_headers: dict) -> str:
        hdrs = {"Content-Type": "application/json"}
        hdrs.update(extra_headers)
        req = urllib.request.Request(url, data=payload, headers=hdrs, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"]

    # Intento 1: Bearer token (keys AQ.* / OAuth)
    try:
        return _try(base_url, {"Authorization": f"Bearer {RAG_GEMINI_KEY}"})
    except urllib.error.HTTPError as exc1:
        if exc1.code not in (401, 403):
            body = exc1.read().decode("utf-8", errors="replace")[:300]
            return f"⚠️ Error Gemini API ({exc1.code}): {body}"
        # Intento 2: ?key= clásico (keys AIzaSy*)
        try:
            return _try(f"{base_url}?key={RAG_GEMINI_KEY}", {})
        except urllib.error.HTTPError as exc2:
            body = exc2.read().decode("utf-8", errors="replace")[:300]
            return f"⚠️ Error Gemini API ({exc2.code}): {body}"
    except Exception as exc:
        return f"⚠️ Error al llamar a Gemini: {exc}"


def _rag_call_openai(system: str, messages: list[dict]) -> str:
    """Llama a OpenAI API (urllib stdlib). R-090."""
    if not RAG_OPENAI_KEY:
        return "⚠️ OPENAI_API_KEY no configurada en config.env."
    import urllib.request, urllib.error

    msgs = [{"role": "system", "content": system}] + messages
    payload = json.dumps({
        "model": RAG_OPENAI_MODEL,
        "messages": msgs,
        "max_tokens": RAG_MAX_TOKENS,
        "temperature": 0.25,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {RAG_OPENAI_KEY}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:300]
        return f"⚠️ Error OpenAI API ({exc.code}): {body}"
    except Exception as exc:
        return f"⚠️ Error al llamar a OpenAI: {exc}"


def _rag_call_groq(system: str, messages: list[dict]) -> str:
    """Llama a Groq API (compatible OpenAI, urllib stdlib). R-090."""
    if not RAG_GROQ_KEY:
        return "⚠️ GROQ_API_KEY no configurada en config.env."
    import urllib.request, urllib.error

    msgs = [{"role": "system", "content": system}] + messages
    payload = json.dumps({
        "model": RAG_GROQ_MODEL,
        "messages": msgs,
        "max_tokens": RAG_MAX_TOKENS,
        "temperature": 0.25,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {RAG_GROQ_KEY}",
                 "User-Agent": "VigexPanel/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:300]
        return f"⚠️ Error Groq API ({exc.code}): {body}"
    except Exception as exc:
        return f"⚠️ Error al llamar a Groq: {exc}"


def _rag_generate(query: str, historial: list[dict]) -> str:
    """Pipeline completo: retrieval → system prompt → LLM → respuesta. R-090."""
    context = _rag_build_context(query)
    system = _RAG_SYSTEM_PROMPT
    if context:
        system += f"\n\nDocumentación relevante:\n\n{context}"

    # Limitar historial para no exceder la ventana de contexto del modelo
    messages = historial[-12:] + [{"role": "user", "content": query}]

    if RAG_LLM_PROVIDER == "anthropic":
        return _rag_call_anthropic(system, messages)
    if RAG_LLM_PROVIDER == "gemini":
        return _rag_call_gemini(system, messages)
    if RAG_LLM_PROVIDER == "openai":
        return _rag_call_openai(system, messages)
    if RAG_LLM_PROVIDER == "groq":
        return _rag_call_groq(system, messages)
    return _rag_call_ollama(system, messages)


def _rag_check_ollama() -> dict:
    """Comprueba si Ollama está disponible y el modelo configurado está descargado."""
    import urllib.request
    import urllib.error
    try:
        req = urllib.request.Request(f"{RAG_OLLAMA_URL}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            modelos = [m.get("name", "") for m in data.get("models", [])]
            model_ok = any(RAG_OLLAMA_MODEL in m for m in modelos)
            return {"disponible": True, "modelos": modelos, "modelo_ok": model_ok}
    except Exception:
        return {"disponible": False, "modelos": [], "modelo_ok": False}


@app.get("/asistente")
def asistente_page(request: Request):
    """Página del Asistente IA con RAG. R-090"""
    if not is_authenticated(request):
        return RedirectResponse(url="/login", status_code=303)

    context = get_common_context(request)
    context["rag_provider"]      = RAG_LLM_PROVIDER
    _model_map = {
        "ollama":    RAG_OLLAMA_MODEL,
        "anthropic": RAG_ANTHROPIC_MODEL,
        "gemini":    RAG_GEMINI_MODEL,
        "openai":    RAG_OPENAI_MODEL,
        "groq":      RAG_GROQ_MODEL,
    }
    context["rag_model"]         = _model_map.get(RAG_LLM_PROVIDER, RAG_OLLAMA_MODEL)
    context["rag_faq_total"]     = len(_FAQ_ENTRIES)

    # Solo comprobamos el estado de Ollama si el proveedor es local
    if RAG_LLM_PROVIDER == "ollama":
        context["rag_status"] = _rag_check_ollama()
    else:
        context["rag_status"] = {"disponible": True, "modelo_ok": True, "modelos": []}

    return templates.TemplateResponse(request, "asistente.html", context)


@app.post("/api/asistente/chat")
async def asistente_chat_api(request: Request):
    """Endpoint de chat del Asistente IA. R-090 / R-090-sec"""
    # ── Autenticación ────────────────────────────────────────────────────────
    if not is_authenticated(request):
        return JSONResponse({"error": "No autenticado."}, status_code=401)

    # ── Permiso de módulo (R-090-sec) ────────────────────────────────────────
    if not has_permission(request, "asistente"):
        return JSONResponse(
            {"error": "Sin permiso para usar el Asistente IA. Contacta con el administrador."},
            status_code=403,
        )

    # ── Rate limiting por usuario (R-090-sec) ────────────────────────────────
    username = request.session.get("user", "anon")
    if not _rag_check_rate_limit(username):
        return JSONResponse(
            {"error": (
                f"Demasiadas consultas. Máximo {RAG_RATE_LIMIT_REQS} mensajes "
                f"por {RAG_RATE_LIMIT_WINDOW} segundos. Espera un momento."
            )},
            status_code=429,
        )

    data = await request.json()
    mensaje   = (data.get("mensaje") or "").strip()
    historial = data.get("historial", [])

    if not mensaje:
        return JSONResponse({"error": "Mensaje vacío."}, status_code=400)
    if len(mensaje) > 2000:
        return JSONResponse({"error": "Mensaje demasiado largo (máx. 2 000 caracteres)."}, status_code=400)

    # Sanitizar historial
    historial_limpio: list[dict] = [
        {"role": m["role"], "content": str(m["content"])[:3000]}
        for m in historial
        if isinstance(m, dict)
        and m.get("role") in ("user", "assistant")
        and m.get("content")
    ][-20:]

    respuesta = _rag_generate(mensaje, historial_limpio)

    log_event(
        tipo="ASISTENTE_IA",
        resultado="OK",
        usuario=request.session.get("user", "anon"),
        ip_origen=request.client.host if request.client else None,
        recurso="POST /api/asistente/chat",
        detalle=f"RAG query len={len(mensaje)} provider={RAG_LLM_PROVIDER}",
    )

    return JSONResponse({"respuesta": respuesta})


# =============================================================================
# R-068 / Ruta 8.7 — DRO: Orquestación de recuperación ante desastres
# =============================================================================

_DRO_PASOS: list[dict] = [
    {
        "num": 1,
        "titulo": "Verificar estado del servidor",
        "descripcion": (
            "Comprueba que el servidor de la API responde, el disco tiene espacio suficiente "
            "y los servicios críticos están activos."
        ),
        "accion_label": "Ir a Monitoreo",
        "accion_url": "/monitoreo",
        "accion_icon": "fa-chart-area",
        "tipo": "normal",
    },
    {
        "num": 2,
        "titulo": "Verificar integridad de copias",
        "descripcion": (
            "Revisa que existen copias recientes con SHA256 válido antes de iniciar cualquier "
            "restauración. Una copia corrupta puede empeorar la situación."
        ),
        "accion_label": "Ver integridad",
        "accion_url": "/copias/salud",
        "accion_icon": "fa-shield-check",
        "tipo": "normal",
    },
    {
        "num": 3,
        "titulo": "Seleccionar y restaurar la copia",
        "descripcion": (
            "Elige la copia más reciente en buen estado. Usa el botón 'Restaurar' en la "
            "pantalla de Copias para lanzar el proceso vía SSH. El panel pedirá confirmación "
            "antes de ejecutar."
        ),
        "accion_label": "Ir a Copias",
        "accion_url": "/backups",
        "accion_icon": "fa-database",
        "tipo": "critico",
    },
    {
        "num": 4,
        "titulo": "Verificar servicios tras la restauración",
        "descripcion": (
            "Una vez finalizada la restauración, comprueba que todos los servicios configurados "
            "vuelven a estar activos. Reinicia los que estén caídos."
        ),
        "accion_label": "Ver servicios",
        "accion_url": "/servicios",
        "accion_icon": "fa-server",
        "tipo": "normal",
    },
    {
        "num": 5,
        "titulo": "Revisar alertas activas",
        "descripcion": (
            "Comprueba si quedan alertas sin resolver después de la recuperación. "
            "Desactiva las alertas que ya estén corregidas para evitar notificaciones "
            "redundantes."
        ),
        "accion_label": "Ver alertas",
        "accion_url": "/alertas",
        "accion_icon": "fa-bell",
        "tipo": "normal",
    },
    {
        "num": 6,
        "titulo": "Documentar el incidente",
        "descripcion": (
            "Abre un ticket de soporte describiendo qué falló, cuándo ocurrió, qué copia "
            "se restauró y el tiempo de recuperación (RTO real). Esta información es clave "
            "para mejorar el plan ante futuras incidencias."
        ),
        "accion_label": "Abrir ticket",
        "accion_url": "/soporte",
        "accion_icon": "fa-headset",
        "tipo": "normal",
    },
]


@app.get("/recuperacion")
def recuperacion_dro(request: Request):
    """Pantalla DRO: runbook guiado de recuperación ante desastres. R-068"""
    if not is_authenticated(request):
        return RedirectResponse(url="/login", status_code=303)

    # Recopilar estado actual del servidor para el resumen inicial
    estado: dict[str, Any] = {}

    # Disco (usa la función de monitoreo existente si está disponible)
    try:
        import shutil as _shutil
        total, usado, libre = _shutil.disk_usage("/")
        estado["disco_pct"] = round(usado / total * 100)
        estado["disco_libre_gb"] = round(libre / (1024 ** 3), 1)
        estado["disco_ok"] = estado["disco_pct"] < 85
    except Exception:
        estado["disco_pct"] = None
        estado["disco_ok"] = None

    # Última copia
    try:
        historial = cargar_historial_backups(limit=1)
        if historial:
            ultima = historial[0]
            estado["ultima_copia_fecha"] = ultima.get("fecha", "—")
            estado["ultima_copia_ok"] = (ultima.get("estado", "").upper() == "OK")
        else:
            estado["ultima_copia_fecha"] = "Sin registros"
            estado["ultima_copia_ok"] = False
    except Exception:
        estado["ultima_copia_fecha"] = "No disponible"
        estado["ultima_copia_ok"] = None

    # Alertas — total de eventos registrados
    try:
        stats = get_alert_stats()
        estado["alertas_activas"] = stats.get("alerts_total", 0)
    except Exception:
        estado["alertas_activas"] = None

    context = get_common_context(request)
    context["dro_pasos"] = _DRO_PASOS
    context["estado"] = estado
    return templates.TemplateResponse(request, "recuperacion.html", context)


# =====================================================================
# R-080 / Ruta 10.4 — Heartbeat hacia Vigex Central
# =====================================================================

def _collect_heartbeat_data() -> dict:
    """Recopila métricas locales para el heartbeat. Sin excepciones al exterior."""
    data: dict = {
        "cliente_id": CENTRAL_SUPPORT_CLIENT_ID,
        "nombre_cliente": CENTRAL_SUPPORT_CLIENT_NAME,
        "version_panel": os.getenv("VIGEX_VERSION", "1.0-rc1"),
    }
    # Disco
    try:
        import shutil as _shutil
        uso = _shutil.disk_usage("/")
        data["disco_pct"] = int(uso.used * 100 / uso.total) if uso.total else None
    except Exception:
        data["disco_pct"] = None

    # Último backup
    try:
        historial = cargar_historial_backups(limit=1)
        if historial:
            ultimo = historial[0]
            data["backups_ok"] = 1 if str(ultimo.get("estado", "")).upper() == "OK" else 0
            data["ultimo_backup"] = str(ultimo.get("fecha", ""))
        else:
            data["backups_ok"] = None
            data["ultimo_backup"] = ""
    except Exception:
        data["backups_ok"] = None
        data["ultimo_backup"] = ""

    # Alertas
    try:
        stats = get_alert_stats()
        data["alertas_activas"] = int(stats.get("alerts_total", 0))
    except Exception:
        data["alertas_activas"] = None

    # Uptime del proceso (si está disponible)
    try:
        import time as _time
        data["uptime_segundos"] = int(_time.time() - _startup_ts)
    except Exception:
        data["uptime_segundos"] = None

    return data


# Timestamp de arranque del proceso (para calcular uptime)
import time as _time_mod
_startup_ts: float = _time_mod.time()


def _fire_heartbeat() -> None:
    """Envía el heartbeat a Central en segundo plano. Fallo silencioso."""
    if not CENTRAL_HEARTBEAT_URL or not CENTRAL_SUPPORT_ENABLED:
        return
    try:
        import urllib.request as _req
        import json as _json
        data = _collect_heartbeat_data()
        body = _json.dumps(data).encode("utf-8")
        req = _req.Request(
            CENTRAL_HEARTBEAT_URL,
            data=body,
            headers={
                "Content-Type": "application/json",
                "X-Vigex-Client-Token": CENTRAL_SUPPORT_TOKEN,
                "User-Agent": "Vigex-Panel/1.0",
            },
            method="POST",
        )
        with _req.urlopen(req, timeout=CENTRAL_SUPPORT_TIMEOUT) as _r:
            pass  # respuesta ignorada
    except Exception:
        pass  # silencioso — el heartbeat nunca debe interrumpir el panel


def _heartbeat_daemon() -> None:
    """Daemon thread: envía heartbeat cada CENTRAL_HEARTBEAT_INTERVAL segundos."""
    import time as _t
    _t.sleep(30)  # espera inicial para que la app arranque completamente
    while True:
        _fire_heartbeat()
        _t.sleep(max(60, CENTRAL_HEARTBEAT_INTERVAL))


if CENTRAL_SUPPORT_ENABLED and CENTRAL_HEARTBEAT_URL:
    threading.Thread(
        target=_heartbeat_daemon,
        daemon=True,
        name="vigex-heartbeat",
    ).start()


@app.get("/api/v1/heartbeat")
def api_heartbeat(request: Request):
    """
    Endpoint público de salud del panel (sin autenticación para llamadas de monitoring).
    Devuelve métricas básicas del servidor en JSON.
    """
    return _collect_heartbeat_data()


# =====================================================================
# R-086 / Ruta 12.2 — API de producto: endpoint de información de versión
# =====================================================================

_VIGEX_API_VERSION = "1.0"
_VIGEX_BUILD_DATE = "2026-06-08"

@app.get("/api/v1/info")
def api_info():
    """
    Información pública de la instalación Vigex.
    Utilizable por integraciones externas para verificar compatibilidad.
    No requiere autenticación.
    """
    return {
        "producto": "Vigex",
        "api_version": _VIGEX_API_VERSION,
        "panel_version": os.getenv("VIGEX_VERSION", "1.0-rc1"),
        "build_date": _VIGEX_BUILD_DATE,
        "endpoints_publicos": [
            "GET /health",
            "GET /api/v1/info",
            "GET /api/v1/heartbeat",
        ],
        "endpoints_autenticados": [
            "GET /api/soporte/faq?q=",
            "POST /api/soporte/tickets",
            "GET /api/soporte/estado/{ticket_id}",
        ],
        "documentacion": "/api/docs",
    }
