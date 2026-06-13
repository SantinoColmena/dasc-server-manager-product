#!/usr/bin/env python3
"""
Vigex Central — Gestión de licencias por línea de comandos.

Uso:
    python manage_licenses.py list
    python manage_licenses.py get <cliente_id>
    python manage_licenses.py set <cliente_id> --plan lite|standard|pro|managed
                                                [--expiry-licencia YYYY-MM-DD]
                                                [--expiry-soporte  YYYY-MM-DD]
    python manage_licenses.py keygen
    python manage_licenses.py sign <cliente_id> --plan lite|standard|pro|managed
                                                 [--expiry YYYY-MM-DD]

La clave privada se lee de la variable de entorno VIGEX_PRIVATE_KEY
o del fichero ~/.vigex/private.key (nunca la guardes en el repo).

Debe ejecutarse desde el directorio donde está main.py (mismo CWD que Uvicorn),
o con la variable DATABASE_PATH apuntando al fichero central.db.
"""

import argparse
import base64
import json
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


# ── Firma de licencias Ed25519 ───────────────────────────────────────────────

def _load_private_key_bytes() -> bytes:
    """Lee la clave privada desde VIGEX_PRIVATE_KEY (env) o ~/.vigex/private.key."""
    raw = os.environ.get("VIGEX_PRIVATE_KEY", "").strip()
    if raw:
        try:
            return base64.b64decode(raw)
        except Exception:
            print("[Error] VIGEX_PRIVATE_KEY no es base64 válido.", file=sys.stderr)
            sys.exit(1)
    key_file = Path.home() / ".vigex" / "private.key"
    if key_file.exists():
        try:
            return base64.b64decode(key_file.read_text().strip())
        except Exception:
            print(f"[Error] No se pudo leer {key_file}", file=sys.stderr)
            sys.exit(1)
    print(
        "[Error] No se encontró la clave privada.\n"
        "  Opción A: export VIGEX_PRIVATE_KEY=<base64>\n"
        f"  Opción B: guarda la clave en {key_file}",
        file=sys.stderr,
    )
    sys.exit(1)


def cmd_keygen(_args):
    """Genera un nuevo par de claves Ed25519 para firma de licencias."""
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        from cryptography.hazmat.primitives.serialization import (
            Encoding, PublicFormat, PrivateFormat, NoEncryption,
        )
    except ImportError:
        print("[Error] Instala cryptography: pip install cryptography", file=sys.stderr)
        sys.exit(1)

    key = Ed25519PrivateKey.generate()
    priv_b64 = base64.b64encode(
        key.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
    ).decode()
    pub_b64 = base64.b64encode(
        key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    ).decode()

    key_file = Path.home() / ".vigex" / "private.key"
    key_file.parent.mkdir(parents=True, exist_ok=True)
    key_file.write_text(priv_b64)
    key_file.chmod(0o600)

    print()
    print("=" * 60)
    print("  PAR DE CLAVES Ed25519 GENERADO")
    print("=" * 60)
    print()
    print(f"  Clave privada guardada en: {key_file}")
    print(f"  (también disponible como VIGEX_PRIVATE_KEY)")
    print()
    print("  CLAVE PUBLICA — pega este valor en deploy/api/package/main.py")
    print(f"  como _VIGEX_PUBLIC_KEY_B64:")
    print()
    print(f"    {pub_b64}")
    print()
    print("  NUNCA compartas ni comitees la clave privada.")
    print("=" * 60)
    print()


