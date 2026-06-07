# R-053B — Validación de instalación desde cero · Perfil Standard (2 VMs)

> **Resultado:** ✅ La instalación Standard desde cero en 2 VMs limpias **funciona** y
> queda operativa. R-053B **CERRADO** (2026-06-07).
>
> Relacionado: [`R-053A_validacion_lite.md`](R-053A_validacion_lite.md) ·
> [`R-053D_checklist_instalacion_desde_cero.md`](R-053D_checklist_instalacion_desde_cero.md).

## 1. Entorno de validación

- **Herramienta:** multipass 1.16.3 (Hyper-V) sobre Windows 11.
- **VMs:**

  | VM | IP | Rol | Recursos |
  |---|---|---|---|
  | `dasc-std-db` | 172.19.222.6 | MariaDB / BD de logs | 2 vCPU / 4 GiB / 20 GiB |
  | `dasc-std-api` | 172.19.211.191 | Panel API + backup-services | 2 vCPU / 4 GiB / 20 GiB |

- **Imágenes:** Ubuntu 22.04 LTS cloud (mismas que R-053A).
- **Rama:** `docs/roadmap-canonico`.
- **Orden de instalación:** `install_db.sh` (dasc-std-db) → `install_backup_services.sh`
  (dasc-std-api) → `install_dasc_api.sh` (dasc-std-api).
- **Método:** no interactivo (variables por entorno en scripts driver).

## 2. Defectos encontrados y corregidos

| ID | Severidad | Defecto | Causa raíz | Fix |
|---|---|---|---|---|
| **B4** | 🟠 Funcional | `install_backup_services.sh` abortaba por `mysqlbinlog` ausente en el host de backup | En Ubuntu 22.04, `mysqlbinlog`/`mariadb-binlog` solo existe en `mariadb-server-10.6`; el host de backup Standard/Pro no tiene servidor local | Eliminado de la lista de comandos requeridos; convertido en AVISO no bloqueante. Los scripts de runtime usan `mysqldump`, no `mysqlbinlog` |
| **B5** | 🔴 Bloqueante | `install_dasc_api.sh` salía silenciosamente al configurar SSH en el segundo host | `unset DASC_PASS` dentro del bucle borraba la contraseña antes de la segunda iteración; `read` desde `stdin=/dev/null` devuelve exit 1, que `set -euo pipefail` convierte en salida sin mensaje de error | `unset DASC_PASS` movido fuera del bucle (justo después de `done`) |

**Ficheros modificados:**
`deploy/backup-services/install_backup_services.sh` (B4) ·
`deploy/api/install_dasc_api.sh` (B5).

> **Nota sobre B5:** el bug afecta a cualquier perfil con ≥ 2 hosts SSH distintos
> (Standard y Pro). En Lite/single todo va a `127.0.0.1` por lo que el bucle
> solo itera una vez y el bug no se manifiesta.

## 3. Verificación funcional (2 VMs tras instalar)

| Check | Resultado |
|---|---|
| Instalación completa (3 instaladores, 2 VMs) | ✅ `Instalación completada`, sin fallos |
| `config.env` final — perfil | ✅ `DASC_PROFILE=standard` |
| `config.env` — hosts sin placeholders | ✅ `BACKUPS_HOST=127.0.0.1`, `SERVICIOS_HOST=127.0.0.1`, `LOGS_DB_HOST=172.19.222.6`, `TERMINAL_DATABASE_HOST=172.19.222.6` |
| `DASC_SSH_ALLOWED_HOSTS` | ✅ `127.0.0.1,localhost,172.19.222.6` |
| SSH sin contraseña panel→DB (`dasc@172.19.222.6`) | ✅ `hostname=dasc-std-db`, `uid=1001(dasc)`, exit 0 |
| Conectividad BD de logs (172.19.222.6) | ✅ `SHOW TABLES → eventos` con credenciales del panel |
| Backup real vía red | ✅ `mysqldump employees` desde dasc-std-api a 172.19.222.6 → `std_test_backup.sql.gz` (861 B) |
| Panel HTTP | ✅ `GET / → 303`, `GET /login → 200` |
| Servicios systemd — dasc-std-api | ✅ `dasc-api`, `ssh`, `cron` activos |
| Servicios systemd — dasc-std-db | ✅ `mariadb`, `ssh` activos |
| Scripts backup-services instalados | ✅ `backups_api.sh`, `restore_api.sh`, `servicios_api.sh` en `/usr/local/bin/` |

## 4. Observaciones adicionales

- **`BACKUP_DB_HOST` / `RESTORE_DB_HOST` en `config.env`** — aparecen como
  `IP_SERVIDOR_DB` (placeholder del ejemplo) pero **ningún código los referencia**:
  `main.py`, `backups_api.sh` y `restore_api.sh` usan la clave `host=` del
  `.my.cnf` de dasc. No es un defecto funcional, sino claves residuales del
  ejemplo que deberán limpiarse en una tarea de deuda técnica.
- **Compatibilidad B3** — el fix del drop-in `00-dasc-ssh.conf`
  (`PasswordAuthentication yes`) sigue siendo necesario en imágenes cloud
  de Ubuntu 22.04 para ambas VMs.

## 5. Conclusión

El perfil **Standard instala desde cero en 2 VMs limpias y queda completamente
operativo**, una vez aplicados B4 y B5. El defecto B5 es específico de perfiles
multi-host y no habría sido detectado sin la validación real en VMs separadas.
