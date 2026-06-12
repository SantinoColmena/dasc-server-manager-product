#!/usr/bin/env python3
"""
Vigex Central — Gestión de licencias por línea de comandos.

Uso:
    python manage_licenses.py list
    python manage_licenses.py get <cliente_id>
    python manage_licenses.py set <cliente_id> --plan lite|standard|pro|managed
                                                [--expiry-licencia YYYY-MM-DD]
                                                [--expiry-soporte  YYYY-MM-DD]

Debe ejecutarse desde el directorio donde está main.py (mismo CWD que Uvicorn),
o con la variable DATABASE_PATH apuntando al fichero central.db.
"""

import argparse
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Localizar la base de datos ──────────────────────────────────────────────
_SCRIPT_DIR = Path(__file__).resolve().parent
_DB_PATH = Path(os.environ.get("DATABASE_PATH", str(_SCRIPT_DIR / "data" / "central.db")))

PLANES_VALIDOS = {"lite", "standard", "pro", "managed"}


def _connect():
    if not _DB_PATH.exists():
        print(f"[Error] Base de datos no encontrada: {_DB_PATH}", file=sys.stderr)
        print("       Arranca Vigex Central al menos una vez antes de usar este script.", file=sys.stderr)
        sys.exit(1)
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def _soporte_estado(expiry_soporte: str | None) -> str:
    if not expiry_soporte:
        return "sin soporte"
    try:
        dias = (datetime.strptime(expiry_soporte, "%Y-%m-%d") - datetime.now()).days
        if dias >= 0:
            return f"activo ({dias}d restantes)"
        return f"caducado hace {abs(dias)}d"
    except ValueError:
        return f"fecha inválida: {expiry_soporte}"


def cmd_list(_args):
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, nombre, activo, plan, expiry_licencia, expiry_soporte FROM central_clients ORDER BY fecha_alta"
        ).fetchall()
    if not rows:
        print("No hay clientes registrados.")
        return
    print(f"{'ID':<28} {'Nombre':<26} {'Plan':<10} {'Soporte'}")
    print("-" * 80)
    for r in rows:
        estado_activo = "✓" if r["activo"] else "✗"
        soporte = _soporte_estado(r["expiry_soporte"])
        print(f"[{estado_activo}] {r['id']:<26} {r['nombre']:<26} {r['plan'] or 'lite':<10} {soporte}")


def cmd_get(args):
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, nombre, activo, plan, expiry_licencia, expiry_soporte, fecha_alta FROM central_clients WHERE id = ?",
            (args.cliente_id,),
        ).fetchone()
    if not row:
        print(f"[Error] Cliente '{args.cliente_id}' no encontrado.", file=sys.stderr)
        sys.exit(1)
    print(f"ID              : {row['id']}")
    print(f"Nombre          : {row['nombre']}")
    print(f"Activo          : {'Sí' if row['activo'] else 'No'}")
    print(f"Plan            : {row['plan'] or 'lite'}")
    print(f"Licencia hasta  : {row['expiry_licencia'] or 'perpetua'}")
    print(f"Soporte hasta   : {row['expiry_soporte'] or '—'} ({_soporte_estado(row['expiry_soporte'])})")
    print(f"Alta            : {row['fecha_alta']}")


def cmd_set(args):
    plan = (args.plan or "").lower().strip() if args.plan else None
    if plan and plan not in PLANES_VALIDOS:
        print(f"[Error] Plan inválido: '{plan}'. Opciones: {', '.join(sorted(PLANES_VALIDOS))}", file=sys.stderr)
        sys.exit(1)

    for campo, val in [("--expiry-licencia", args.expiry_licencia), ("--expiry-soporte", args.expiry_soporte)]:
        if val:
            try:
                datetime.strptime(val, "%Y-%m-%d")
            except ValueError:
                print(f"[Error] Fecha inválida para {campo}: '{val}'. Formato esperado: YYYY-MM-DD", file=sys.stderr)
                sys.exit(1)

    with _connect() as conn:
        row = conn.execute("SELECT id FROM central_clients WHERE id = ?", (args.cliente_id,)).fetchone()
        if not row:
            print(f"[Error] Cliente '{args.cliente_id}' no encontrado.", file=sys.stderr)
            sys.exit(1)

        updates = []
        params = []
        if plan:
            updates.append("plan = ?")
            params.append(plan)
        if args.expiry_licencia is not None:
            updates.append("expiry_licencia = ?")
            params.append(args.expiry_licencia or None)
        if args.expiry_soporte is not None:
            updates.append("expiry_soporte = ?")
            params.append(args.expiry_soporte or None)

        if not updates:
            print("[Aviso] No se especificó ningún campo a actualizar (--plan, --expiry-licencia, --expiry-soporte).")
            return

        params.append(args.cliente_id)
        conn.execute(f"UPDATE central_clients SET {', '.join(updates)} WHERE id = ?", params)
        conn.commit()

    print(f"[OK] Licencia actualizada para '{args.cliente_id}'.")
    cmd_get(args)


def main():
    parser = argparse.ArgumentParser(
        description="Gestión de licencias Vigex Central",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="Lista todos los clientes con su estado de licencia")

    p_get = sub.add_parser("get", help="Muestra el detalle de licencia de un cliente")
    p_get.add_argument("cliente_id")

    p_set = sub.add_parser("set", help="Actualiza plan y/o fechas de expiración")
    p_set.add_argument("cliente_id")
    p_set.add_argument("--plan", choices=list(PLANES_VALIDOS), help="Plan de licencia")
    p_set.add_argument("--expiry-licencia", metavar="YYYY-MM-DD", help="Fecha fin de licencia (vacío=perpetua)")
    p_set.add_argument("--expiry-soporte", metavar="YYYY-MM-DD", help="Fecha fin del soporte mensual")

    args = parser.parse_args()
    {"list": cmd_list, "get": cmd_get, "set": cmd_set}[args.cmd](args)


if __name__ == "__main__":
    main()