def cmd_sign(args):
    """Genera y firma una clave de licencia para un cliente."""
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    except ImportError:
        print("[Error] Instala cryptography: pip install cryptography", file=sys.stderr)
        sys.exit(1)

    plan = (args.plan or "lite").lower()
    if plan not in PLANES_VALIDOS:
        print(f"[Error] Plan inválido: {plan}", file=sys.stderr)
        sys.exit(1)

    expiry = (args.expiry or "").strip()
    if expiry:
        try:
            datetime.strptime(expiry, "%Y-%m-%d")
        except ValueError:
            print(f"[Error] Fecha inválida: {expiry}. Formato: YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)

    priv_bytes = _load_private_key_bytes()
    try:
        key = Ed25519PrivateKey.from_private_bytes(priv_bytes)
    except Exception as e:
        print(f"[Error] Clave privada inválida: {e}", file=sys.stderr)
        sys.exit(1)

    payload_dict: dict = {
        "client_id": args.cliente_id,
        "plan":      plan,
        "expiry":    expiry,
        "issued":    datetime.now().strftime("%Y-%m-%d"),
    }
    hostname = (getattr(args, "hostname", "") or "").strip()
    if hostname:
        payload_dict["hostname"] = hostname
    payload = json.dumps(payload_dict, separators=(",", ":")).encode()

    sig = key.sign(payload)
    payload_b64 = base64.urlsafe_b64encode(payload).decode().rstrip("=")
    sig_b64     = base64.urlsafe_b64encode(sig).decode().rstrip("=")
    license_key = f"VGX1.{payload_b64}.{sig_b64}"

    print()
    print("=" * 60)
    print(f"  LICENCIA GENERADA — {args.cliente_id}")
    print("=" * 60)
    print(f"  Plan     : {plan}")
    print(f"  Expiry   : {expiry or 'perpetua'}")
    print(f"  Hostname : {hostname or 'sin restricción'}")
    print(f"  Emitida  : {datetime.now().strftime('%Y-%m-%d')}")
    print()
    print("  Clave de licencia:")
    print(f"  {license_key}")
    print()
    print("  Añade al config.env del cliente:")
    print(f"  VIGEX_LICENSE_KEY={license_key}")
    print("=" * 60)
    print()


def cmd_verify(args):
    """Verifica una clave de licencia sin necesitar la clave privada."""
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except ImportError:
        print("[Error] Instala cryptography: pip install cryptography", file=sys.stderr)
        sys.exit(1)

    pub_b64 = os.environ.get("VIGEX_PUBLIC_KEY", "").strip()
    if not pub_b64:
        print("[Error] Proporciona la clave pública via VIGEX_PUBLIC_KEY=<base64>", file=sys.stderr)
        sys.exit(1)

    lk = args.license_key.strip()
    parts = lk.split(".")
    if len(parts) != 3 or parts[0] != "VGX1":
        print("[INVALIDA] Formato incorrecto (esperado: VGX1.<payload>.<firma>)")
        sys.exit(1)

    def _pad(s): return s + "=" * (-len(s) % 4)
    try:
        payload_bytes = base64.urlsafe_b64decode(_pad(parts[1]))
        payload = json.loads(payload_bytes)
        sig = base64.urlsafe_b64decode(_pad(parts[2]))
        pub_key = Ed25519PublicKey.from_public_bytes(base64.b64decode(pub_b64))
        pub_key.verify(sig, payload_bytes)
    except Exception as e:
        print(f"[INVALIDA] {e}")
        sys.exit(1)

    expiry = payload.get("expiry", "")
    expired = False
    if expiry:
        expired = datetime.strptime(expiry, "%Y-%m-%d") < datetime.now()

    print(f"[VALIDA]  client_id={payload.get('client_id')}  plan={payload.get('plan')}  "
          f"expiry={expiry or 'perpetua'}  {'*** CADUCADA ***' if expired else 'vigente'}")


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

    p_set = sub.add_parser("set", help="Actualiza plan y/o fechas de expiración en Central")
    p_set.add_argument("cliente_id")
    p_set.add_argument("--plan", choices=list(PLANES_VALIDOS), help="Plan de licencia")
    p_set.add_argument("--expiry-licencia", metavar="YYYY-MM-DD", help="Fecha fin de licencia (vacío=perpetua)")
    p_set.add_argument("--expiry-soporte", metavar="YYYY-MM-DD", help="Fecha fin del soporte mensual")

    sub.add_parser("keygen", help="Genera un nuevo par de claves Ed25519 (solo la primera vez)")

    p_sign = sub.add_parser("sign", help="Firma y genera la VIGEX_LICENSE_KEY para un cliente")
    p_sign.add_argument("cliente_id")
    p_sign.add_argument("--plan", choices=list(PLANES_VALIDOS), default="lite", help="Plan de licencia")
    p_sign.add_argument("--expiry", metavar="YYYY-MM-DD", default="", help="Fecha de expiración (vacío=perpetua)")
    p_sign.add_argument("--hostname", default="", help="Hostname del servidor destino (vacío = sin restricción)")

    p_verify = sub.add_parser("verify", help="Verifica una clave de licencia (requiere VIGEX_PUBLIC_KEY)")
    p_verify.add_argument("license_key")

    args = parser.parse_args()
    {
        "list":   cmd_list,
        "get":    cmd_get,
        "set":    cmd_set,
        "keygen": cmd_keygen,
        "sign":   cmd_sign,
        "verify": cmd_verify,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
