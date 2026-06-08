#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path


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
        values[key.strip()] = value.strip().strip('"').strip("'")

    return values


def first_config(env: dict, keys: list[str], default: str = "") -> str:
    for key in keys:
        value = env.get(key)
        if value:
            return value

    return default


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def find_mysql_binary() -> str:
    for candidate in ["mariadb", "mysql"]:
        found = shutil.which(candidate)
        if found:
            return found

    raise RuntimeError("No se encontró mariadb ni mysql. Instala mariadb-client.")


def find_latest_backup(backup_dir: Path) -> Path:
    meta_files = sorted(
        backup_dir.glob("*.sql.meta.json"),
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    )

    for meta_file in meta_files:
        try:
            data = json.loads(meta_file.read_text(encoding="utf-8", errors="ignore"))
            output = data.get("output")
            if output and Path(output).exists():
                return Path(output)
        except Exception:
            continue

    sql_files = sorted(
        backup_dir.glob("*.sql"),
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    )

    if not sql_files:
        raise RuntimeError(f"No se encontraron backups .sql en {backup_dir}")

    return sql_files[0]


def verify_sha256(backup_path: Path) -> dict:
    sha_path = Path(str(backup_path) + ".sha256")

    result = {
        "sha_file": str(sha_path),
        "sha_file_exists": sha_path.exists(),
        "expected": "",
        "calculated": "",
        "ok": False,
    }

    if not sha_path.exists():
        return result

    first_line = sha_path.read_text(encoding="utf-8", errors="ignore").splitlines()[0].strip()
    expected = first_line.split()[0] if first_line else ""
    calculated = sha256_file(backup_path)

    result["expected"] = expected
    result["calculated"] = calculated
    result["ok"] = bool(expected and expected == calculated)

    return result


def inspect_target_db(host: str, user: str, password: str, database: str) -> dict:
    result = {
        "status": "ERROR",
        "tables": [],
        "eventos_count": None,
        "error": None,
    }

    try:
        import pymysql

        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            autocommit=True,
            connect_timeout=5,
            cursorclass=pymysql.cursors.DictCursor,
        )

        with conn.cursor() as cur:
            cur.execute("SHOW TABLES")
            rows = cur.fetchall()
            tables = []

            for row in rows:
                tables.extend(str(value) for value in row.values())

            result["tables"] = tables

            if "eventos" in tables:
                cur.execute("SELECT COUNT(*) AS total FROM eventos")
                count_row = cur.fetchone()
                result["eventos_count"] = count_row["total"] if count_row else None

        conn.close()
        result["status"] = "OK"

    except Exception as exc:
        result["error"] = str(exc)

    return result


def write_restore_report(root: Path, payload: dict) -> Path:
    report_dir = root / "reports" / "restores"
    report_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_path = report_dir / f"restore_{timestamp}.json"
    report_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.chmod(report_path, 0o640)

    return report_path


