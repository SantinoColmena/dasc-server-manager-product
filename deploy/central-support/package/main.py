import os
import hmac
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "central_support.db"

APP_NAME = "DASC Central Support"
DEMO_CLIENT_ID = os.getenv("DASC_CENTRAL_DEMO_CLIENT_ID", "cliente-demo-a")
DEMO_CLIENT_NAME = os.getenv("DASC_CENTRAL_DEMO_CLIENT_NAME", "Cliente Demo A")
DEMO_CLIENT_TOKEN = os.getenv("DASC_CENTRAL_DEMO_TOKEN", "dasc-central-demo-token-lab")

# =====================
# R-049Q - CONFIG AUTENTICACION CENTRAL
# =====================

CENTRAL_AUTH_ENABLED = os.getenv("DASC_CENTRAL_AUTH_ENABLED", "true").strip().lower() in ("1", "true", "yes", "on")
CENTRAL_SECRET_KEY = os.getenv("DASC_CENTRAL_SECRET_KEY", "dasc-central-support-secret-lab-change-me")
CENTRAL_ADMIN_USER = os.getenv("DASC_CENTRAL_ADMIN_USER", "admin")
CENTRAL_ADMIN_PASSWORD = os.getenv("DASC_CENTRAL_ADMIN_PASSWORD", "admin")
CENTRAL_TECH_USER = os.getenv("DASC_CENTRAL_TECH_USER", "tecnico")
CENTRAL_TECH_PASSWORD = os.getenv("DASC_CENTRAL_TECH_PASSWORD", "tecnico")


app = FastAPI(title=APP_NAME)
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

    return str(row["token"]) == str(token)


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


@app.on_event("startup")
def startup():
    init_db()


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
    x_dasc_client_token: Optional[str] = Header(default=None),
):
    if not validate_client_token(payload.cliente_id, x_dasc_client_token):
        raise HTTPException(status_code=401, detail="Token de cliente no válido")

    ticket_id = create_central_ticket(payload)

    return {
        "ok": True,
        "central_ticket_id": ticket_id,
        "estado": "Nuevo",
        "mensaje": "Ticket recibido en API central DASC",
    }



# =====================
# R-049P - API CONSULTA TICKET CENTRAL
# =====================

@app.get("/api/v1/support/tickets/{ticket_id}")
def api_get_support_ticket_status(
    ticket_id: str,
    x_dasc_client_token: Optional[str] = Header(default=None),
    x_dasc_client_id: Optional[str] = Header(default=None),
):
    ticket = get_central_ticket(ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket central no encontrado")

    client_id = (x_dasc_client_id or "").strip()

    if not client_id:
        raise HTTPException(status_code=400, detail="Falta cabecera X-DASC-Client-ID")

    if client_id != ticket.get("cliente_id"):
        raise HTTPException(status_code=403, detail="El ticket no pertenece al cliente indicado")

    if not validate_client_token(client_id, x_dasc_client_token):
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

    if CENTRAL_ADMIN_USER and CENTRAL_ADMIN_PASSWORD:
        users[CENTRAL_ADMIN_USER] = {
            "password": CENTRAL_ADMIN_PASSWORD,
            "role": "admin",
            "label": "Administrador central",
        }

    if CENTRAL_TECH_USER and CENTRAL_TECH_PASSWORD:
        users[CENTRAL_TECH_USER] = {
            "password": CENTRAL_TECH_PASSWORD,
            "role": "tecnico",
            "label": "Tecnico DASC",
        }

    return users


def validate_central_login(username, password):
    username = (username or "").strip()
    password = password or ""

    users = get_central_users()
    user = users.get(username)

    if not user:
        return None

    expected = user.get("password", "")

    if not hmac.compare_digest(password, expected):
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
            detalle="Actualización realizada desde panel central DASC",
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

    usuario = request.session.get("central_user", "dasc_tecnico_lab")

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
