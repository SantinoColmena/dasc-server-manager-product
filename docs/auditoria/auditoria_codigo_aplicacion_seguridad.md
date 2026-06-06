# Auditoría de seguridad y calidad del código de aplicación

Fecha: 2026-06-06
Versión auditada: `v1.0-rc1` (rama de trabajo Fase 6)
Autor: revisión asistida (Claude Code)

## Objetivo

Revisar el **código de aplicación** de DASC Server Manager (panel/API local y
Central Support) en busca de errores, incompatibilidades, fallos de
ciberseguridad, y oportunidades de optimización sobre lo que ya está
desarrollado y a priori cerrado.

## Contexto

La tarea R-052 (cerrada en R-052H) realizó una revisión de seguridad centrada en
**infraestructura**: secretos en el repositorio, permisos de instalación,
exposición de puertos, claves SSH, usuario de servicio dedicado y endurecimiento
de Central Support.

Esta auditoría **extiende R-052 al nivel de código de aplicación**, que no había
sido revisado en profundidad: inyección de comandos/SQL, gestión de sesión,
control de acceso, path traversal, comparación de secretos y dependencias.

## Alcance

Revisado:

- `deploy/api/package/main.py` — rutas de SSH remoto, terminal web, backups,
  servicios, login/sesión, gestión de usuarios, descarga/restauración.
- `deploy/central-support/package/main.py` — autenticación de API por token,
  login de panel, consultas SQL.
- `deploy/backup-services/package/servicios_api.sh` — validación de entrada.

No cubierto en esta pasada (pendiente):

- Módulo de alertas/Telegram.
- `scripts/retry_central_pending.py`.
- Scripts de instalación, nginx y hardening en detalle.
- XSS en plantillas Jinja2 (autoescapado activo por defecto, riesgo bajo).
- Auditoría CVE completa de dependencias (`pip-audit`).

## Resumen de hallazgos

| ID | Severidad | Hallazgo | Estado |
|---|---|---|---|
| H-1 | 🔴 Alta | Inyección de comandos remota vía SSH en `/backups/run` y `/servicios/accion` | ✅ Resuelto |
| M-1 | 🟠 Media | CORS `*` con `allow_credentials=True` y sin protección CSRF | Pendiente |
| M-2 | 🟠 Media | Cookie de sesión sin `https_only`, sin caducidad ni timeout | Pendiente |
| M-3 | 🟠 Media | Sin protección anti fuerza bruta en `/login` | Pendiente |
| M-4 | 🟠 Media | Contraseñas en texto plano en Central Support | Pendiente |
| M-5 | 🟠 Media | Token de cliente comparado sin tiempo constante | Pendiente |
| L-1 | 🟡 Baja | Permiso `terminal` = ejecución remota de comandos por diseño | Documentar |
| L-2 | 🟡 Baja | `paramiko` en `requirements.txt` aparentemente sin uso | Pendiente |
| L-3 | 🟡 Baja | Incompatibilidad conocida `passlib 1.7.4` + `bcrypt 4.0.1` | Verificar |
| L-4 | 🟡 Baja | Fuga de detalle de error (`stderr`/excepciones) al usuario | Pendiente |
| L-5 | 🟡 Baja | `@app.on_event("startup")` deprecado (Central Support) | Pendiente |
| L-6 | 🟡 Baja | `main.py` ~5000 líneas en un solo fichero (mantenibilidad) | Pendiente |

---

## H-1 (ALTA) — Inyección de comandos remota vía SSH · RESUELTO

### Descripción

`ssh_run()` pasaba `[script] + args` como operandos separados al cliente `ssh`
local. OpenSSH **reconcatena esos operandos con espacios y los entrega al shell
del usuario remoto**, que sí interpreta metacaracteres. `validate_ssh_run()`
solo comprueba que el script esté en la allowlist y la longitud del argumento;
**no saneaba metacaracteres**.

Los endpoints `/backups/run` (campos `db`, `dest`, `name`, `base_ref`, `notes`)
y `/servicios/accion` (campos `service`, `action`) pasaban input del usuario
**sin validar ni escapar**. Un usuario autenticado con permiso `backups` (o
`servicios`) podía inyectar `;`, `$()` o backticks y ejecutar comandos
arbitrarios como `dasc` en el host remoto.

### Impacto

- Ejecución remota de comandos autenticada como `dasc` en el host de
  backups/servicios.
- Rompe el modelo de permisos por módulo (un usuario "solo backups" obtiene
  ejecución arbitraria).
- **Evade la allowlist de `validate_ssh_run`**, que es el control de seguridad
  documentado para la ejecución remota.

`servicios_api.sh` bloqueaba `/ ; | &` en el nombre de servicio, pero (a) no
bloqueaba `$()`, backticks ni espacios y (b) esa comprobación se ejecuta
*después* de que el shell remoto ya expandió la sustitución de comandos.

### Corrección aplicada

1. **Corrección central en `ssh_run()`**: el comando remoto se construye ahora
   como una **única cadena con cada token escapado** mediante `shlex.quote`, de
   modo que el shell remoto no interpreta metacaracteres. Esto protege a *todos*
   los llamadores de `ssh_run`, no solo a los dos endpoints.
