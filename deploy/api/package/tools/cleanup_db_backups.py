#!/usr/bin/env python3
import argparse
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


def parse_keep(value: str, default: int = 10) -> int:
    try:
        keep = int(str(value).strip())
        if keep < 1:
            return default
        return keep
    except Exception:
        return default


def find_backup_sets(backup_dir: Path):
    backups = []

    for sql_file in backup_dir.glob("*.sql"):
        sha_file = Path(str(sql_file) + ".sha256")
        meta_file = Path(str(sql_file) + ".meta.json")

        backups.append({
            "sql": sql_file,
            "sha": sha_file,
            "meta": meta_file,
            "mtime": sql_file.stat().st_mtime,
            "size": sql_file.stat().st_size,
        })

    backups.sort(key=lambda item: item["mtime"], reverse=True)
    return backups


def fmt_time(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def main():
    parser = argparse.ArgumentParser(description="Aplica política de retención sobre backups completos DASC.")
    parser.add_argument("--root", default="/opt/dasc/api", help="Ruta raíz de instalación API.")
    parser.add_argument("--backup-dir", default="", help="Directorio de backups. Si se omite usa BACKUP_OUTPUT_DIR.")
    parser.add_argument("--keep", default="", help="Número de backups completos a conservar.")
    parser.add_argument("--apply", action="store_true", help="Aplica borrado real. Sin esto solo muestra lo que haría.")
    parser.add_argument("--include-orphans", action="store_true", help="Muestra ficheros .sha256/.meta.json sin .sql asociado.")

    args = parser.parse_args()

    root = Path(args.root).resolve()
    env = load_env_file(root / "config.env")

    backup_dir = Path(args.backup_dir or env.get("BACKUP_OUTPUT_DIR", "/var/backups/dasc/mysql/full")).resolve()
    keep = parse_keep(args.keep or env.get("BACKUP_RETENTION_KEEP", "10"), default=10)

    print("Política de retención de backups DASC")
    print(f"Root: {root}")
    print(f"Directorio: {backup_dir}")
    print(f"Conservar últimos: {keep}")
    print(f"Modo: {'APLICAR' if args.apply else 'DRY-RUN'}")
    print("")

    if not backup_dir.exists():
        print("ERROR: no existe el directorio de backups.")
        raise SystemExit(1)

    backups = find_backup_sets(backup_dir)

    print(f"Backups .sql detectados: {len(backups)}")
    print("")

    if not backups:
        print("No hay backups que procesar.")
        return

    keep_items = backups[:keep]
    delete_items = backups[keep:]

    print("Backups conservados:")
    for item in keep_items:
        print(f"- KEEP   {item['sql']} | {item['size']} bytes | {fmt_time(item['mtime'])}")

    print("")

    if not delete_items:
        print("No hay backups antiguos para eliminar.")
    else:
        print("Backups candidatos a eliminación:")
        for item in delete_items:
            print(f"- DELETE {item['sql']} | {item['size']} bytes | {fmt_time(item['mtime'])}")

            for sidecar in [item["sha"], item["meta"]]:
                if sidecar.exists():
                    print(f"         asociado: {sidecar}")

        print("")

        if args.apply:
            deleted = 0

            for item in delete_items:
                for path in [item["sql"], item["sha"], item["meta"]]:
                    if path.exists():
                        path.unlink()
                        deleted += 1
                        print(f"Eliminado: {path}")

            print("")
            print(f"Total ficheros eliminados: {deleted}")
        else:
            print("DRY-RUN: no se ha eliminado nada. Usa --apply para aplicar la limpieza real.")

    if args.include_orphans:
        print("")
        print("Revisión de ficheros asociados huérfanos:")

        sql_paths = {str(item["sql"]) for item in backups}
        orphans = []

        for sidecar in list(backup_dir.glob("*.sql.sha256")) + list(backup_dir.glob("*.sql.meta.json")):
            base = str(sidecar)
            if base.endswith(".sha256"):
                expected_sql = base[:-7]
            elif base.endswith(".meta.json"):
                expected_sql = base[:-10]
            else:
                expected_sql = ""

            if expected_sql and expected_sql not in sql_paths:
                orphans.append(sidecar)

        if not orphans:
            print("No se han detectado huérfanos.")
        else:
            for orphan in orphans:
                print(f"- ORPHAN {orphan}")

    print("")
    print("Resultado: OK")


if __name__ == "__main__":
    main()
