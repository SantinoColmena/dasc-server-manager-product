import os
import hmac
import hashlib
import secrets
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "central_support.db"

APP_NAME = "Vigex Central"
DEMO_CLIENT_ID = os.getenv("Vigex_CENTRAL_DEMO_CLIENT_ID", "cliente-demo-a")
DEMO_CLIENT_NAME = os.getenv("Vigex_CENTRAL_DEMO_CLIENT_NAME", "Cliente Demo A")
DEMO_CLIENT_TOKEN = os.getenv("Vigex_CENTRAL_DEMO_TOKEN", "vigex-central-demo-token-lab")

# =====================
# R-049Q - CONFIG AUTENTICACION CENTRAL
# =====================

CENTRAL_AUTH_ENABLED = os.getenv("Vigex_CENTRAL_AUTH_ENABLED", "true").strip().lower() in ("1", "true", "yes", "on")
CENTRAL_LAB_MODE = os.getenv("Vigex_CENTRAL_LAB_MODE", "false").strip().lower() in ("1", "true", "yes", "on")

DEFAULT_LAB_ADMIN_USER = "admin"
DEFAULT_LAB_ADMIN_PASSWORD = "admin"
DEFAULT_LAB_TECH_USER = "tecnico"
DEFAULT_LAB_TECH_PASSWORD = "tecnico"

CENTRAL_SECRET_KEY = os.getenv("Vigex_CENTRAL_SECRET_KEY", "").strip()
if not CENTRAL_SECRET_KEY:
    CENTRAL_SECRET_KEY = (
        "vigex-central-secret-lab-change-me"
        if CENTRAL_LAB_MODE
        else secrets.token_urlsafe(48)
    )

CENTRAL_ADMIN_USER = os.getenv(
    "Vigex_CENTRAL_ADMIN_USER",
    DEFAULT_LAB_ADMIN_USER if CENTRAL_LAB_MODE else "",
)
CENTRAL_ADMIN_PASSWORD = os.getenv(
    "Vigex_CENTRAL_ADMIN_PASSWORD",
    DEFAULT_LAB_ADMIN_PASSWORD if CENTRAL_LAB_MODE else "",
)
CENTRAL_TECH_USER = os.getenv(
    "Vigex_CENTRAL_TECH_USER",
    DEFAULT_LAB_TECH_USER if CENTRAL_LAB_MODE else "",
)
CENTRAL_TECH_PASSWORD = os.getenv(
    "Vigex_CENTRAL_TECH_PASSWORD",
    DEFAULT_LAB_TECH_PASSWORD if CENTRAL_LAB_MODE else "",
)

# M-4: soporte opcional de contraseñas hasheadas (PBKDF2-SHA256, sin
# dependencias externas). Si se define el hash, tiene prioridad sobre la
# contraseña en texto plano. Retrocompatible: si no se define, el
# comportamiento es idéntico al anterior.
CENTRAL_ADMIN_PASSWORD_HASH = os.getenv("Vigex_CENTRAL_ADMIN_PASSWORD_HASH", "").strip()
CENTRAL_TECH_PASSWORD_HASH = os.getenv("Vigex_CENTRAL_TECH_PASSWORD_HASH", "").strip()


def verify_pbkdf2(plain, stored):
    """Verifica una contraseña contra un hash PBKDF2-SHA256.

    Formato: pbkdf2_sha256$<iteraciones>$<salt_hex>$<hash_hex>
    Generar uno:
      python -c "import hashlib,os; s=os.urandom(16); dk=hashlib.pbkdf2_hmac('sha256', b'TU_PASS', s, 200000); print('pbkdf2_sha256$200000$'+s.hex()+'$'+dk.hex())"
    """
    try:
        algo, iter_s, salt_hex, dk_hex = (stored or "").split("$")
        if algo != "pbkdf2_sha256":
            return False
        dk = hashlib.pbkdf2_hmac(
            "sha256",
            (plain or "").encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iter_s),
        )
        return hmac.compare_digest(dk, bytes.fromhex(dk_hex))
    except Exception:
        return False


