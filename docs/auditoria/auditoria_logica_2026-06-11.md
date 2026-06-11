# Auditoría exhaustiva de lógica — 2026-06-11

> **Contexto.** Revisión profunda de toda la lógica del producto solicitada por el
> desarrollador tras un ciclo de desarrollo hecho mayoritariamente con un modelo
> menor. Objetivo: dejar el código "perfecto y limpio". Auditor: Opus 4.8.
> **Alcance:** `deploy/api/package/main.py` (~9.400 líneas),
> `deploy/central-support/package/main.py`, y los scripts bash de
> `deploy/backup-services/package/`.

## 1. Resumen ejecutivo

Se auditaron 8 áreas. El modelo de seguridad del producto (allowlist SSH +
`shlex.quote`, auth bcrypt, CSRF, permisos por módulo, SQL parametrizado, token
multi-cliente) es **sólido y consistente**. Se encontraron **3 defectos
accionables** —2 de severidad alta, 1 de robustez— **todos corregidos** en este
mismo commit. El resto del código quedó verificado sin hallazgos.

| # | Severidad | Área | Estado |
|---|---|---|---|
| FINDING-1 | 🔴 Alta (RCE autenticado) | Automatización de backups (heredoc) | ✅ Corregido |
| FINDING-2 | 🟠 Alta (disponibilidad) | Asistente IA R-090 (event loop) | ✅ Corregido |
| FINDING-3 | 🟡 Robustez | `backups_api.sh` (TSV) | ✅ Corregido |
| Extra | 🟢 Limpieza | `SyntaxWarning` escape `\w` | ✅ Corregido |

## 2. Hallazgos y correcciones

### FINDING-1 — Inyección por delimitador de heredoc (RCE en host de backups)
- **Dónde:** `crear_automatizacion_backup_remota()` + ruta `POST /backups/automation/create`.
- **Causa:** los campos de texto libre `notes` (y `db`/`dest`) se interpolan, vía
  `shlex.quote`, dentro de un heredoc con delimitador fijo
  (`<<'VIGEX_CRON_BLOCK'`). `shlex.quote` **preserva los saltos de línea
  literales**, de modo que un `notes` con `"\nVIGEX_CRON_BLOCK\n<comandos>"`
  cierra el heredoc antes de tiempo y ejecuta `<comandos>` como shell en el host
  de backups. Requiere usuario autenticado con permiso `backups`.
- **Impacto:** ejecución de comandos arbitrarios en el host de backups, eludiendo
  el allowlist de scripts SSH en el que se apoya el modelo de seguridad. Además,
  un salto de línea corrompía el crontab aunque no hubiera ataque.
- **Fix:** se rechaza cualquier carácter de control (`ord < 32`) en `db`, `dest`
  y `notes` en la ruta. Una entrada de cron es siempre de una sola línea, así que
  el rechazo es además correcto funcionalmente. *(Defensa en profundidad: ver
  FINDING-3 en el lado bash.)*

### FINDING-2 — Llamada bloqueante al LLM congela el event loop
- **Dónde:** `asistente_chat_api()` (`async`) → `_rag_generate()`.
- **Causa:** `_rag_generate` hace HTTP **bloqueante** (`urllib`, `timeout=300` con
  Ollama; SDK síncrono con Anthropic). Llamado directamente dentro de una ruta
  `async`, bloquea el event loop de Uvicorn. Con el despliegue documentado (un
  solo worker), **una sola consulta congela el panel entero para todos los
  usuarios** durante la inferencia (hasta 5 minutos con Ollama en CPU).
- **Impacto:** denegación de servicio trivial; el proveedor por defecto (Ollama
  local en CPU) es justamente el más lento.
- **Fix:** se delega la generación a un hilo con
  `await asyncio.to_thread(_rag_generate, ...)`, liberando el event loop.

### FINDING-3 — Corrupción de `history.tsv` por `echo -e` + entrada sin sanear
- **Dónde:** `backups_api.sh`, escritura de la fila de historial.
- **Causa:** la fila se escribía con `echo -e` y `${DB}`/`${NOTES}` sin sanear. Un
  salto de línea o tabulador en `notes` rompe el TSV (líneas/columnas falsas) y
  `echo -e` además interpreta secuencias con backslash.
- **Impacto:** principalmente robustez (rompe el listado y el parsing del
  historial). El impacto de seguridad es bajo porque `restore_api.sh` y el borrado
  en cascada validan checksum y contención de ruta antes de actuar.
- **Fix:** se neutralizan `\n`/`\r`/`\t` en `DB` y `NOTES` (mismo patrón que
  `audit_log`) y se escribe con `printf` en lugar de `echo -e`.

### Extra — `SyntaxWarning: invalid escape sequence '\w'`
- **Dónde:** cadena de ayuda con una ruta Windows `tools\windows\...` en `main.py`.
- **Fix:** backslashes escapados (`tools\\windows\\...`). Verificado con
  `python -W error::SyntaxWarning -m py_compile`.

## 3. Áreas verificadas sin hallazgos

- **Ejecución SSH:** `validate_ssh_run` (allowlist host+script), `ssh_run`
  (`shlex.quote` por token), `leer_backup_remoto` (ruta validada + `--`), borrado
  en cascada (IDs `isdigit`). Sólido.
