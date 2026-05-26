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
import posixpath
from pathlib import Path
from datetime import datetime
from typing import Any

from passlib.context import CryptContext
import pymysql
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse, Response
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

# =====================
# CONFIG LOGIN / SESIÓN
# =====================
SECRET_KEY = os.getenv("SECRET_KEY", "cambia-esta-clave-por-una-segura")
ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# =====================
# CONFIG MULTI-SERVIDOR
# =====================
USUARIO = os.getenv("SSH_USER", "dasc")
SERVIDOR_BACKUPS = os.getenv("BACKUPS_HOST", "192.168.60.30")
SERVIDOR_SERVICIOS = os.getenv("SERVICIOS_HOST", "192.168.60.30")
CACTI_URL = os.getenv("CACTI_URL", "http://127.0.0.1/cacti/")

LOGS_DB_HOST = os.getenv("LOGS_DB_HOST", "192.168.60.20")
LOGS_DB_NAME = os.getenv("LOGS_DB_NAME", "dasc_logs")
LOGS_DB_USER = os.getenv("LOGS_DB_USER", "dasc_logs")
LOGS_DB_PASS = os.getenv("LOGS_DB_PASS", "dascpass")
LOGS_ORIGIN = os.getenv("LOGS_ORIGIN", "dasc-web")

TERMINAL_MAIN_HOST = os.getenv("TERMINAL_MAIN_HOST", "127.0.0.1")
TERMINAL_DATABASE_HOST = os.getenv("TERMINAL_DATABASE_HOST", LOGS_DB_HOST)
TERMINAL_TIMEOUT = int(os.getenv("TERMINAL_TIMEOUT", "30"))
TERMINAL_MAX_COMMAND_LENGTH = int(os.getenv("TERMINAL_MAX_COMMAND_LENGTH", "4000"))

SCRIPT_SERVICIOS = os.getenv("SCRIPT_SERVICIOS", "/usr/local/bin/servicios_api.sh")
SCRIPT_BACKUPS = os.getenv("SCRIPT_BACKUPS", "/usr/local/bin/backups_api.sh")
SCRIPT_RESTORE = os.getenv("SCRIPT_RESTORE", "/usr/local/bin/restore_api.sh")
BACKUP_AUTOMATION_MARKER = "# DASC_BACKUP_AUTO"
BACKUP_AUTOMATION_LOG = os.getenv("BACKUP_AUTOMATION_LOG", "/home/dasc/backups/.dasc/cron.log")


# =====================
# CONFIG SSH ENDURECIDO
# =====================
SSH_KEY_PATH = os.getenv("DASC_SSH_KEY", "/opt/dasc/api/.ssh/id_rsa_dasc")
SSH_KNOWN_HOSTS_PATH = os.getenv("DASC_SSH_KNOWN_HOSTS", "/opt/dasc/api/.ssh/known_hosts_dasc")
SSH_TIMEOUT = int(os.getenv("DASC_SSH_TIMEOUT", "30"))
SSH_CONNECT_TIMEOUT = int(os.getenv("DASC_SSH_CONNECT_TIMEOUT", "10"))
SSH_STDIN_MAX_LENGTH = int(os.getenv("DASC_SSH_STDIN_MAX_LENGTH", "20000"))

_default_ssh_hosts = f"{SERVIDOR_BACKUPS},{SERVIDOR_SERVICIOS}"
SSH_ALLOWED_HOSTS = {
    item.strip()
    for item in os.getenv("DASC_SSH_ALLOWED_HOSTS", _default_ssh_hosts).split(",")
    if item.strip()
}


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
    }

    if script not in allowed_scripts:
        raise ValueError(f"Script SSH no permitido: {script}")

    if any(len(str(arg)) > 1000 for arg in args):
        raise ValueError("Argumento SSH demasiado largo")

    if script == "cat" and args != ["/home/dasc/backups/.dasc/history.tsv"]:
        raise ValueError("Uso de cat no permitido")

    if script == "crontab" and args != ["-l"]:
        raise ValueError("Uso de crontab no permitido")

    if script == "/bin/bash" and args != ["-lc", "hostname && date"]:
        raise ValueError("Uso de /bin/bash no permitido en ssh_run")


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


@app.on_event("startup")
def startup_event() -> None:
    ensure_users_file()
    init_alerts_db()
    ensure_default_recipient()



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
        cmd = build_ssh_base_command(host) + [script] + args

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
        ["/home/dasc/backups/.dasc/history.tsv"],
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
cat >> "$TMP" <<'DASC_CRON_BLOCK'
{block.rstrip()}
DASC_CRON_BLOCK
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
        [str(backup_id), "/home/dasc/backups", "SI"],
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
    allowed_root = "/home/dasc/backups"

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

