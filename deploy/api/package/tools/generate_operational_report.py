#!/usr/bin/env python3
import argparse
from datetime import datetime
from pathlib import Path


SENSITIVE_WORDS = [
    "PASS",
    "PASSWORD",
    "TOKEN",
    "SECRET",
    "KEY",
    "CHAT_ID",
]


REQUIRED_KEYS = [
    "SECRET_KEY",
    "ADMIN_USER",
    "ADMIN_PASSWORD",
    "SSH_USER",
    "BACKUPS_HOST",
    "SERVICIOS_HOST",
    "LOGS_DB_HOST",
    "LOGS_DB_NAME",
    "LOGS_DB_USER",
    "LOGS_DB_PASS",
]


def load_env_file(path: Path) -> dict:
    values = {}

    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        values[key] = value

    return values


def mask_value(key: str, value: str) -> str:
    upper_key = key.upper()

    if any(word in upper_key for word in SENSITIVE_WORDS):
        if not value:
            return "(vacío)"
        return "***"

    if value == "":
        return "(vacío)"

    return value


def markdown_table(rows):
    output = []
    output.append("| Campo | Valor |")
    output.append("|---|---|")

    for key, value in rows:
        output.append(f"| {key} | {value} |")

    return output


def check_config(env: dict):
    rows = []
    missing = []

    for key in REQUIRED_KEYS:
        if key in env and str(env.get(key, "")).strip():
            rows.append((key, "OK"))
        else:
            rows.append((key, "FALTA"))
            missing.append(key)

    return rows, missing


def inspect_runtime_files(root: Path):
    data_dir = root / "data"
    reports_dir = root / "reports"
    users_file = data_dir / "users.json"
    alerts_db = data_dir / "alerts.db"

    rows = [
        ("Directorio data", "OK" if data_dir.exists() else "FALTA"),
        ("Directorio reports", "OK" if reports_dir.exists() else "FALTA"),
        ("users.json runtime", "OK" if users_file.exists() else "No existe todavía"),
        ("alerts.db runtime", "OK" if alerts_db.exists() else "No existe todavía"),
    ]

    return rows


def inspect_logs_db(env: dict):
    result = {
        "available": False,
        "status": "No comprobada",
        "total_events": None,
        "recent_events": [],
        "error": None,
    }

    required = ["LOGS_DB_HOST", "LOGS_DB_NAME", "LOGS_DB_USER", "LOGS_DB_PASS"]
    if not all(env.get(k) for k in required):
        result["status"] = "No comprobada: faltan variables LOGS_DB_*"
        return result

    try:
        import pymysql

        conn = pymysql.connect(
            host=env["LOGS_DB_HOST"],
            user=env["LOGS_DB_USER"],
            password=env["LOGS_DB_PASS"],
            database=env["LOGS_DB_NAME"],
            autocommit=True,
            connect_timeout=3,
            cursorclass=pymysql.cursors.DictCursor,
        )

        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS total FROM eventos")
            row = cur.fetchone()
            result["total_events"] = row["total"] if row else 0

            cur.execute(
                """
                SELECT fecha, tipo, usuario, recurso, resultado, detalle
                FROM eventos
                ORDER BY fecha DESC
                LIMIT 10
                """
            )
            result["recent_events"] = cur.fetchall()

        conn.close()

        result["available"] = True
        result["status"] = "OK"

    except Exception as exc:
        result["status"] = "ERROR"
        result["error"] = str(exc)

    return result


