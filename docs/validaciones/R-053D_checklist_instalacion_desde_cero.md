# R-053D — Checklist reproducible de instalación desde cero (por perfil)

> **Objetivo (R-053).** Instalar Vigex en una **VM limpia** partiendo del repo/tag,
> **sin pasos manuales ocultos**, y dejar evidencia consolidada por perfil.
> Este documento es el guion ejecutable y el informe consolidado de resultados.
>
> Estado: ✅ **CERRADO 2026-06-14** · Los 3 perfiles validados:
> **Lite ✅ (R-053A) · Standard ✅ (R-053B) · Pro ✅ (R-053C)**

---

## 0. Hallazgos del barrido estático (previo a la VM)

Trazada la secuencia real de instaladores para Lite leyendo el código. Conclusiones
que el checklist debe respetar (y que R-053 deja documentadas para que no sean
"pasos ocultos"):

| # | Hallazgo | Severidad | Acción en el checklist |
|---|---|---|---|
| F1 | **No hay orquestador único** para Lite: hay que correr 3 instaladores en una sola VM, en orden. | Media | El orden se fija abajo: **db → backup-services → api**. |
| F2 | `install_vigex_api.sh` solo configura el SSH a sí mismo (127.0.0.1) si **ya existen `sshd` + usuario `vigex`**. Si se corre primero, salta el paso (no bloqueante) y los backups no funcionan. | Media | Por eso `db` y `backup-services` van **antes** que `api`. |
| F3 | La contraseña del usuario `vigex` se fija **por separado** en `install_db.sh` y en `install_backup_services.sh`. En Lite (misma VM) **deben coincidir**. | Media | Pasar `APP_PASSWORD` por entorno a ambos, o teclear la misma. |
| F4 | `install_db.sh` **no** auto-rellena `BACKUP_ALLOWED_HOST`/`LOGS_ALLOWED_HOST` a `127.0.0.1` en perfil lite: los **pregunta**. | Baja | En Lite responder `127.0.0.1` (o pasarlos por entorno). |
| F5 | La **copia externa es obligatoria** en Lite (`EXTERNAL_BACKUP_REQUIRED=yes`) pero el instalador la deja **deshabilitada** (`ENABLED=no`, `TYPE=none`). | Media | Habilitar y probar la copia externa en R-053A. |
| F6 | **Mojibake** en mensajes de `install_vigex_api.sh` y `install_backup_services.sh` (p. ej. `ejecuciÃ³n`). Cosmético pero visible al cliente durante la instalación. | Baja | Anotado para limpieza; no bloquea R-053A. |
| F7 | `install_backup_services.sh` línea ~169: `is_empty_or_placeholder "$DB_NAME" && DB_NAME="$DB_NAME"` es un no-op (se asigna a sí mismo). | Baja | Anotado; inofensivo. |

### Hallazgos adicionales — R-053B Standard (2026-06-07)

| ID | Hallazgo | Severidad | Acción |
|---|---|---|---|
| **B4** | `install_backup_services.sh` abortaba por `mysqlbinlog` ausente en el host de backup Standard/Pro (no tiene `mariadb-server` local). | 🟠 Bloqueante en Standard/Pro | Eliminado de `required_cmd`; convertido en AVISO. **Fix aplicado.** |
| **B5** | `install_vigex_api.sh` terminaba silenciosamente en el segundo host SSH: `unset VIGEX_PASS` dentro del bucle borraba la contraseña; `read` desde `stdin=/dev/null` devuelve exit 1, que `set -euo pipefail` convierte en salida silenciosa. | 🔴 Bloqueante en Standard/Pro | `unset VIGEX_PASS` movido fuera del bucle. **Fix aplicado.** |

> Los instaladores se gobiernan por `VIGEX_PROFILE` + variables de entorno +
> el fichero de handoff de secretos DB (`/root/vigex-db-install-secrets.env`).
> Las plantillas de `config/perfiles/` son una vista de referencia; el instalador
> no las lee directamente.

---

## 1. Pre-flight (en la máquina Windows, antes de la VM)

- [ ] `.\tools\windows\check_api_package_installable.ps1` → 50/50 OK.
- [ ] `.\tools\windows\check_repo_clean.ps1` → sin secretos ni `config.env` real.
- [ ] Tag/commit de partida anotado: `__________`.

