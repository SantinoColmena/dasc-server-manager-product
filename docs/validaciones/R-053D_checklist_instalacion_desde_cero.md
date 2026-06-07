# R-053D — Checklist reproducible de instalación desde cero (por perfil)

> **Objetivo (R-053).** Instalar DASC en una **VM limpia** partiendo del repo/tag,
> **sin pasos manuales ocultos**, y dejar evidencia consolidada por perfil.
> Este documento es el guion que se ejecuta y la plantilla de informe.
>
> Estado: ✅ **CERRADO 2026-06-07** · Los 3 perfiles validados: **Lite ✅ (R-053A) · Standard ✅ (R-053B) · Pro ✅ (R-053C)**.

---

## 0. Hallazgos del barrido estático (previo a la VM)

Trazada la secuencia real de instaladores para Lite leyendo el código. Conclusiones
que el checklist debe respetar (y que R-053 debe dejar documentadas para que no
sean "pasos ocultos"):

| # | Hallazgo | Severidad | Acción en el checklist |
|---|---|---|---|
| F1 | **No hay orquestador único** para Lite: hay que correr 3 instaladores en una sola VM, en orden. | Media | El orden se fija abajo: **db → backup-services → api**. |
| F2 | `install_dasc_api.sh` solo configura el SSH a sí mismo (127.0.0.1) si **ya existen `sshd` + usuario `dasc`**. Si se corre primero, salta el paso (no bloqueante) y los backups no funcionan. | Media | Por eso `db` y `backup-services` van **antes** que `api`. |
| F3 | La contraseña del usuario `dasc` se fija **por separado** en `install_db.sh` y en `install_backup_services.sh`. En Lite (misma VM) **deben coincidir**. | Media | Pasar `APP_PASSWORD` por entorno a ambos, o teclear la misma. |
| F4 | `install_db.sh` **no** auto-rellena `BACKUP_ALLOWED_HOST`/`LOGS_ALLOWED_HOST` a `127.0.0.1` en perfil lite: los **pregunta**. | Baja | En Lite responder `127.0.0.1` (o pasarlos por entorno). |
| F5 | La **copia externa es obligatoria** en Lite (`EXTERNAL_BACKUP_REQUIRED=yes`) pero el instalador la deja **deshabilitada** (`ENABLED=no`, `TYPE=none`). | Media | R-053A debe validar habilitar y probar la copia externa. |
| F6 | **Mojibake** en mensajes de `install_dasc_api.sh` y `install_backup_services.sh` (p. ej. `ejecuciÃ³n`, `contraseÃ±a`). Cosmético pero visible al cliente durante la instalación. | Baja | Anotado para limpieza (no bloquea R-053A). |
| F7 | `install_backup_services.sh` línea ~169: `is_empty_or_placeholder "$DB_NAME" && DB_NAME="$DB_NAME"` es un no-op (se asigna a sí mismo). | Baja | Anotado; inofensivo. |

### Hallazgos adicionales — R-053B Standard (2026-06-07)

| ID | Hallazgo | Severidad | Acción |
|---|---|---|---|
| **B4** | `install_backup_services.sh` abortaba por `mysqlbinlog` ausente en el host de backup Standard/Pro (no tiene `mariadb-server-10.6` local) | 🟠 Bloqueante en Standard/Pro | Eliminado de la lista `required_cmd`; convertido en AVISO. **Fix aplicado.** |
| **B5** | `install_dasc_api.sh` terminaba silenciosamente en el segundo host SSH: `unset DASC_PASS` dentro del bucle borraba la contraseña; `read` desde `stdin=/dev/null` devuelve exit 1, que `set -euo pipefail` convierte en salida silenciosa | 🔴 Bloqueante en Standard/Pro | `unset DASC_PASS` movido fuera del bucle. **Fix aplicado.** |

> Las plantillas de `config/perfiles/` y `scripts/generar_config_perfil.sh` generan
> un `config.env` de referencia, pero **los instaladores se gobiernan por
> `DASC_PROFILE` + variables de entorno + el fichero de handoff de secretos DB**
> (`/root/dasc-db-install-secrets.env`). Conviene aclararlo en docs (R-056).

---

## 1. Pre-flight (en la máquina Windows, antes de la VM)

- [ ] `./tools/windows/check_api_package_installable.ps1` → en verde (paquete API instalable).
- [ ] `./tools/windows/check_repo_clean.ps1` → sin secretos ni `config.env` real.
- [ ] Tag/commit de partida anotado: `__________` (la validación parte de aquí).

