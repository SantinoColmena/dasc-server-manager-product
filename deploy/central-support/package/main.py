import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "central_support.db"

APP_NAME = "DASC Central Support"
DEMO_CLIENT_ID = os.getenv("DASC_CENTRAL_DEMO_CLIENT_ID", "cliente-demo-a")
DEMO_CLIENT_NAME = os.getenv("DASC_CENTRAL_DEMO_CLIENT_NAME", "Cliente Demo A")
DEMO_CLIENT_TOKEN = os.getenv("DASC_CENTRAL_DEMO_TOKEN", "dasc-central-demo-token-lab")

app = FastAPI(title=APP_NAME)
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


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    tickets = list_tickets(limit=100)

    return templates.TemplateResponse(
        request,
        "central_dashboard.html",
        {
            "tickets": tickets,
            "total": len(tickets),
            "demo_client_id": DEMO_CLIENT_ID,
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
    ticket = get_central_ticket(ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket central no encontrado")

    return templates.TemplateResponse(
        request,
        "central_ticket_detail.html",
        {
            "ticket": ticket,
        },
    )