## 2. Preparar la VM limpia (multipass)

```powershell
# lanzar VM Ubuntu 22.04 limpia
multipass launch 22.04 --name vigex-lite --cpus 2 --memory 4G --disk 20G

# llevar el repo a la VM partiendo del commit actual
git archive --format=tar.gz -o vigex-src.tgz HEAD
multipass transfer vigex-src.tgz vigex-lite:/home/ubuntu/vigex-src.tgz
multipass exec vigex-lite -- bash -lc "mkdir -p ~/vigex && tar xzf ~/vigex-src.tgz -C ~/vigex"
multipass shell vigex-lite
```

- [ ] VM `vigex-lite` arrancada y limpia (Ubuntu 22.04).
- [ ] Repo extraído en `~/vigex` dentro de la VM.

---

## 3. Instalación Lite — orden obligatorio (dentro de la VM)

> Exportar el perfil y una contraseña común de `vigex` para evitar incoherencias (F3):
> ```bash
> export VIGEX_PROFILE=lite
> export APP_PASSWORD='<password-vigex>'
> ```

### 3.1 Base de datos (MariaDB + SSH + usuario vigex)

```bash
cd ~/vigex/deploy/db
sudo -E VIGEX_PROFILE=lite APP_PASSWORD="$APP_PASSWORD" \
    BACKUP_ALLOWED_HOST=127.0.0.1 LOGS_ALLOWED_HOST=127.0.0.1 \
    bash install_db.sh
```

- [ ] MariaDB activo (`:3306`), `ssh` activo (`:22`), usuario `vigex` creado.
- [ ] Secretos exportados en `/root/vigex-db-install-secrets.env`.

### 3.2 Backups + servicios (scripts en /usr/local/bin, .my.cnf, sudoers)

```bash
cd ~/vigex/deploy/backup-services
sudo -E VIGEX_PROFILE=lite APP_PASSWORD="$APP_PASSWORD" bash install_backup_services.sh
```

- [ ] Scripts `backups_api.sh`, `restore_api.sh`, `servicios_api.sh` en `/usr/local/bin`.
- [ ] `~vigex/.my.cnf` y `.my_restore.cnf` (600) → prueba `mysql`/`mysqldump` OK.
- [ ] AVISO `mysqlbinlog no disponible` esperado (B4) — no bloqueante. ✅

### 3.3 Panel + API (FastAPI/Uvicorn :8000 + clave SSH al propio host)

```bash
cd ~/vigex/deploy/api
sudo -E VIGEX_PROFILE=lite ADMIN_PASSWORD_INPUT='<password-admin-panel>' \
    VIGEX_PASS="$APP_PASSWORD" bash install_vigex_api.sh
```

- [ ] Servicio `vigex-api` activo; `curl -I http://127.0.0.1:8000` responde HTTP 200.
- [ ] Clave de la API autorizada en `vigex@127.0.0.1` (paso SSH **no** saltado).

### 3.4 Copia externa obligatoria (F5)

- [ ] Configurar destino externo (en VM: `/mnt/vigex-external` montado) y
      `EXTERNAL_BACKUP_ENABLED=yes` + `EXTERNAL_BACKUP_TYPE` en `config.env`.
- [ ] Ejecutar `sync_external_backup.sh` → exit 0, copia verificada en el destino.

### 3.5 (Opcional en R-053A) Proxy HTTPS

> HTTPS real/certbot es `R-054`. En R-053A basta validar el panel por HTTP en `:8000`.

## 4. Verificación funcional (smoke)

- [ ] Login en el panel con el admin (hash bcrypt, no texto plano).
- [ ] Lanzar un **backup** desde el panel → aparece en historial y en disco.
- [ ] Lanzar una **restauración** controlada (o `restore_drill_api.sh`).
- [ ] Ver **logs** (DB `vigex_logs`) y una **alerta** de prueba.
- [ ] Acción de **servicio** (start/stop/status) vía panel (sudoers sin password).
- [ ] Reinicio de la VM → `vigex-api`, `mariadb`, `ssh`, `cron` levantan solos.

## 5. Idempotencia / re-instalación