def is_default_lab_credential(username, password):
    return (
        (username == DEFAULT_LAB_ADMIN_USER and password == DEFAULT_LAB_ADMIN_PASSWORD)
        or (username == DEFAULT_LAB_TECH_USER and password == DEFAULT_LAB_TECH_PASSWORD)
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    # L-5: inicialización al arranque (sustituye a @app.on_event("startup")).
    init_db()
    yield


app = FastAPI(title=APP_NAME, lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=CENTRAL_SECRET_KEY)
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


class CentralTicketIn(BaseModel):
    cliente_id: str = Field(..., min_length=1)
    nombre_cliente: str = Field(..., min_length=1)
    ticket_local_id: Optional[str] = ""
    tipo: str = Field(..., min_length=1)
    prioridad: str = Field(..., min_length=1)
    servicio: str = Field(..., min_length=1)
    descripcion: str = Field(..., min_length=1)
    evidencia: Optional[str] = ""
    contacto: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    fecha_origen: Optional[str] = ""
    version_panel: Optional[str] = ""
    origen: Optional[str] = "panel-local"


def now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def db_connect():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with db_connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS central_clients (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                token TEXT NOT NULL,
                activo INTEGER NOT NULL DEFAULT 1,
                fecha_alta TEXT NOT NULL
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS central_tickets (
                id TEXT PRIMARY KEY,
                fecha_recepcion TEXT NOT NULL,
                fecha_actualizacion TEXT NOT NULL,
                cliente_id TEXT NOT NULL,
                nombre_cliente TEXT NOT NULL,
                ticket_local_id TEXT,
                tipo TEXT NOT NULL,
                prioridad TEXT NOT NULL,
                servicio TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                evidencia TEXT,
                contacto TEXT NOT NULL,
                email TEXT NOT NULL,
                fecha_origen TEXT,
                version_panel TEXT,
                origen TEXT,
                estado TEXT NOT NULL DEFAULT 'Nuevo'
            )
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_central_tickets_cliente
            ON central_tickets (cliente_id)
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_central_tickets_estado
            ON central_tickets (estado)
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_central_tickets_prioridad
            ON central_tickets (prioridad)
            """
        )

        conn.execute(
            """
            INSERT OR IGNORE INTO central_clients (
                id,
                nombre,
                token,
                activo,
                fecha_alta
            )
            VALUES (?, ?, ?, 1, ?)
            """,
            (
                DEMO_CLIENT_ID,
                DEMO_CLIENT_NAME,
                DEMO_CLIENT_TOKEN,
                now_text(),
            ),
        )

        conn.commit()


def validate_client_token(cliente_id, token):
    init_db()

    if not token:
        return False

    with db_connect() as conn:
        row = conn.execute(
            """
            SELECT id, token, activo
            FROM central_clients
            WHERE id = ?
            """,
            (cliente_id,),
        ).fetchone()

    if not row:
        return False

    if int(row["activo"]) != 1:
        return False

    # M-5: comparación en tiempo constante para evitar ataques de temporización.
    return hmac.compare_digest(str(row["token"]), str(token))


def next_central_ticket_id():
    init_db()

    year = datetime.now().year
    prefix = f"CENTRAL-{year}-"
    max_num = 0

    with db_connect() as conn:
        rows = conn.execute(
            "SELECT id FROM central_tickets WHERE id LIKE ?",
            (f"{prefix}%",),
        ).fetchall()

    for row in rows:
        ticket_id = str(row["id"])
        try:
            num = int(ticket_id.replace(prefix, ""))
            max_num = max(max_num, num)
        except Exception:
            pass

    return f"{prefix}{max_num + 1:04d}"


def create_central_ticket(payload: CentralTicketIn):
    init_db()

    ticket_id = next_central_ticket_id()
    now = now_text()

    with db_connect() as conn:
        conn.execute(
            """
            INSERT INTO central_tickets (
                id,
                fecha_recepcion,
                fecha_actualizacion,
                cliente_id,
                nombre_cliente,
                ticket_local_id,
                tipo,
                prioridad,
                servicio,
                descripcion,
                evidencia,
                contacto,
                email,
                fecha_origen,
                version_panel,
                origen,
                estado
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ticket_id,
                now,
                now,
                payload.cliente_id,
                payload.nombre_cliente,
                payload.ticket_local_id or "",
                payload.tipo,
                payload.prioridad,
                payload.servicio,
                payload.descripcion,
                payload.evidencia or "",
                payload.contacto,
                payload.email,
                payload.fecha_origen or "",
                payload.version_panel or "",
                payload.origen or "panel-local",
                "Nuevo",
            ),
        )
        conn.commit()

    return ticket_id


def list_tickets(limit=100):
    init_db()

    with db_connect() as conn:
        rows = conn.execute(
            """
            SELECT
                id,
                fecha_recepcion,
                fecha_actualizacion,
                cliente_id,
                nombre_cliente,
                ticket_local_id,
                tipo,
                prioridad,
                servicio,
                descripcion,
                evidencia,
                contacto,
                email,
                fecha_origen,
                version_panel,
                origen,
                estado
            FROM central_tickets
            ORDER BY fecha_recepcion DESC, id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]


# L-5: inicialización movida a la función `lifespan` (ver arriba).


@app.get("/health")
def health():
    init_db()
    return {
        "status": "ok",
        "app": APP_NAME,
        "db": str(DB_PATH),
        "demo_client_id": DEMO_CLIENT_ID,
    }


@app.post("/api/v1/support/tickets")
def receive_support_ticket(
    payload: CentralTicketIn,
    x_vigex_client_token: Optional[str] = Header(default=None),
):
    if not validate_client_token(payload.cliente_id, x_vigex_client_token):
        raise HTTPException(status_code=401, detail="Token de cliente no válido")

    ticket_id = create_central_ticket(payload)

    return {
        "ok": True,
        "central_ticket_id": ticket_id,
        "estado": "Nuevo",
        "mensaje": "Ticket recibido en API central Vigex",
    }



# =====================
# R-049P - API CONSULTA TICKET CENTRAL
# =====================

@app.get("/api/v1/support/tickets/{ticket_id}")
def api_get_support_ticket_status(
    ticket_id: str,
    x_vigex_client_token: Optional[str] = Header(default=None),
    x_vigex_client_id: Optional[str] = Header(default=None),
):
    ticket = get_central_ticket(ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket central no encontrado")

    client_id = (x_vigex_client_id or "").strip()

    if not client_id:
        raise HTTPException(status_code=400, detail="Falta cabecera X-Vigex-Client-ID")

    if client_id != ticket.get("cliente_id"):
        raise HTTPException(status_code=403, detail="El ticket no pertenece al cliente indicado")

    if not validate_client_token(client_id, x_vigex_client_token):
        raise HTTPException(status_code=401, detail="Token de cliente no válido")

    return {
        "ok": True,
        "ticket": {
            "id": ticket.get("id", ""),
            "cliente_id": ticket.get("cliente_id", ""),
            "nombre_cliente": ticket.get("nombre_cliente", ""),
            "ticket_local_id": ticket.get("ticket_local_id", ""),
            "tipo": ticket.get("tipo", ""),
            "prioridad": ticket.get("prioridad", ""),
            "servicio": ticket.get("servicio", ""),
            "estado": ticket.get("estado", ""),
            "fecha_recepcion": ticket.get("fecha_recepcion", ""),
            "fecha_actualizacion": ticket.get("fecha_actualizacion", ""),
        },
    }


# =====================
# R-049Q - LOGIN Y ROLES PANEL CENTRAL
# =====================

def get_central_users():
    users = {}

    def add_user(username, password, password_hash, role, label):
        username = (username or "").strip()
        password = password or ""
        password_hash = (password_hash or "").strip()

        if not username or (not password and not password_hash):
            return

        # No activar credenciales de laboratorio por defecto fuera de modo lab.
        if not CENTRAL_LAB_MODE and not password_hash and is_default_lab_credential(username, password):
            return

        users[username] = {
            "password": password,
            "password_hash": password_hash,
            "role": role,
            "label": label,
        }

    add_user(
        CENTRAL_ADMIN_USER,
        CENTRAL_ADMIN_PASSWORD,
        CENTRAL_ADMIN_PASSWORD_HASH,
        "admin",
        "Administrador central",
    )

    add_user(
        CENTRAL_TECH_USER,
        CENTRAL_TECH_PASSWORD,
        CENTRAL_TECH_PASSWORD_HASH,
        "tecnico",
        "Tecnico Vigex",
    )

    return users


def validate_central_login(username, password):
    username = (username or "").strip()
    password = password or ""

    users = get_central_users()
    user = users.get(username)

    if not user:
        return None

    stored_hash = user.get("password_hash", "")
    stored_plain = user.get("password", "")

    if stored_hash:
        ok = verify_pbkdf2(password, stored_hash)
    elif stored_plain:
        ok = hmac.compare_digest(password, stored_plain)
    else:
        ok = False

    if not ok:
        return None

    return {
        "username": username,
        "role": user.get("role", "tecnico"),
        "label": user.get("label", username),
    }


def is_central_authenticated(request):
    if not CENTRAL_AUTH_ENABLED:
        return True

    return bool(request.session.get("central_user"))


def get_central_session_context(request):
    return {
        "current_user": request.session.get("central_user", ""),
        "current_role": request.session.get("central_role", ""),
        "current_label": request.session.get("central_label", ""),
        "auth_enabled": CENTRAL_AUTH_ENABLED,
    }


def central_login_redirect():
    return RedirectResponse(url="/login?msg=Sesion+requerida", status_code=303)


@app.get("/login", response_class=HTMLResponse)
def central_login_page(request: Request):
    if is_central_authenticated(request) and CENTRAL_AUTH_ENABLED:
        return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse(
        request,
        "central_login.html",
        {
            "msg": request.query_params.get("msg"),
            "auth_enabled": CENTRAL_AUTH_ENABLED,
            "central_lab_mode": CENTRAL_LAB_MODE,
            "configured_users_count": len(get_central_users()),
        },
    )


@app.post("/login")
def central_login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    user = validate_central_login(username, password)

    if not user:
        return RedirectResponse(
            url="/login?msg=Credenciales+no+validas",
            status_code=303,
        )

    request.session["central_user"] = user["username"]
    request.session["central_role"] = user["role"]
    request.session["central_label"] = user["label"]

    return RedirectResponse(url="/", status_code=303)


@app.get("/logout")
def central_logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login?msg=Sesion+cerrada", status_code=303)

@app.get("/", response_class=HTMLResponse)
def dashboard(
    request: Request,
    estado: str = "",
    prioridad: str = "",
    q: str = "",
):
    if not is_central_authenticated(request):
        return central_login_redirect()

    tickets_all = list_tickets(limit=500)

    estado = (estado or "").strip()
    prioridad = (prioridad or "").strip()
    q = (q or "").strip().lower()

    def ticket_matches(ticket):
        if estado and ticket.get("estado") != estado:
            return False

        if prioridad and ticket.get("prioridad") != prioridad:
            return False

        if q:
            searchable = " ".join(
                str(ticket.get(key, ""))
                for key in (
                    "id",
                    "cliente_id",
                    "nombre_cliente",
                    "ticket_local_id",
                    "tipo",
                    "prioridad",
                    "estado",
                    "servicio",
                    "contacto",
                    "email",
                )
            ).lower()

            if q not in searchable:
                return False

        return True

    tickets = [ticket for ticket in tickets_all if ticket_matches(ticket)]

    total = len(tickets_all)
    nuevos = sum(1 for ticket in tickets_all if ticket.get("estado") == "Nuevo")
    en_gestion = sum(
        1
        for ticket in tickets_all
        if ticket.get("estado") in ("En análisis", "En curso", "Pendiente cliente")
    )
    cerrados = sum(
        1
        for ticket in tickets_all
        if ticket.get("estado") in ("Resuelto", "Cerrado")
    )
    criticos = sum(1 for ticket in tickets_all if ticket.get("prioridad") == "Crítica")

    return templates.TemplateResponse(
        request,
        "central_dashboard.html",
        {
            "tickets": tickets,
            "total": total,
            "total_filtrado": len(tickets),
            "nuevos": nuevos,
            "en_gestion": en_gestion,
            "cerrados": cerrados,
            "criticos": criticos,
            "demo_client_id": DEMO_CLIENT_ID,
            "estados": CENTRAL_TICKET_STATES,
            "prioridades": CENTRAL_TICKET_PRIORITIES,
            "filters": {
                "estado": estado,
                "prioridad": prioridad,
                "q": q,
            },
            **get_central_session_context(request),
        },
    )

# =====================
# R-049J - DETALLE TICKET CENTRAL
# =====================

def get_central_ticket(ticket_id):
    init_db()

    with db_connect() as conn:
        row = conn.execute(
            """
            SELECT
                id,
                fecha_recepcion,
                fecha_actualizacion,
                cliente_id,
                nombre_cliente,
                ticket_local_id,
                tipo,
                prioridad,
                servicio,
                descripcion,
                evidencia,
                contacto,
                email,
                fecha_origen,
                version_panel,
                origen,
                estado
            FROM central_tickets
            WHERE id = ?
            """,
            (ticket_id,),
        ).fetchone()

    if not row:
        return None

    return dict(row)

@app.get("/tickets/{ticket_id}", response_class=HTMLResponse)
def central_ticket_detail(request: Request, ticket_id: str):
    if not is_central_authenticated(request):
        return central_login_redirect()

    ticket = get_central_ticket(ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket central no encontrado")

    history = get_central_ticket_history(ticket_id)

    return templates.TemplateResponse(
        request,
        "central_ticket_detail.html",
        {
            "ticket": ticket,
            "history": history,
            "msg": request.query_params.get("msg"),
            "estados": CENTRAL_TICKET_STATES,
            "prioridades": CENTRAL_TICKET_PRIORITIES,
            **get_central_session_context(request),
        },
    )

# =====================
# R-049K - ESTADO PRIORIDAD CENTRAL
# =====================

CENTRAL_TICKET_STATES = [
    "Nuevo",
    "En análisis",
    "Pendiente cliente",
    "En curso",
    "Resuelto",
    "Cerrado",
]

CENTRAL_TICKET_PRIORITIES = [
    "Baja",
    "Media",
    "Alta",
    "Crítica",
]


def ensure_central_history_table():
    init_db()

    with db_connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS central_ticket_history (
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
            CREATE INDEX IF NOT EXISTS idx_central_history_ticket
            ON central_ticket_history (ticket_id)
            """
        )

        conn.commit()


def get_central_ticket_history(ticket_id, limit=50):
    ensure_central_history_table()

    with db_connect() as conn:
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
            FROM central_ticket_history
            WHERE ticket_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (ticket_id, limit),
        ).fetchall()

    return [dict(row) for row in rows]