def build_report(root: Path, client: str, period: str, output_path: Path):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    config_path = root / "config.env"
    config_mode = "real"

    if not config_path.exists():
        config_path = root / "config.env.example"
        config_mode = "ejemplo"

    env = load_env_file(config_path)
    config_rows, missing_config = check_config(env)
    runtime_rows = inspect_runtime_files(root)
    logs_db = inspect_logs_db(env)

    lines = []

    lines.append("# Informe operativo DASC Server Manager")
    lines.append("")
    lines.append("## 1. Datos generales")
    lines.append("")
    lines.extend(markdown_table([
        ("Cliente / entorno", client),
        ("Periodo", period),
        ("Fecha de generación", now),
        ("Ruta de instalación revisada", str(root)),
        ("Archivo de configuración leído", str(config_path)),
        ("Modo de configuración", config_mode),
    ]))
    lines.append("")

    lines.append("## 2. Resumen")
    lines.append("")
    lines.append("Este informe se genera desde el paquete API de DASC Server Manager.")
    lines.append("")
    lines.append("Su objetivo es acercar el informe mensual desde una herramienta interna de GitHub hacia una herramienta real de producto.")
    lines.append("")
    lines.append("Esta versión todavía es operativa básica, pero ya está pensada para ejecutarse en el servidor donde se instala DASC.")
    lines.append("")

    lines.append("## 3. Configuración mínima")
    lines.append("")
    lines.extend(markdown_table(config_rows))
    lines.append("")

    lines.append("## 4. Variables relevantes detectadas")
    lines.append("")
    lines.append("| Variable | Valor seguro |")
    lines.append("|---|---|")

    for key in sorted(env.keys()):
        if key in REQUIRED_KEYS or key.startswith("TELEGRAM_") or key.startswith("ALERTS_") or key.endswith("_HOST"):
            lines.append(f"| {key} | {mask_value(key, env.get(key, ''))} |")

    lines.append("")

    lines.append("## 5. Archivos runtime")
    lines.append("")
    lines.extend(markdown_table(runtime_rows))
    lines.append("")

    lines.append("## 6. Base de datos de logs")
    lines.append("")
    lines.extend(markdown_table([
        ("Estado", logs_db["status"]),
        ("Eventos totales", str(logs_db["total_events"]) if logs_db["total_events"] is not None else "No disponible"),
    ]))
    lines.append("")

    if logs_db["error"]:
        lines.append("Error detectado:")
        lines.append("")
        lines.append("~~~text")
        lines.append(logs_db["error"])
        lines.append("~~~")
        lines.append("")

    if logs_db["recent_events"]:
        lines.append("Últimos eventos registrados:")
        lines.append("")
        lines.append("| Fecha | Tipo | Usuario | Recurso | Resultado | Detalle |")
        lines.append("|---|---|---|---|---|---|")

        for event in logs_db["recent_events"]:
            fecha = str(event.get("fecha", "-"))
            tipo = str(event.get("tipo", "-"))
            usuario = str(event.get("usuario", "-"))
            recurso = str(event.get("recurso", "-")).replace("|", "/")
            resultado = str(event.get("resultado", "-"))
            detalle = str(event.get("detalle", "-")).replace("|", "/")
            lines.append(f"| {fecha} | {tipo} | {usuario} | {recurso} | {resultado} | {detalle} |")

        lines.append("")

    lines.append("## 7. Limitaciones de esta versión")
    lines.append("")
    lines.append("Esta versión todavía no sustituye un informe mensual final para cliente.")
    lines.append("")
    lines.append("Pendiente para evolucionar a herramienta lista para cliente:")
    lines.append("")
    lines.append("- Consultar estado real de backups.")
    lines.append("- Incluir última restauración de prueba.")
    lines.append("- Incluir alertas enviadas.")
    lines.append("- Incluir estado de servicios.")
    lines.append("- Generar una versión resumida para cliente no técnico.")
    lines.append("- Exportar a PDF o enviar por email.")
    lines.append("")

    lines.append("## 8. Conclusión")
    lines.append("")

    if missing_config:
        lines.append("Resultado: REVISAR CONFIGURACIÓN.")
        lines.append("")
        lines.append("Faltan variables mínimas para considerar el entorno preparado:")
        lines.append("")
        for key in missing_config:
            lines.append(f"- {key}")
    elif logs_db["status"] == "ERROR":
        lines.append("Resultado: OPERATIVO PARCIAL.")
        lines.append("")
        lines.append("La configuración mínima existe, pero la base de datos de logs no se pudo consultar.")
    else:
        lines.append("Resultado: BASE OPERATIVA OK.")
        lines.append("")
        lines.append("El informe operativo puede generarse desde el paquete API y sirve como base para evolucionar hacia informe real de cliente.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Genera un informe operativo de DASC Server Manager.")
    parser.add_argument("--root", default=".", help="Ruta raíz de la instalación API. Ej: /opt/dasc/api")
    parser.add_argument("--client", default="DASC interno", help="Nombre de cliente o entorno.")
    parser.add_argument("--period", default=datetime.now().strftime("%Y-%m"), help="Periodo del informe. Ej: 2026-05")
    parser.add_argument("--output", default="", help="Ruta de salida del informe Markdown.")

    args = parser.parse_args()

    root = Path(args.root).resolve()

    if args.output:
        output_path = Path(args.output).resolve()
    else:
        safe_period = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in args.period)
        output_path = root / "reports" / f"informe_operativo_{safe_period}.md"

    generated = build_report(
        root=root,
        client=args.client,
        period=args.period,
        output_path=output_path,
    )

    print(f"Informe operativo generado en: {generated}")


if __name__ == "__main__":
    main()