- **Terminal (`/api/terminal/run`):** RCE por diseño, pero bien contenido —
  permiso `terminal`, host restringido a máquinas configuradas, límite de
  longitud y auditoría completa.
- **Auth/sesión/CSRF:** bcrypt (passlib), lockout por IP, CSRF con
  `compare_digest`, cookie `httponly`+`samesite=lax`+`https_only` configurable,
  orden de middleware correcto, gating por `has_permission`/`is_admin`.
- **Restauración/retención:** `restore_api.sh` valida ID, confirmación, contención
  de ruta (`readlink -m`), SHA256 y `gzip -t`. `safe_retention_cleanup` nunca borra
  fuera del root permitido.
- **Asistente IA (resto):** auth + permiso + rate limiting + límites de longitud +
  sanitización de historial; sin acceso a herramientas (prompt-injection de bajo
  riesgo).
- **Central Support:** SQL parametrizado, `validate_client_token` rechaza cliente
  inactivo y usa `compare_digest`, y la consulta de ticket verifica pertenencia al
  cliente (sin fuga entre clientes).
- **Alertas/monitorización:** SQL parametrizado; contenido de alertas interno.
- **Scripts bash restantes:** `servicios_api.sh` (ACTION whitelist, SERVICE
  saneado), `sync_external_backup.sh` (config de operador, `trap cleanup`). Todos
  con `set -euo pipefail`.

## 4. Notas menores · ✅ TODAS CORREGIDAS (commit posterior)

Inicialmente registradas como de bajo impacto; corregidas a petición del
desarrollador para dejar el código 100 % limpio:

- ✅ Central `GET /api/v1/support/tickets/{id}`: ahora valida el token del cliente
  **antes** de revelar la existencia del ticket (elimina el oráculo de existencia).
- ✅ Modelo Anthropic por defecto actualizado de `claude-3-haiku-20240307`
  (deprecado) a `claude-haiku-4-5`, en `main.py` y `config.env.example`.
- ✅ `asistente_chat_api`: un body JSON malformado devuelve ahora 400 (no 500).
- ✅ `backups_api.sh`: se rechaza un nombre de BD que empiece por `-` para que
  `mysqldump` no lo interprete como una opción.

## 5. Verificación

- `python -W error::SyntaxWarning -m py_compile main.py` → limpio.
- `bash -n backups_api.sh` → OK; EOL LF preservado (`file`).
- `check_api_package_installable.ps1` → 50/50 OK.
- `check_repo_clean.ps1` → exit 0.

---

## 6. Segundo pase — rendimiento y consistencia (2026-06-11)

Revisión adicional con foco distinto al de seguridad: rendimiento, concurrencia y
consistencia. Tres hallazgos, **todos corregidos**.

### OPT-1 — Multiplexación SSH (rendimiento)
- **Dónde:** `/api/dashboard/status` (3 conexiones SSH/petición) y
  `/api/monitoreo/metrics` (4 conexiones al mismo host: loadavg, meminfo, df, uptime).
- **Causa:** cada dato abría una conexión SSH nueva (TCP + handshake cripto) en
  serie. En páginas que autorefrescan, la latencia es la suma de todas.
- **Fix:** `build_ssh_base_command` añade `ControlMaster=auto` +
  `ControlPath=…/cm-%C` + `ControlPersist=30`. La primera conexión deja un socket
  de control y las siguientes lo reutilizan (1 handshake + N aperturas baratas).
  Configurable (`VIGEX_SSH_MULTIPLEX`, `_CONTROL_PERSIST`, `_CONTROL_DIR`) y con
  degradación elegante si el socket no es escribible. Sin nueva superficie de
  seguridad: mismo host/usuario/clave, allowlist intacto.

### CONS-1 — Thread-safety inconsistente (concurrencia)
- **Causa:** el módulo de informes usaba `_REPORTS_LOCK`, pero `_login_failures`,
  `_rag_rate_buckets` y el subsistema proactivo se modificaban desde varios hilos
  (threadpool de FastAPI + worker de fondo) sin lock → posibles pérdidas de
  actualización en patrones leer-modificar-escribir.
- **Fix:** locks dedicados — `_login_lock`, `_rag_rate_lock` y `_proactivo_lock`
  (este serializa `_run_proactive_checks`, llamado por el worker y por el endpoint
  manual de check). `_proactivo_estado` queda protegido sin candar cada campo.

### CONS-2 — Comandos SSH construidos a mano (consistencia)
- **Causa:** `leer_backup_remoto` y `run_ssh_terminal_command` armaban el comando
  SSH a mano, sin `ConnectTimeout` y sin multiplexación.
- **Fix:** ambos usan ya `build_ssh_base_command`. Una operación contra un host
  inaccesible falla rápido (10 s) en vez de colgarse hasta `SSH_TIMEOUT` (30 s).

**Notas observadas, no corregidas (sin impacto real):** `get_db()` sin
`try/finally` (no se filtra hoy porque las rutas con red capturan internamente) y
`cargar_historial_backups(limit=1)` que transfiere el `history.tsv` entero.

**Verificación:** `py_compile` sin warnings, `check_api_package_installable` 50/50,
`check_repo_clean` exit 0.