## 2. Preparar la VM limpia (multipass)

```powershell
# (una vez) instalar multipass en Windows
winget install Canonical.Multipass

# lanzar VM Ubuntu 22.04 limpia
multipass launch 22.04 --name dasc-lite --cpus 2 --memory 4G --disk 20G

# llevar el repo a la VM partiendo del tag/commit (sin arrastrar permisos de Windows)
git archive --format=tar.gz -o dasc-src.tgz HEAD
multipass transfer dasc-src.tgz dasc-lite:/home/ubuntu/dasc-src.tgz
multipass exec dasc-lite -- bash -lc "mkdir -p ~/dasc && tar xzf ~/dasc-src.tgz -C ~/dasc"
multipass shell dasc-lite   # entrar a la VM
```

- [ ] VM `dasc-lite` arrancada y limpia (Ubuntu 22.04).
- [ ] Repo extraído en `~/dasc` dentro de la VM.

## 3. Instalación Lite — orden obligatorio (dentro de la VM)

> Exportar el perfil y una contraseña común de `dasc` para evitar incoherencias (F3):
> ```bash
> export DASC_PROFILE=lite
> export APP_PASSWORD='<password-dasc>'
> ```

### 3.1 Base de datos (MariaDB + SSH + usuario dasc)
```bash
cd ~/dasc/deploy/db
sudo -E DASC_PROFILE=lite APP_PASSWORD="$APP_PASSWORD" \
    BACKUP_ALLOWED_HOST=127.0.0.1 LOGS_ALLOWED_HOST=127.0.0.1 \
    ./install_db.sh
```
- [ ] MariaDB activo (`:3306`), `ssh` activo (`:22`), usuario `dasc` creado.
- [ ] Secretos exportados en `/root/dasc-db-install-secrets.env`.

### 3.2 Backups + servicios (scripts en /usr/local/bin, .my.cnf, sudoers)
```bash
cd ~/dasc/deploy/backup-services
sudo -E DASC_PROFILE=lite APP_PASSWORD="$APP_PASSWORD" ./install_backup_services.sh
```
- [ ] Scripts `backups_api.sh`, `restore_api.sh`, `servicios_api.sh` en `/usr/local/bin`.
- [ ] `~dasc/.my.cnf` y `.my_restore.cnf` (600) → prueba `mysql`/`mysqldump` OK.

### 3.3 Panel + API (FastAPI/Uvicorn :8000 + clave SSH al propio host)
```bash
cd ~/dasc/deploy/api
sudo -E DASC_PROFILE=lite ADMIN_PASSWORD_INPUT='<password-admin-panel>' \
    DASC_PASS="$APP_PASSWORD" ./install_dasc_api.sh
```
- [ ] Servicio `dasc-api` activo; `curl -I http://127.0.0.1:8000` responde.
- [ ] Clave de la API autorizada en `dasc@127.0.0.1` (paso SSH **no** saltado).

### 3.4 Copia externa obligatoria (F5)
- [ ] Configurar destino externo (mínimo en VM: `/mnt/dasc-external` montado) y
      `EXTERNAL_BACKUP_ENABLED=yes` + `EXTERNAL_BACKUP_TYPE` adecuado en `config.env`.
- [ ] Ejecutar `sync_external_backup.sh` y verificar copia en el destino.

### 3.5 (Opcional en R-053A) Proxy HTTPS
> HTTPS real/certbot es **R-054**. En R-053A basta validar el panel por HTTP en `:8000`.

## 4. Verificación funcional (humo)

- [ ] Login en el panel con el admin (hash bcrypt, no texto plano).
- [ ] Lanzar un **backup** desde el panel → aparece en historial y en disco.
- [ ] Lanzar una **restauración** controlada (o `restore_drill_api.sh`).
- [ ] Ver **logs** (DB `dasc_logs`) y una **alerta** de prueba.
- [ ] Acción de **servicio** (start/stop/status) vía panel (sudoers sin password).
- [ ] Reinicio de la VM → `dasc-api`, `mariadb`, `ssh`, `cron` levantan solos.

## 5. Idempotencia / re-instalación
- [ ] Re-ejecutar los 3 instaladores no rompe nada (config.env, venv, SECRET_KEY,
      ADMIN_PASSWORD y known_hosts se conservan/regeneran sin duplicar).

---

## 6. Instalación Standard — orden obligatorio (2 VMs)