- [ ] Re-ejecutar los 3 instaladores no rompe nada (`config.env`, venv, `SECRET_KEY`,
      `ADMIN_PASSWORD` y `known_hosts` se conservan/regeneran sin duplicar).

---

## 6. Instalación Standard — orden obligatorio (2 VMs)

> **VMs requeridas:** `vigex-std-db` (MariaDB) + `vigex-std-api` (Panel + backup-services).

```powershell
multipass launch 22.04 --name vigex-std-db  --cpus 2 --memory 4G --disk 20G
multipass launch 22.04 --name vigex-std-api --cpus 2 --memory 4G --disk 20G
```

Transferir el repo a cada una (igual que sección 2).

### 6.1 En vigex-std-db — Base de datos

```bash
export DB_HOST_IP=$(multipass info vigex-std-db  | grep IPv4 | awk '{print $2}')
export API_HOST_IP=$(multipass info vigex-std-api | grep IPv4 | awk '{print $2}')

cd ~/vigex/deploy/db
sudo -E VIGEX_PROFILE=standard APP_PASSWORD=<pass-vigex-db> \
    BACKUP_ALLOWED_HOST="$API_HOST_IP" LOGS_ALLOWED_HOST="$API_HOST_IP" \
    bash install_db.sh
```

- [ ] MariaDB activo, usuario `vigex` creado, secretos en `/root/vigex-db-install-secrets.env`.

### 6.2 En vigex-std-api — Backup-services

```bash
cd ~/vigex/deploy/backup-services
sudo -E VIGEX_PROFILE=standard APP_PASSWORD=<pass-vigex-api> \
    DB_HOST="$DB_HOST_IP" DB_PORT=3306 \
    DB_BACKUP_USER=vigex_backup DB_BACKUP_PASS=<pass-backup> \
    DB_RESTORE_USER=vigex_restore DB_RESTORE_PASS=<pass-restore> \
    DB_NAME=vigex_app LOGS_DB_NAME=vigex_logs \
    LOGS_DB_USER=vigex_logs LOGS_DB_PASS=<pass-logs> \
    bash install_backup_services.sh
```

- [ ] Scripts `backups_api.sh`, `restore_api.sh`, `servicios_api.sh` en `/usr/local/bin`.
- [ ] `.my.cnf` del usuario `vigex` apunta a `host=<IP_vigex-std-db>`.
- [ ] AVISO `mysqlbinlog no disponible` esperado (B4). ✅

### 6.3 En vigex-std-api — Panel API

```bash
cd ~/vigex/deploy/api
sudo -E VIGEX_PROFILE=standard \
    BACKUPS_HOST=127.0.0.1 SERVICIOS_HOST=127.0.0.1 \
    LOGS_DB_HOST="$DB_HOST_IP" TERMINAL_DATABASE_HOST="$DB_HOST_IP" \
    LOGS_DB_NAME=vigex_logs LOGS_DB_USER=vigex_logs LOGS_DB_PASS=<pass-logs> \
    ADMIN_USERNAME=admin ADMIN_PASSWORD_INPUT=<pass-admin> \
    VIGEX_PASS=<pass-vigex-api> \
    bash install_vigex_api.sh </dev/null
```

- [ ] `vigex-api` activo; `curl -I http://127.0.0.1:8000` responde HTTP 200.
- [ ] SSH sin contraseña `vigex@vigex-std-api → vigex@vigex-std-db` verificado.
- [ ] `VIGEX_SSH_ALLOWED_HOSTS` incluye `127.0.0.1,localhost,<IP_vigex-std-db>`.

> **Nota:** `VIGEX_PASS` debe coincidir con el password del usuario `vigex` en el host
> destino. Redirigir `stdin` (`</dev/null`) es necesario para ejecución no interactiva (B5).

---

## 7. Instalación Pro — orden obligatorio (3 VMs)

> **VMs requeridas:** `vigex-pro-db` (MariaDB) + `vigex-pro-backup` (backup-services)
> + `vigex-pro-api` (Panel).

```powershell
multipass launch 22.04 --name vigex-pro-db     --cpus 2 --memory 4G --disk 20G
multipass launch 22.04 --name vigex-pro-backup --cpus 2 --memory 4G --disk 20G
multipass launch 22.04 --name vigex-pro-api    --cpus 2 --memory 4G --disk 20G
```