2. **Validación de entrada (defensa en profundidad)**:
   - Nuevo helper `es_token_simple()` (alfanumérico + caracteres seguros).
   - `/backups/run`: valida `db`, `name`, `base_ref`, fuerza `dest` dentro de
     `/home/dasc/backups`, valida `compress` y `retention` (alineado con
     `automation/create`).
   - `/servicios/accion`: whitelist de `action` ∈ {start, stop, restart} y
     charset de `service`.

### Verificación

- `python -m py_compile main.py` → sin errores.
- Demostración del escapado: el payload `x; touch /tmp/pwned #` queda como un
  único argumento literal `'x; touch /tmp/pwned #'` (no se ejecuta).
- `tools/windows/check_api_package_installable.ps1` → Resultado OK (0 fallidas).

### Nota de diseño

Las rutas de **descarga** (`leer_backup_remoto`) y **automatización**
(`crear_automatizacion_backup_remota`) ya usaban `shlex.quote`. La inconsistencia
era el origen del fallo; ahora el escapado está centralizado en `ssh_run`.

---

## M-1 (MEDIA) — CORS permisivo y ausencia de CSRF

`CORSMiddleware` con `allow_origins=["*"]` y `allow_credentials=True`. El panel
usa cookies de sesión; aunque `SameSite=Lax` (valor por defecto de Starlette)
mitiga el CSRF en POST cross-site, no hay tokens anti-CSRF en los POST que
cambian estado (servicios, backups, usuarios, terminal).

**Recomendación:** restringir `allow_origins` a la(s) URL(s) reales del panel (o
eliminar CORS si no hay frontend externo) y valorar token anti-CSRF.

## M-2 (MEDIA) — Cookie de sesión sin endurecer

`SessionMiddleware(secret_key=SECRET_KEY)` sin `https_only`, sin `max_age`
(por defecto 14 días) y sin timeout de inactividad. Con HTTPS aún pendiente
(límite reconocido en R-052H), la cookie puede viajar en claro.

**Recomendación:** `https_only=True` (al activar HTTPS), `same_site="lax"`,
`max_age` razonable y caducidad de sesión.

## M-3 (MEDIA) — Sin protección anti fuerza bruta en login

`get_auth_user` usa bcrypt (hash lento, correcto), pero `/login` no limita
intentos ni bloquea. Se registran los fallos en `auth_logs` pero no se actúa.

**Recomendación:** límite por IP/usuario con retardo, o fail2ban sobre el log
(coherente con el fail2ban pendiente en R-052H).

## M-4 (MEDIA) — Contraseñas en texto plano en Central Support

El login central usa `hmac.compare_digest` (correcto), pero almacena y compara
las contraseñas **en claro** desde `config.env`, a diferencia del panel local
que usa bcrypt.

**Recomendación:** hashear (bcrypt) también en Central Support.

## M-5 (MEDIA) — Token de cliente sin comparación de tiempo constante

`validate_client_token` compara con `==` (`str(row["token"]) == str(token)`),
vulnerable a ataque de temporización. El login de panel sí usa `compare_digest`.

**Recomendación:** usar `hmac.compare_digest` también para el token de cliente.

---

## Hallazgos de severidad baja / observaciones

- **L-1 — `terminal` = RCE por diseño.** Conceder el permiso `terminal` equivale
  a shell completo en panel + backups + DB. No es un fallo, pero debe
  **documentarse** y reservarse a administradores.
- **L-2 — `paramiko==2.9.3` en `requirements.txt`** aparenta no usarse (el SSH se
  hace por `subprocess`). Si no se usa, eliminar (menos superficie de ataque); si
  se usa, actualizar.
- **L-3 — `passlib 1.7.4` + `bcrypt 4.0.1`**: combinación con incompatibilidad
  conocida (passlib lee `bcrypt.__about__`, eliminado en bcrypt 4.x). Verificar
  hash/verify en la máquina real; considerar fijar `bcrypt<4.1` o actualizar
  passlib.
- **L-4 — Fuga de detalle de error.** `stderr`/excepciones se devuelven en
  respuestas y alertas. Aceptable en panel interno, pero es divulgación de
  información.
- **L-5 — `@app.on_event("startup")`** (Central Support) está deprecado; migrar a
  `lifespan`.
- **L-6 — `main.py` ~5000 líneas** en un solo fichero: deuda de mantenibilidad.
  Modularizar reduciría el riesgo de error al editar.

## Aspectos correctos verificados

- **SQL parametrizado** en todo (pymysql `%s`, SQLite `?`); no se encontró
  inyección SQL.
- **Path traversal en descarga** defendido: `posixpath.normpath` + prefijo
  obligatorio `/home/dasc/backups/` + `shlex.quote` + chequeo de byte nulo.
- **Automatización CRON**: `shlex.quote` + heredoc con delimitador citado + ID
  generado en servidor.
- IDs de backup validados como enteros / `isdigit()`.
- SSH con clave dedicada, `BatchMode`, `StrictHostKeyChecking` y `known_hosts`
  propio.

## Próximos pasos recomendados

1. Abordar M-1 a M-5 (endurecimiento de sesión, CORS/CSRF, fuerza bruta,
   credenciales y comparación de token de Central Support).
2. Resolver L-2 y L-3 junto con la auditoría de dependencias pendiente en R-052H.
3. Documentar L-1 (alcance real del permiso `terminal`).
4. Continuar con R-053 (validación de instalación desde cero) ya con H-1
   corregido.