HIST="/home/dasc/backups/.dasc/history.tsv"
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
    /home/dasc/backups/*)
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


app.add_middleware(AuthAndLogMiddleware)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    auth_user = get_auth_user(username, password)
    if auth_user:
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
            "description": "Servidor donde se ejecuta el panel DASC y la API principal.",
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
        "<b>DASC</b>\n"
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
    dest: str = Form("/home/dasc/backups"),
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
    dest = (dest or "/home/dasc/backups").strip()

    if not db:
        return RedirectResponse(
            url="/backups?ok=0&msg=La+base+de+datos+es+obligatoria",
            status_code=303,
        )

    if not dest.startswith("/home/dasc/backups"):
        return RedirectResponse(
            url="/backups?ok=0&msg=La+ruta+destino+debe+estar+dentro+de+/home/dasc/backups",
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
        "X-DASC-Backup-ID": str(backup_id),
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
    dest: str = Form("/home/dasc/backups"),
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
CENTRAL_SUPPORT_TOKEN = os.getenv("CENTRAL_SUPPORT_TOKEN", "dasc-central-demo-token-lab").strip()
CENTRAL_SUPPORT_TIMEOUT = int(os.getenv("CENTRAL_SUPPORT_TIMEOUT", "5"))


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
                    str(ticket.get("canal", "Panel DASC")),
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
                "panel",
            ),
        )
        conn.commit()


def next_support_ticket_id():
    ensure_support_db()

    year = _support_datetime.now().year
    prefix = f"DASC-{year}-"
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
        "version_panel": os.getenv("DASC_VERSION", "lab-local"),
        "origen": "panel-local",
    }

    data = _support_json.dumps(payload, ensure_ascii=False).encode("utf-8")

    req = _support_urlrequest.Request(
        CENTRAL_SUPPORT_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "X-DASC-Client-Token": CENTRAL_SUPPORT_TOKEN,
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



@app.get("/soporte")
def soporte_page(request: Request):
    if not is_admin(request):
        return permission_redirect("Acceso reservado al equipo técnico DASC.")

    context = get_common_context(request)
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
        return permission_redirect("Acceso reservado al equipo técnico DASC.")

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
        "canal": "Panel DASC",
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


def search_support_tickets(estado="", prioridad="", tipo="", q="", limit=100):
    ensure_support_db()

    where = []
    params = []

    estado = (estado or "").strip()
    prioridad = (prioridad or "").strip()
    tipo = (tipo or "").strip()
    q = (q or "").strip()

    if estado:
        where.append("estado = ?")
        params.append(estado)

    if prioridad:
        where.append("prioridad = ?")
        params.append(prioridad)

    if tipo:
        where.append("tipo = ?")
        params.append(tipo)

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


def support_ticket_counts():
    ensure_support_db()

    counts = {
        "total": 0,
        "por_estado": {},
        "por_prioridad": {},
    }

    with support_db_connect() as conn:
        total_row = conn.execute("SELECT COUNT(*) AS total FROM support_tickets").fetchone()
        counts["total"] = total_row["total"] if total_row else 0

        for row in conn.execute(
            "SELECT estado, COUNT(*) AS total FROM support_tickets GROUP BY estado ORDER BY estado"
        ):
            counts["por_estado"][row["estado"]] = row["total"]

        for row in conn.execute(
            "SELECT prioridad, COUNT(*) AS total FROM support_tickets GROUP BY prioridad ORDER BY prioridad"
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
                AND COALESCE(central_sync_status, '') IN ('error', '')
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
        return permission_redirect("Acceso reservado al equipo técnico DASC.")

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

@app.get("/soporte/tickets")
def soporte_tickets_page(
    request: Request,
    estado: str = "",
    prioridad: str = "",
    tipo: str = "",
    q: str = "",
):
    if not is_admin(request):
        return permission_redirect("Acceso reservado al equipo técnico DASC.")

    context = get_common_context(request)

    tickets = search_support_tickets(
        estado=estado,
        prioridad=prioridad,
        tipo=tipo,
        q=q,
        limit=100,
    )

    context["tickets"] = tickets
    context["counts"] = support_ticket_counts()
    context["support_statuses"] = SUPPORT_STATUSES
    context["support_priorities"] = SUPPORT_PRIORITIES
    context["support_types"] = SUPPORT_TYPES
    context["filters"] = {
        "estado": estado,
        "prioridad": prioridad,
        "tipo": tipo,
        "q": q,
    }

    return templates.TemplateResponse(request, "soporte_tickets.html", context)


@app.get("/soporte/tickets/{ticket_id}")
def soporte_ticket_detail_page(request: Request, ticket_id: str):
    if not is_admin(request):
        return permission_redirect("Acceso reservado al equipo técnico DASC.")

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
):
    if not is_admin(request):
        return permission_redirect("Acceso reservado al equipo técnico DASC.")

    usuario = request.session.get("user", "anon")

    ok, msg = update_support_ticket_status_priority(
        ticket_id=ticket_id,
        nuevo_estado=estado,
        nueva_prioridad=prioridad,
        usuario=usuario,
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
Equipo DASC""",
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
Equipo DASC""",
    },
    {
        "key": "analisis",
        "titulo": "Incidencia en análisis",
        "uso": "Informar de que el equipo DASC está revisando el caso.",
        "texto": """Hola {contacto},

Estamos revisando la solicitud {ticket_id}.

El caso queda en análisis técnico. Estamos comprobando el estado del servicio afectado y revisando las evidencias disponibles.

Servicio afectado: {servicio}
Estado actual del ticket: {estado}

Te informaremos con el resultado o con el siguiente paso necesario.

Un saludo,
Equipo DASC""",
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
Equipo DASC""",
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
Equipo DASC""",
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
Equipo DASC""",
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
Equipo DASC""",
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

    return f"""# Resumen técnico de ticket DASC

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

Revisar el caso, confirmar diagnóstico y actualizar el estado del ticket en DASC.

## Nota

Este resumen se ha generado desde DASC Server Manager para copiarlo en Jira, Zammad u otra herramienta interna de soporte.
"""