Transferir el repo a cada una (igual que sección 2).

### 7.1 En vigex-pro-db — Base de datos

```bash
export DB_HOST_IP=$(multipass info vigex-pro-db     | grep IPv4 | awk '{print $2}')
export BK_HOST_IP=$(multipass info vigex-pro-backup | grep IPv4 | awk '{print $2}')

cd ~/vigex/deploy/db
sudo -E VIGEX_PROFILE=pro APP_PASSWORD=<pass-vigex-db> \
    BACKUP_ALLOWED_HOST="$BK_HOST_IP" LOGS_ALLOWED_HOST="$BK_HOST_IP" \
    bash install_db.sh
```

- [ ] MariaDB activo, usuario `vigex` creado, secretos en `/root/vigex-db-install-secrets.env`.

### 7.2 En vigex-pro-backup — Backup-services

```bash
cd ~/vigex/deploy/backup-services
sudo -E VIGEX_PROFILE=pro APP_PASSWORD=<pass-vigex-backup> \
    DB_HOST="$DB_HOST_IP" DB_PORT=3306 \
    DB_BACKUP_USER=vigex_backup DB_BACKUP_PASS=<pass-backup> \
    DB_RESTORE_USER=vigex_restore DB_RESTORE_PASS=<pass-restore> \
    DB_NAME=vigex_app LOGS_DB_NAME=vigex_logs \
    LOGS_DB_USER=vigex_logs LOGS_DB_PASS=<pass-logs> \
    bash install_backup_services.sh
```

- [ ] Scripts en `/usr/local/bin`. `.my.cnf` apunta a `host=<IP_vigex-pro-db>`.
- [ ] AVISO `mysqlbinlog no disponible` esperado (B4). ✅

### 7.3 En vigex-pro-api — Panel API

```bash
export API_HOST_IP=$(multipass info vigex-pro-api | grep IPv4 | awk '{print $2}')

cd ~/vigex/deploy/api
sudo -E VIGEX_PROFILE=pro \
    BACKUPS_HOST="$BK_HOST_IP" SERVICIOS_HOST="$BK_HOST_IP" \
    LOGS_DB_HOST="$DB_HOST_IP" TERMINAL_DATABASE_HOST="$DB_HOST_IP" \
    LOGS_DB_NAME=vigex_logs LOGS_DB_USER=vigex_logs LOGS_DB_PASS=<pass-logs> \
    ADMIN_USERNAME=admin ADMIN_PASSWORD_INPUT=<pass-admin> \
    VIGEX_PASS=<pass-vigex-backup> \
    bash install_vigex_api.sh </dev/null
```

- [ ] `vigex-api` activo; `curl -I http://127.0.0.1:8000` responde HTTP 200.
- [ ] SSH sin contraseña a 2 hosts remotos (`vigex-pro-db` y `vigex-pro-backup`) verificado.
- [ ] `VIGEX_SSH_ALLOWED_HOSTS` incluye las IPs de los 3 hosts.

> **Nota Pro:** `VIGEX_PASS` es la contraseña del usuario `vigex` en el **host de backup**
> (que es el primer host SSH que el instalador configura). Pasarlo por entorno (B5).

---

## Informe consolidado por perfil

| Perfil | Commit | VMs (SO / recursos) | Resultado | Incidencias | Evidencia |
|---|---|---|---|---|---|
| Lite (R-053A) | `9317e57` | Ubuntu 22.04, 1 VM, 2 vCPU / 4 GiB | ✅ Cerrado 2026-06-07 | B1, B2, F8, B3 | [`R-053A`](R-053A_validacion_lite.md) |
| Standard (R-053B) | `092e37d` | Ubuntu 22.04, 2 VMs, 2 vCPU / 4 GiB c/u | ✅ Cerrado 2026-06-07 | B4, B5 | [`R-053B`](R-053B_validacion_standard.md) |
| Pro (R-053C) | `ca049d1` | Ubuntu 22.04, 3 VMs (2 + 4 + 4 GiB) | ✅ Cerrado 2026-06-07 | ninguno nuevo | [`R-053C`](R-053C_validacion_pro.md) |

**Criterio de cierre R-053:** los 3 perfiles instalan desde cero sin pasos manuales
no documentados, con panel operativo y backup + restauración verificados.