def add_central_ticket_history(
    ticket_id,
    usuario,
    accion,
    valor_anterior,
    valor_nuevo,
    detalle,
):
    ensure_central_history_table()

    with db_connect() as conn:
        conn.execute(
            """
            INSERT INTO central_ticket_history (
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
                now_text(),
                usuario,
                accion,
                valor_anterior,
                valor_nuevo,
                detalle,
            ),
        )
        conn.commit()


def update_central_ticket_status_priority(ticket_id, estado, prioridad, usuario):
    ticket = get_central_ticket(ticket_id)

    if not ticket:
        return False, "Ticket central no encontrado"

    estado = (estado or "").strip()
    prioridad = (prioridad or "").strip()

    if estado not in CENTRAL_TICKET_STATES:
        return False, "Estado no válido"

    if prioridad not in CENTRAL_TICKET_PRIORITIES:
        return False, "Prioridad no válida"

    old_estado = ticket.get("estado", "")
    old_prioridad = ticket.get("prioridad", "")

    changes = []

    if old_estado != estado:
        changes.append(("Cambio de estado", old_estado, estado))

    if old_prioridad != prioridad:
        changes.append(("Cambio de prioridad", old_prioridad, prioridad))

    if not changes:
        return True, "Sin cambios"

    with db_connect() as conn:
        conn.execute(
            """
            UPDATE central_tickets
            SET estado = ?, prioridad = ?, fecha_actualizacion = ?
            WHERE id = ?
            """,
            (
                estado,
                prioridad,
                now_text(),
                ticket_id,
            ),
        )
        conn.commit()

    for accion, valor_anterior, valor_nuevo in changes:
        add_central_ticket_history(
            ticket_id=ticket_id,
            usuario=usuario,
            accion=accion,
            valor_anterior=valor_anterior,
            valor_nuevo=valor_nuevo,
            detalle="Actualización realizada desde panel central Vigex",
        )

    return True, "Ticket actualizado"


@app.post("/tickets/{ticket_id}/estado")
def central_ticket_update_status_priority(
    request: Request,
    ticket_id: str,
    estado: str = Form(...),
    prioridad: str = Form(...),
):
    if not is_central_authenticated(request):
        return central_login_redirect()

    usuario = request.session.get("central_user", "vigex_tecnico_lab")

    ok, msg = update_central_ticket_status_priority(
        ticket_id=ticket_id,
        estado=estado,
        prioridad=prioridad,
        usuario=usuario,
    )

    if not ok:
        return RedirectResponse(
            url=f"/tickets/{ticket_id}?msg=Error:+{msg.replace(' ', '+')}",
            status_code=303,
        )

    return RedirectResponse(
        url=f"/tickets/{ticket_id}?msg={msg.replace(' ', '+')}",
        status_code=303,
    )


# =====================
# R-079 / Ruta 10.3 — Gestión de clientes (solo admin)
# =====================

def is_central_admin(request) -> bool:
    return request.session.get("central_role") == "admin"


def require_admin(request):
    """Devuelve None si ok, o una respuesta de redirección/error si no autorizado."""
    if not is_central_authenticated(request):
        return central_login_redirect()
    if not is_central_admin(request):
        raise HTTPException(status_code=403, detail="Se requiere rol de administrador")
    return None


def list_clients() -> list:
    init_db()
    with db_connect() as conn:
        rows = conn.execute(
            """
            SELECT id, nombre, token, activo, fecha_alta
            FROM central_clients
            ORDER BY fecha_alta DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def add_client(client_id: str, nombre: str) -> dict:
    """Alta de cliente con token seguro (256 bits). Devuelve el dict con el token."""
    token = secrets.token_hex(32)
    now = now_text()
    with db_connect() as conn:
        conn.execute(
            """
            INSERT INTO central_clients (id, nombre, token, activo, fecha_alta)
            VALUES (?, ?, ?, 1, ?)
            """,
            (client_id, nombre, token, now),
        )
        conn.commit()
    return {"id": client_id, "nombre": nombre, "token": token, "activo": 1, "fecha_alta": now}


def set_client_active(client_id: str, activo: int):
    with db_connect() as conn:
        conn.execute(
            "UPDATE central_clients SET activo = ? WHERE id = ?",
            (activo, client_id),
        )
        conn.commit()


def rotate_client_token(client_id: str) -> str:
    token = secrets.token_hex(32)
    with db_connect() as conn:
        conn.execute(
            "UPDATE central_clients SET token = ? WHERE id = ?",
            (token, client_id),
        )
        conn.commit()
    return token


@app.get("/clientes", response_class=HTMLResponse)
def central_clientes(request: Request):
    guard = require_admin(request)
    if guard is not None:
        return guard
    clientes = list_clients()
    return templates.TemplateResponse(
        request,
        "central_clientes.html",
        {
            "clientes": clientes,
            "msg": request.query_params.get("msg"),
            "nuevo_token": request.query_params.get("nuevo_token"),
            "nuevo_cliente_id": request.query_params.get("nuevo_cliente_id"),
            **get_central_session_context(request),
        },
    )


@app.post("/clientes/nuevo")
def central_cliente_nuevo(
    request: Request,
    cliente_id: str = Form(...),
    nombre: str = Form(...),
):
    guard = require_admin(request)
    if guard is not None:
        return guard
    cliente_id = cliente_id.strip().lower().replace(" ", "-")
    nombre = nombre.strip()
    if not cliente_id or not nombre:
        return RedirectResponse(url="/clientes?msg=ID+y+nombre+son+obligatorios", status_code=303)
    existing = list_clients()
    if any(c["id"] == cliente_id for c in existing):
        return RedirectResponse(
            url=f"/clientes?msg=Ya+existe+un+cliente+con+ID+{cliente_id}",
            status_code=303,
        )
    cliente = add_client(cliente_id, nombre)
    add_audit_log(
        usuario=request.session.get("central_user", "admin"),
        accion="cliente_nuevo",
        detalle=f"Nuevo cliente: {nombre} (ID: {cliente_id})",
    )
    return RedirectResponse(
        url=(
            f"/clientes?nuevo_token={cliente['token']}"
            f"&nuevo_cliente_id={cliente_id}"
            f"&msg=Cliente+creado+correctamente"
        ),
        status_code=303,
    )


@app.post("/clientes/{cliente_id}/revocar")
def central_cliente_revocar(request: Request, cliente_id: str):
    guard = require_admin(request)
    if guard is not None:
        return guard
    if cliente_id == DEMO_CLIENT_ID:
        return RedirectResponse(
            url="/clientes?msg=No+se+puede+revocar+el+cliente+demo",
            status_code=303,
        )
    clientes = list_clients()
    cliente = next((c for c in clientes if c["id"] == cliente_id), None)
    if not cliente:
        return RedirectResponse(url="/clientes?msg=Cliente+no+encontrado", status_code=303)
    nuevo_activo = 0 if int(cliente["activo"]) == 1 else 1
    set_client_active(cliente_id, nuevo_activo)
    accion_txt = "desactivado" if nuevo_activo == 0 else "reactivado"
    add_audit_log(
        usuario=request.session.get("central_user", "admin"),
        accion=f"cliente_{accion_txt}",
        detalle=f"Cliente {cliente_id} {accion_txt}",
    )
    return RedirectResponse(url=f"/clientes?msg=Cliente+{accion_txt}", status_code=303)


@app.post("/clientes/{cliente_id}/rotar")
def central_cliente_rotar(request: Request, cliente_id: str):
    guard = require_admin(request)
    if guard is not None:
        return guard
    clientes = list_clients()
    if not any(c["id"] == cliente_id for c in clientes):
        return RedirectResponse(url="/clientes?msg=Cliente+no+encontrado", status_code=303)
    nuevo_token = rotate_client_token(cliente_id)
    add_audit_log(
        usuario=request.session.get("central_user", "admin"),
        accion="token_rotado",
        detalle=f"Token rotado para cliente {cliente_id}",
    )
    return RedirectResponse(
        url=(
            f"/clientes?nuevo_token={nuevo_token}"
            f"&nuevo_cliente_id={cliente_id}"
            f"&msg=Token+rotado+correctamente"
        ),
        status_code=303,
    )


# =====================
# R-080 / Ruta 10.4 — Heartbeat y dashboard de salud global
# =====================

import json as _json_mod
from datetime import datetime as _dt


def ensure_heartbeats_table():
    init_db()
    with db_connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS central_heartbeats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id TEXT NOT NULL,
                nombre_cliente TEXT NOT NULL,
                fecha TEXT NOT NULL,
                version_panel TEXT,
                disco_pct INTEGER,
                backups_ok INTEGER,
                ultimo_backup TEXT,
                alertas_activas INTEGER,
                servicios_activos INTEGER,
                uptime_segundos INTEGER,
                datos_extra TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_heartbeats_cliente
            ON central_heartbeats (cliente_id)
            """
        )
        conn.commit()


def save_heartbeat(cliente_id: str, nombre_cliente: str, datos: dict):
    ensure_heartbeats_table()
    with db_connect() as conn:
        conn.execute(
            """
            INSERT INTO central_heartbeats (
                cliente_id, nombre_cliente, fecha,
                version_panel, disco_pct, backups_ok, ultimo_backup,
                alertas_activas, servicios_activos, uptime_segundos, datos_extra
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                cliente_id,
                nombre_cliente,
                now_text(),
                datos.get("version_panel", ""),
                datos.get("disco_pct"),
                datos.get("backups_ok"),
                datos.get("ultimo_backup", ""),
                datos.get("alertas_activas"),
                datos.get("servicios_activos"),
                datos.get("uptime_segundos"),
                datos.get("datos_extra", ""),
            ),
        )
        conn.commit()


