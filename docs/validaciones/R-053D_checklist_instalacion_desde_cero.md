# R-053D — Checklist reproducible de instalación desde cero (por perfil)

> **Objetivo (R-053).** Instalar DASC en una **VM limpia** partiendo del repo/tag,
> **sin pasos manuales ocultos**, y dejar evidencia consolidada por perfil.
> Este documento es el guion que se ejecuta y la plantilla de informe.
>
> Estado: 🔵 en curso · Perfil en validación: **Lite/single (R-053A)**.

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

## Informe consolidado por perfil (rellenar tras la corrida)

| Perfil | Tag/commit | VM (SO/recursos) | Resultado | Incidencias | Evidencia |
|---|---|---|---|---|---|
| Lite (R-053A) | | Ubuntu 22.04 | ⬜ | | |
| Standard (R-053B) | | | ⬜ | | |
| Pro (R-053C) | | | ⬜ | | |

**Criterio de cierre R-053:** los 3 perfiles instalan desde cero sin pasos manuales
no documentados, con panel operativo y backup+restauración verificados.
