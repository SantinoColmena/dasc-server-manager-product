#!/usr/bin/env python3
import os
import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_DIR))
os.chdir(APP_DIR)

try:
    import main
except Exception as exc:
    print(f"ERROR: no se pudo importar main.py: {exc}")
    raise


def to_int(value, default):
    try:
        return int(value)
    except Exception:
        return default


def main_cli():
    limit = to_int(os.getenv("DASC_CENTRAL_RETRY_LIMIT", "50"), 50)

    results = main.retry_pending_central_sync_tickets(limit=limit)

    total = len(results)
    sent = sum(1 for item in results if item.get("sent"))
    errors = sum(1 for item in results if item.get("status") == "error")
    skipped = sum(1 for item in results if item.get("status") == "disabled")

    detail = (
        f"Reintento automatico central: "
        f"total={total}, enviados={sent}, errores={errors}, omitidos={skipped}"
    )

    print(detail)

    try:
        main.log_event(
            tipo="soporte",
            resultado="OK" if errors == 0 else "ERROR",
            usuario="systemd-timer",
            ip_origen="127.0.0.1",
            recurso="SYSTEMD TIMER /soporte/tickets/reintentar-central",
            detalle=detail,
        )
    except Exception as exc:
        print(f"AVISO: no se pudo registrar log en MariaDB: {exc}")

    for item in results:
        print(item)

    return 0


if __name__ == "__main__":
    raise SystemExit(main_cli())