def get_last_heartbeat_per_client() -> list:
    ensure_heartbeats_table()
    with db_connect() as conn:
        rows = conn.execute(
            """
            SELECT h.*
            FROM central_heartbeats h
            INNER JOIN (
                SELECT cliente_id, MAX(id) AS max_id
                FROM central_heartbeats
                GROUP BY cliente_id
            ) latest ON h.id = latest.max_id
            ORDER BY h.fecha DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def _semaforo(fecha_str) -> str:
    """Verde < 10 min · Naranja < 60 min · Rojo ≥ 60 min o sin dato."""
    if not fecha_str:
        return "rojo"
    try:
        ts = _dt.strptime(str(fecha_str), "%Y-%m-%d %H:%M:%S")
        minutos = (_dt.now() - ts).total_seconds() / 60
        if minutos < 10:
            return "verde"
        if minutos < 60:
            return "naranja"
        return "rojo"
    except Exception:
        return "rojo"


class HeartbeatIn(BaseModel):
    cliente_id: str = Field(..., min_length=1)
    nombre_cliente: str = Field(..., min_length=1)
    version_panel: Optional[str] = ""
    disco_pct: Optional[int] = None
    backups_ok: Optional[int] = None
    ultimo_backup: Optional[str] = ""
    alertas_activas: Optional[int] = None
    servicios_activos: Optional[int] = None
    uptime_segundos: Optional[int] = None
    datos_extra: Optional[str] = ""


@app.post("/api/v1/heartbeat")
def receive_heartbeat(
    payload: HeartbeatIn,
    x_vigex_client_token: Optional[str] = Header(default=None),
):
    """Recibe heartbeat periódico de un panel cliente. Requiere token válido."""
    if not validate_client_token(payload.cliente_id, x_vigex_client_token):
        raise HTTPException(status_code=401, detail="Token de cliente no válido")
    save_heartbeat(
        cliente_id=payload.cliente_id,
        nombre_cliente=payload.nombre_cliente,
        datos=payload.dict(),
    )
    return {"ok": True, "mensaje": "Heartbeat registrado"}


@app.get("/salud", response_class=HTMLResponse)
def central_salud(request: Request):
    if not is_central_authenticated(request):
        return central_login_redirect()
    heartbeats = get_last_heartbeat_per_client()
    clientes_estado = []
    for hb in heartbeats:
        hb_dict = dict(hb)
        hb_dict["semaforo"] = _semaforo(hb_dict.get("fecha"))
        clientes_estado.append(hb_dict)
    # Clientes sin heartbeat alguno
    todos = list_clients()
    ids_con_hb = {c["cliente_id"] for c in clientes_estado}
    for c in todos:
        if c["id"] not in ids_con_hb and int(c["activo"]) == 1:
            clientes_estado.append({
                "cliente_id": c["id"],
                "nombre_cliente": c["nombre"],
                "fecha": None,
                "semaforo": "rojo",
                "disco_pct": None,
                "backups_ok": None,
                "ultimo_backup": None,
                "alertas_activas": None,
                "servicios_activos": None,
                "version_panel": None,
            })
    verdes   = sum(1 for c in clientes_estado if c["semaforo"] == "verde")
    naranjas = sum(1 for c in clientes_estado if c["semaforo"] == "naranja")
    rojos    = sum(1 for c in clientes_estado if c["semaforo"] == "rojo")
    return templates.TemplateResponse(
        request,
        "central_salud.html",
        {
            "clientes": clientes_estado,
            "verdes": verdes,
            "naranjas": naranjas,
            "rojos": rojos,
            **get_central_session_context(request),
        },
    )


# =====================
# R-081 / Ruta 10.5 — Log de auditoría de acciones de admin
# =====================

def ensure_audit_table():
    init_db()
    with db_connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS central_audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                usuario TEXT NOT NULL,
                accion TEXT NOT NULL,
                detalle TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_audit_usuario
            ON central_audit_log (usuario)
            """
        )
        conn.commit()


def add_audit_log(usuario: str, accion: str, detalle: str = ""):
    ensure_audit_table()
    with db_connect() as conn:
        conn.execute(
            """
            INSERT INTO central_audit_log (fecha, usuario, accion, detalle)
            VALUES (?, ?, ?, ?)
            """,
            (now_text(), usuario, accion, detalle),
        )
        conn.commit()


def get_audit_log(limit: int = 200) -> list:
    ensure_audit_table()
    with db_connect() as conn:
        rows = conn.execute(
            """
            SELECT id, fecha, usuario, accion, detalle
            FROM central_audit_log
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


@app.get("/auditoria", response_class=HTMLResponse)
def central_auditoria(request: Request):
    guard = require_admin(request)
    if guard is not None:
        return guard
    registros = get_audit_log(limit=200)
    return templates.TemplateResponse(
        request,
        "central_auditoria.html",
        {
            "registros": registros,
            **get_central_session_context(request),
        },
    )