def main():
    parser = argparse.ArgumentParser(description="Restaura un backup completo Vigex en una base de prueba/controlada.")
    parser.add_argument("--root", default="/opt/vigex/api", help="Ruta raíz de instalación API.")
    parser.add_argument("--backup", default="", help="Ruta del backup .sql. Si se omite usa el último backup válido.")
    parser.add_argument("--target-db", default="", help="Base de datos destino de restauración.")
    parser.add_argument("--apply", action="store_true", help="Aplica restauración real. Sin esto solo hace dry-run.")

    args = parser.parse_args()

    root = Path(args.root).resolve()
    env = load_env_file(root / "config.env")

    backup_dir = Path(env.get("BACKUP_OUTPUT_DIR", "/var/backups/vigex/mysql/full")).resolve()
    backup_path = Path(args.backup).resolve() if args.backup else find_latest_backup(backup_dir)

    source_db = first_config(env, ["BACKUP_DB_NAME", "LOGS_DB_NAME"], default="")
    target_db = args.target_db or first_config(env, ["RESTORE_TARGET_DB"], default="vigex_logs_restore_test")

    host = first_config(env, ["RESTORE_DB_HOST", "BACKUP_DB_HOST", "LOGS_DB_HOST"], default="")
    user = first_config(env, ["RESTORE_DB_USER"], default="")
    password = first_config(env, ["RESTORE_DB_PASS"], default="")

    print("Restauración controlada de backup Vigex")
    print(f"Root: {root}")
    print(f"Modo: {'APLICAR' if args.apply else 'DRY-RUN'}")
    print(f"Backup: {backup_path}")
    print(f"Base origen esperada: {source_db or 'No definida'}")
    print(f"Base destino: {target_db}")
    print(f"Host destino: {host}")
    print(f"Usuario restore: {user}")
    print("")

    if not backup_path.exists():
        print("ERROR: no existe el backup indicado.")
        raise SystemExit(1)

    if not str(backup_path).endswith(".sql"):
        print("ERROR: el backup debe ser un archivo .sql.")
        raise SystemExit(1)

    if not host or not user or not password:
        print("ERROR: faltan variables RESTORE_DB_HOST/RESTORE_DB_USER/RESTORE_DB_PASS.")
        raise SystemExit(1)

    if source_db and target_db == source_db:
        print("ERROR: la base destino coincide con la base original. Operación bloqueada por seguridad.")
        raise SystemExit(1)

    sha = verify_sha256(backup_path)

    if not sha["sha_file_exists"]:
        print("ERROR: falta el archivo .sha256 asociado al backup.")
        raise SystemExit(1)

    if not sha["ok"]:
        print("ERROR: el SHA256 no coincide.")
        print(f"Esperado: {sha['expected']}")
        print(f"Calculado: {sha['calculated']}")
        raise SystemExit(1)

    print("SHA256: OK")

    before = inspect_target_db(host, user, password, target_db)

    if before["status"] != "OK":
        print("ERROR: no se puede acceder a la base destino.")
        print(before["error"])
        raise SystemExit(1)

    print(f"Conexión destino: OK")
    print(f"Tablas antes: {', '.join(before['tables']) if before['tables'] else '(sin tablas)'}")
    print(f"Eventos antes: {before['eventos_count'] if before['eventos_count'] is not None else 'No disponible'}")
    print("")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "apply" if args.apply else "dry-run",
        "root": str(root),
        "backup": str(backup_path),
        "sha256": sha,
        "source_db": source_db,
        "target_db": target_db,
        "host": host,
        "user": user,
        "before": before,
        "after": None,
        "status": "DRY-RUN",
    }

    if not args.apply:
        report_path = write_restore_report(root, payload)
        print("DRY-RUN: no se ha restaurado nada. Usa --apply para aplicar la restauración real.")
        print(f"Evidencia: {report_path}")
        print("Resultado: OK")
        return

    mysql_binary = find_mysql_binary()

    fd, tmp_config_name = tempfile.mkstemp(prefix="vigex_restore_", suffix=".cnf")
    tmp_config = Path(tmp_config_name)

    try:
        os.close(fd)
        os.chmod(tmp_config, 0o600)

        tmp_config.write_text(
            "[client]\n"
            f"host={host}\n"
            f"user={user}\n"
            f"password={password}\n",
            encoding="utf-8",
        )

        command = [
            mysql_binary,
            f"--defaults-extra-file={tmp_config}",
            target_db,
        ]

        with backup_path.open("rb") as input_file:
            completed = subprocess.run(
                command,
                stdin=input_file,
                stderr=subprocess.PIPE,
                check=False,
            )

        if completed.returncode != 0:
            payload["status"] = "ERROR"
            payload["error"] = completed.stderr.decode("utf-8", errors="ignore")
            report_path = write_restore_report(root, payload)

            print("ERROR: falló la restauración.")
            print(payload["error"])
            print(f"Evidencia: {report_path}")
            raise SystemExit(completed.returncode)

    finally:
        try:
            tmp_config.unlink(missing_ok=True)
        except Exception:
            pass

    after = inspect_target_db(host, user, password, target_db)
    payload["after"] = after

    if after["status"] != "OK":
        payload["status"] = "ERROR"
        payload["error"] = after["error"]
        report_path = write_restore_report(root, payload)

        print("ERROR: restauración aplicada pero no se pudo validar después.")
        print(after["error"])
        print(f"Evidencia: {report_path}")
        raise SystemExit(1)

    payload["status"] = "OK"
    report_path = write_restore_report(root, payload)

    print("Restauración aplicada correctamente.")
    print(f"Tablas después: {', '.join(after['tables']) if after['tables'] else '(sin tablas)'}")
    print(f"Eventos después: {after['eventos_count'] if after['eventos_count'] is not None else 'No disponible'}")
    print(f"Evidencia: {report_path}")
    print("Resultado: OK")


if __name__ == "__main__":
    main()
