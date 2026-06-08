#!/usr/bin/env python3
import argparse
import json
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


def safe_cell(value) -> str:
    text = str(value if value is not None else "-")
    text = text.replace("|", "/")
    text = text.replace("\n", " ")
    return text


def markdown_table(rows):
    output = []
    output.append("| Campo | Valor |")
    output.append("|---|---|")

    for key, value in rows:
        output.append(f"| {safe_cell(key)} | {safe_cell(value)} |")

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


def load_backup_metadata(meta_path: Path) -> dict:
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8", errors="ignore"))
        data["_meta_path"] = str(meta_path)
        data["_meta_exists"] = True
        return data
    except Exception as exc:
        return {
            "_meta_path": str(meta_path),
            "_meta_exists": False,
            "_error": str(exc),
        }


def inspect_backups(env: dict):
    backup_dir = Path(env.get("BACKUP_OUTPUT_DIR", "/var/backups/vigex/mysql/full")).expanduser()

    result = {
        "status": "No comprobado",
        "backup_dir": str(backup_dir),
        "latest": None,
        "recent": [],
        "error": None,
    }

    if not backup_dir.exists():
        result["status"] = "No comprobado: no existe el directorio de backups"
        return result

    meta_files = sorted(
        backup_dir.glob("*.sql.meta.json"),
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    )

    if not meta_files:
        result["status"] = "No hay backups con metadata"
        return result

    for meta_file in meta_files[:5]:
        meta = load_backup_metadata(meta_file)

        output_path = Path(str(meta.get("output", ""))) if meta.get("output") else None
        sha_path = Path(str(output_path) + ".sha256") if output_path else None

        output_exists = output_path.exists() if output_path else False
        sha_exists = sha_path.exists() if sha_path else False
        real_size = output_path.stat().st_size if output_exists else 0

        meta["output_exists"] = output_exists
        meta["sha_exists"] = sha_exists
        meta["real_size_bytes"] = real_size

        if output_exists and sha_exists and meta.get("has_create_table") is True:
            meta["validation_status"] = "OK"
        else:
            meta["validation_status"] = "REVISAR"

        result["recent"].append(meta)

    result["latest"] = result["recent"][0]

    if result["latest"]["validation_status"] == "OK":
        result["status"] = "OK"
    else:
        result["status"] = "REVISAR"

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
    backups = inspect_backups(env)

    lines = []

    lines.append("# Informe operativo Vigex")
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
    lines.append("Este informe se genera desde el paquete API de Vigex.")
    lines.append("")
    lines.append("Su objetivo es acercar el informe mensual desde una herramienta interna de GitHub hacia una herramienta real de producto.")
    lines.append("")
    lines.append("Esta versión todavía es operativa básica, pero ya está pensada para ejecutarse en el servidor donde se instala Vigex.")
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
        if (
            key in REQUIRED_KEYS
            or key.startswith("TELEGRAM_")
            or key.startswith("ALERTS_")
            or key.startswith("BACKUP_")
            or key.endswith("_HOST")
        ):
            lines.append(f"| {safe_cell(key)} | {safe_cell(mask_value(key, env.get(key, '')))} |")

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
            fecha = safe_cell(event.get("fecha", "-"))
            tipo = safe_cell(event.get("tipo", "-"))
            usuario = safe_cell(event.get("usuario", "-"))
            recurso = safe_cell(event.get("recurso", "-"))
            resultado = safe_cell(event.get("resultado", "-"))
            detalle = safe_cell(event.get("detalle", "-"))
            lines.append(f"| {fecha} | {tipo} | {usuario} | {recurso} | {resultado} | {detalle} |")

        lines.append("")

    lines.append("## 7. Backups completos")
    lines.append("")

    latest_backup = backups.get("latest")

    if latest_backup:
        lines.extend(markdown_table([
            ("Estado", backups["status"]),
            ("Directorio", backups["backup_dir"]),
            ("Último backup", latest_backup.get("output", "No disponible")),
            ("Fecha metadata", latest_backup.get("generated_at", "No disponible")),
            ("Base de datos", latest_backup.get("database", "No disponible")),
            ("Host origen", latest_backup.get("host", "No disponible")),
            ("Usuario backup", latest_backup.get("user", "No disponible")),
            ("Tamaño bytes", latest_backup.get("real_size_bytes", latest_backup.get("size_bytes", "No disponible"))),
            ("SHA256", latest_backup.get("sha256", "No disponible")),
            ("Archivo SQL existe", "OK" if latest_backup.get("output_exists") else "FALTA"),
            ("Archivo SHA256 existe", "OK" if latest_backup.get("sha_exists") else "FALTA"),
            ("Contiene CREATE TABLE", latest_backup.get("has_create_table", "No disponible")),
            ("Contiene INSERT INTO", latest_backup.get("has_insert_into", "No disponible")),
            ("Binario dump", latest_backup.get("dump_binary", "No disponible")),
            ("Etiqueta", latest_backup.get("label", "No disponible")),
        ]))
        lines.append("")

        if backups["recent"]:
            lines.append("Últimos backups detectados:")
            lines.append("")
            lines.append("| Fecha | Base | Archivo | Tamaño | Estado |")
            lines.append("|---|---|---|---|---|")

            for item in backups["recent"]:
                lines.append(
                    f"| {safe_cell(item.get('generated_at', '-'))} "
                    f"| {safe_cell(item.get('database', '-'))} "
                    f"| {safe_cell(item.get('output', '-'))} "
                    f"| {safe_cell(item.get('real_size_bytes', item.get('size_bytes', '-')))} "
                    f"| {safe_cell(item.get('validation_status', '-'))} |"
                )

            lines.append("")
    else:
        lines.extend(markdown_table([
            ("Estado", backups["status"]),
            ("Directorio", backups["backup_dir"]),
        ]))
        lines.append("")

    if backups.get("error"):
        lines.append("Error detectado en backups:")
        lines.append("")
        lines.append("~~~text")
        lines.append(str(backups["error"]))
        lines.append("~~~")
        lines.append("")

    lines.append("## 8. Limitaciones de esta versión")
    lines.append("")
    lines.append("Esta versión todavía no sustituye un informe mensual final para cliente.")
    lines.append("")
    lines.append("Pendiente para evolucionar a herramienta lista para cliente:")
    lines.append("")
    lines.append("- Incluir última restauración de prueba de forma automática.")
    lines.append("- Incluir alertas enviadas.")
    lines.append("- Incluir estado de servicios.")
    lines.append("- Generar una versión resumida para cliente no técnico.")
    lines.append("- Exportar a PDF o enviar por email.")
    lines.append("")

    lines.append("## 9. Conclusión")
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

    elif backups["status"] in ("ERROR", "REVISAR"):
        lines.append("Resultado: OPERATIVO PARCIAL.")
        lines.append("")
        lines.append("La configuración y logs funcionan, pero el estado de backups requiere revisión.")

    elif backups["status"] == "OK":
        lines.append("Resultado: BASE OPERATIVA OK CON BACKUP.")
        lines.append("")
        lines.append("El informe operativo puede generarse desde el paquete API, consulta logs reales y detecta el último backup completo válido.")

    else:
        lines.append("Resultado: BASE OPERATIVA OK.")
        lines.append("")
        lines.append("El informe operativo puede generarse desde el paquete API y sirve como base para evolucionar hacia informe real de cliente.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Genera un informe operativo de Vigex.")
    parser.add_argument("--root", default=".", help="Ruta raíz de la instalación API. Ej: /opt/vigex/api")
    parser.add_argument("--client", default="Vigex interno", help="Nombre de cliente o entorno.")
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