> **VMs requeridas:** `dasc-std-db` (MariaDB) + `dasc-std-api` (Panel + backup-services).
> Preparar ambas con `multipass launch 22.04 --name <nombre> --cpus 2 --memory 4G --disk 20G`
> y transferir el repo a cada una.

### 6.1 En dasc-std-db — Base de datos

```bash
export DB_HOST_IP=<IP_dasc-std-db>   # p. ej. 172.19.222.6
export API_HOST_IP=<IP_dasc-std-api>  # p. ej. 172.19.211.191
# En dasc-std-db:
cd ~/dasc/deploy/db
sudo -E DASC_PROFILE=standard APP_PASSWORD=<pass-dasc-db> \
    BACKUP_ALLOWED_HOST="$API_HOST_IP" LOGS_ALLOWED_HOST="$API_HOST_IP" \
    bash install_db.sh
```
- [ ] MariaDB activo, usuario `dasc` creado, secretos en `/root/dasc-db-install-secrets.env`.

### 6.2 En dasc-std-api — Backup-services

```bash
# En dasc-std-api (leer secretos de dasc-std-db previamente copiados):
cd ~/dasc/deploy/backup-services
sudo -E DASC_PROFILE=standard APP_PASSWORD=<pass-dasc-api> \
    DB_HOST=<IP_dasc-std-db> DB_PORT=3306 \
    DB_BACKUP_USER=dasc_backup DB_BACKUP_PASS=<pass-backup> \
    DB_RESTORE_USER=dasc_restore DB_RESTORE_PASS=<pass-restore> \
    DB_NAME=employees LOGS_DB_NAME=dasc_logs \
    LOGS_DB_USER=dasc_logs LOGS_DB_PASS=<pass-logs> \
    bash install_backup_services.sh
```
- [ ] Scripts `backups_api.sh`, `restore_api.sh`, `servicios_api.sh` en `/usr/local/bin`.
- [ ] `.my.cnf` de dasc apunta a `host=<IP_dasc-std-db>`.
- [ ] AVISO: `mysqlbinlog no disponible` esperado en Standard/Pro (B4). ✅

### 6.3 En dasc-std-api — Panel API

```bash
cd ~/dasc/deploy/api
sudo -E DASC_PROFILE=standard \
    BACKUPS_HOST=127.0.0.1 SERVICIOS_HOST=127.0.0.1 \
    LOGS_DB_HOST=<IP_dasc-std-db> TERMINAL_DATABASE_HOST=<IP_dasc-std-db> \
    LOGS_DB_NAME=dasc_logs LOGS_DB_USER=dasc_logs LOGS_DB_PASS=<pass-logs> \
    ADMIN_USERNAME=admin ADMIN_PASSWORD_INPUT=<pass-admin> \
    DASC_PASS=<pass-dasc-api> \
    bash install_dasc_api.sh </dev/null
```
- [ ] `dasc-api` activo; `curl -I http://127.0.0.1:8000` responde HTTP 200 en `/login`.
- [ ] SSH sin contraseña `ubuntu@dasc-std-api → dasc@dasc-std-db` verificado.
- [ ] `DASC_SSH_ALLOWED_HOSTS` incluye `127.0.0.1,localhost,<IP_dasc-std-db>`.

> **Nota:** `DASC_PASS` debe coincidir con el password del usuario `dasc` en el host destino.
> `exec 0</dev/null` (o redirigir `stdin`) es necesario para ejecución no interactiva (B5).

---

## Informe consolidado por perfil

| Perfil | Commit | VMs (SO/recursos) | Resultado | Incidencias | Evidencia |
|---|---|---|---|---|---|
| Lite (R-053A) | `9317e57` | Ubuntu 22.04, 1 VM, 2 vCPU/4 GiB | ✅ Cerrado 2026-06-07 | B1, B2, F8, B3 | [`R-053A`](R-053A_validacion_lite.md) |
| Standard (R-053B) | `092e37d` | Ubuntu 22.04, 2 VMs, 2 vCPU/4 GiB c/u | ✅ Cerrado 2026-06-07 | B4, B5 | [`R-053B`](R-053B_validacion_standard.md) |
| Pro (R-053C) | `ca049d1` | Ubuntu 22.04, 3 VMs (2+4+4 GiB) | ✅ Cerrado 2026-06-07 | ninguno nuevo | [`R-053C`](R-053C_validacion_pro.md) |

**Criterio de cierre R-053:** los 3 perfiles instalan desde cero sin pasos manuales
no documentados, con panel operativo y backup+restauración verificados.
