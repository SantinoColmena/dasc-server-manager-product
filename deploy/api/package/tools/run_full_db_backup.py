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


def get_config_value(env: dict, primary: str, fallback: str = "", default: str = "") -> str:
    if env.get(primary):
        return env[primary]

    if fallback and env.get(fallback):
        return env[fallback]

    return default


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def find_dump_binary() -> str:
    for candidate in ["mariadb-dump", "mysqldump"]:
        found = shutil.which(candidate)
        if found:
            return found

    raise RuntimeError("No se encontró mariadb-dump ni mysqldump. Instala mariadb-client.")


def validate_backup(path: Path) -> dict:
    result = {
        "exists": path.exists(),
        "size_bytes": path.stat().st_size if path.exists() else 0,
        "has_create_table": False,
        "has_insert_into": False,
    }

    if not path.exists() or result["size_bytes"] == 0:
        return result

    text = path.read_text(encoding="utf-8", errors="ignore")
    result["has_create_table"] = "CREATE TABLE" in text
    result["has_insert_into"] = "INSERT INTO" in text

    return result


def main():
    parser = argparse.ArgumentParser(description="Genera backup completo de base de datos remota para Vigex.")
    parser.add_argument("--root", default="/opt/vigex/api", help="Ruta raíz de la instalación API.")
    parser.add_argument("--database", default="", help="Base de datos a copiar. Si se omite, usa BACKUP_DB_NAME o LOGS_DB_NAME.")
    parser.add_argument("--output-dir", default="", help="Directorio de salida. Si se omite, usa BACKUP_OUTPUT_DIR o /var/backups/vigex/mysql/full.")
    parser.add_argument("--label", default="manual", help="Etiqueta opcional para identificar el backup.")

    args = parser.parse_args()

    root = Path(args.root).resolve()
    env_path = root / "config.env"
    env = load_env_file(env_path)

    db_host = get_config_value(env, "BACKUP_DB_HOST", "LOGS_DB_HOST")
    db_name = args.database or get_config_value(env, "BACKUP_DB_NAME", "LOGS_DB_NAME")
    db_user = get_config_value(env, "BACKUP_DB_USER", "LOGS_DB_USER")
    db_pass = get_config_value(env, "BACKUP_DB_PASS", "LOGS_DB_PASS")
    output_dir = Path(args.output_dir or get_config_value(env, "BACKUP_OUTPUT_DIR", default="/var/backups/vigex/mysql/full")).resolve()

    missing = []
    for key, value in [
        ("BACKUP_DB_HOST/LOGS_DB_HOST", db_host),
        ("BACKUP_DB_NAME/LOGS_DB_NAME", db_name),
        ("BACKUP_DB_USER/LOGS_DB_USER", db_user),
        ("BACKUP_DB_PASS/LOGS_DB_PASS", db_pass),
    ]:
        if not value:
            missing.append(key)

    if missing:
        print("ERROR: faltan variables de configuración:")
        for item in missing:
            print(f"- {item}")
        raise SystemExit(1)

    dump_binary = find_dump_binary()
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_db = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in db_name)
    safe_label = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in args.label)

    backup_path = output_dir / f"{safe_db}_full_{timestamp}_{safe_label}.sql"
    sha_path = Path(str(backup_path) + ".sha256")
    meta_path = Path(str(backup_path) + ".meta.json")

    fd, tmp_config_name = tempfile.mkstemp(prefix="vigex_backup_", suffix=".cnf")
    tmp_config = Path(tmp_config_name)

    try:
        os.close(fd)
        os.chmod(tmp_config, 0o600)

        tmp_config.write_text(
            "[client]\n"
            f"host={db_host}\n"
            f"user={db_user}\n"
            f"password={db_pass}\n",
            encoding="utf-8",
        )

        command = [
            dump_binary,
            f"--defaults-extra-file={tmp_config}",
            "--single-transaction",
            "--routines",
            "--events",
            "--triggers",
            db_name,
        ]

        with backup_path.open("wb") as output_file:
            completed = subprocess.run(
                command,
                stdout=output_file,
                stderr=subprocess.PIPE,
                check=False,
            )

        if completed.returncode != 0:
            if backup_path.exists():
                backup_path.unlink(missing_ok=True)

            print("ERROR: mysqldump/mariadb-dump falló.")
            print(completed.stderr.decode("utf-8", errors="ignore"))
            raise SystemExit(completed.returncode)

        os.chmod(backup_path, 0o640)

        validation = validate_backup(backup_path)

        if not validation["exists"] or validation["size_bytes"] == 0:
            print("ERROR: el backup no existe o está vacío.")
            raise SystemExit(1)

        if not validation["has_create_table"]:
            print("ERROR: el backup no contiene CREATE TABLE.")
            raise SystemExit(1)

        digest = sha256_file(backup_path)
        sha_path.write_text(f"{digest}  {backup_path}\n", encoding="utf-8")
        os.chmod(sha_path, 0o640)

        metadata = {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "root": str(root),
            "config_file": str(env_path),
            "database": db_name,
            "host": db_host,
            "user": db_user,
            "output": str(backup_path),
            "sha256": digest,
            "size_bytes": validation["size_bytes"],
            "has_create_table": validation["has_create_table"],
            "has_insert_into": validation["has_insert_into"],
            "dump_binary": dump_binary,
            "label": args.label,
        }

        meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        os.chmod(meta_path, 0o640)

        print("Backup completo generado correctamente.")
        print(f"Base de datos: {db_name}")
        print(f"Host: {db_host}")
        print(f"Archivo: {backup_path}")
        print(f"SHA256: {digest}")
        print(f"SHA256 file: {sha_path}")
        print(f"Metadata: {meta_path}")
        print(f"Tamaño bytes: {validation['size_bytes']}")
        print(f"CREATE TABLE: {validation['has_create_table']}")
        print(f"INSERT INTO: {validation['has_insert_into']}")

    finally:
        try:
            tmp_config.unlink(missing_ok=True)
        except Exception:
            pass


if __name__ == "__main__":
    main()
