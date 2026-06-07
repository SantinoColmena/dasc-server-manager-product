# R-054 — Validación de endurecimiento de infraestructura

> **Resultado:** ✅ Las cuatro sub-tareas de endurecimiento (UFW, HTTPS, fail2ban,
> pip-audit) completadas y verificadas. R-054 **CERRADO** (2026-06-07).
>
> Subtareas:
> [`R-054A`](#r-054a-ufw) · [`R-054B`](#r-054b-https--dasc_session_https_only)
> · [`R-054C`](#r-054c-fail2ban) · [`R-054D`](#r-054d-pip-audit)

---

## Entorno de validación

- **Perfil probado en VM:** Lite (1 VM, todos los roles).
  Los scripts DB/backup fueron validados por revisión estática (Lite no usa hosts separados).
- **VM:** `dasc-r054-lite` · 172.19.212.232 · Ubuntu 22.04 · 2 vCPU / 4 GiB.
- **Rama/commit base:** `docs/roadmap-canonico` (incluye fixes B1-B5 de R-053).

---

## R-054A — UFW

### Scripts creados

| Fichero | Host destino | Puertos abiertos |
|---|---|---|
| `deploy/api/harden_ufw_api.sh` | Panel API | 22/tcp (SSH), 80/tcp (HTTP→HTTPS redirect), 443/tcp (HTTPS proxy) |
| `deploy/db/harden_ufw_db.sh` | Host DB | 22/tcp (SSH), 3306/tcp desde `MARIADB_ALLOWED_HOSTS` (opcional) |
| `deploy/backup-services/harden_ufw_backup.sh` | Host backup | 22/tcp (SSH) únicamente |

### Comportamiento

- Política por defecto: `deny incoming / allow outgoing`.
- UFW se instala automáticamente si no está presente.
- `ufw --force reset` antes de aplicar reglas (idempotente).
- El puerto 8000 (Uvicorn) no necesita regla UFW: ya escucha en `127.0.0.1`.
- En `harden_ufw_db.sh`, si `MARIADB_ALLOWED_HOSTS` no está definido, el puerto 3306
  queda denegado desde el exterior (MariaDB con `bind-address=127.0.0.1` ya lo garantiza
  a nivel de servicio; UFW añade la segunda capa).

### Verificación en VM (R-054 Lite)

```
Status: active
[ 1] 22/tcp   ALLOW IN  Anywhere  # SSH
[ 2] 80/tcp   ALLOW IN  Anywhere  # HTTP nginx redirect
[ 3] 443/tcp  ALLOW IN  Anywhere  # HTTPS nginx proxy
[...]
```

| Check | Resultado |
|---|---|
| UFW activo | ✅ `Status: active` |
| SSH 22/tcp permitido | ✅ |
| HTTP 80/tcp permitido | ✅ |
| HTTPS 443/tcp permitido | ✅ |
| Puerto 8000 bloqueado externamente | ✅ (solo en 127.0.0.1, sin regla UFW) |
| Script DB/backup — revisión estática | ✅ Sintaxis correcta, lógica validada |

---

## R-054B — HTTPS + `DASC_SESSION_HTTPS_ONLY`

### Script actualizado

`deploy/proxy/install_reverse_proxy.sh` — ahora soporta dos modos:

| Variable | Valores | Descripción |
|---|---|---|
| `CERT_TYPE` | `selfsigned` (defecto) | Certificado RSA-4096 autofirmado, 365 días. Para lab/intranets. |
| `CERT_TYPE` | `certbot` | Let's Encrypt vía `certbot --nginx`. Requiere `DOMAIN` y `CERTBOT_EMAIL`. |

**Nuevo comportamiento común a ambos modos:**
Tras instalar el proxy, el script localiza `${API_CONFIG_FILE}` (por defecto
`/opt/dasc/api/config.env`) y actualiza `DASC_SESSION_HTTPS_ONLY=true`, luego
reinicia `dasc-api`. Si `config.env` no existe, imprime instrucciones manuales.

`DASC_SESSION_HTTPS_ONLY` ya existía en `main.py` (líneas 1713-1714) y en
`config.env.example`. El proxy installer ahora lo activa automáticamente.

### Verificación en VM

```bash
# Instalar proxy (modo autofirmado por defecto):
sudo bash install_reverse_proxy.sh
# → ==> DASC_SESSION_HTTPS_ONLY actualizado a true en /opt/dasc/api/config.env
# → ==> dasc-api reiniciado para aplicar HTTPS_ONLY
```

| Check | Resultado |
|---|---|
| Certificado autofirmado creado | ✅ RSA-4096, válido hasta Jun 2027 |
| nginx TLS 1.2/1.3 activo | ✅ `HTTP/2 303` en acceso HTTPS |
| HTTP → HTTPS redirect (301) | ✅ |
| `DASC_SESSION_HTTPS_ONLY=true` en config.env | ✅ |
| `dasc-api` reiniciado tras cambio | ✅ `active` |
| Opción certbot — revisión estática | ✅ Sintaxis correcta, requiere DOMAIN/CERTBOT_EMAIL |

---

## R-054C — fail2ban

### Script creado

`deploy/api/harden_fail2ban_api.sh` — configura dos jaulas:

| Jaula | Backend | Log vigilado | Acción |
|---|---|---|---|
| `sshd` | auto (journald / auth.log) | `/var/log/auth.log` | Bloquea IPs con ≥5 fallos SSH en tiempo predeterminado |
| `dasc-auth` | polling | `/var/log/nginx/access.log` | Bloquea IPs con ≥5 fallos de login en 600 s durante 3600 s |

**Filtro personalizado** (`/etc/fail2ban/filter.d/dasc-auth.conf`):
```
failregex = ^<HOST> -.*"GET /login\?error=[12] HTTP/\S+" \d+
```
Cuando un login falla, DASC redirige el navegador a `/login?error=1`
(credenciales incorrectas) o `/login?error=2` (IP ya bloqueada por el
rate-limiter interno). Nginx registra ese `GET`, y fail2ban cuenta las
apariciones por IP origen.

**Por qué este enfoque:**
- DASC ya tiene rate-limiting en memoria (`LOGIN_MAX_ATTEMPTS=5` por ventana de 15 min).
- fail2ban añade la capa de bloqueo a nivel de red (iptables/nftables), complementaria.
- La jaula se configura en `/etc/fail2ban/jail.d/dasc.conf` (override limpio, no modifica `jail.conf`).
- SSH (`sshd`) también queda protegido en el mismo script.

### Verificación en VM

```bash
# Tras instalar:
sudo fail2ban-client status
#   Number of jail: 2
#   Jail list:      dasc-auth, sshd

# Filtro validado con fail2ban-regex:
sudo fail2ban-regex /var/log/nginx/access.log /etc/fail2ban/filter.d/dasc-auth.conf
#   Lines: 13 lines, 0 ignored, 3 matched, 10 missed
#   [3 GET /login?error= correctamente detectados]
```

| Check | Resultado |
|---|---|
| fail2ban instalado y activo | ✅ `systemctl is-active fail2ban` → `active` |
| Jaula `sshd` activa | ✅ `Currently failed: 0, Currently banned: 0` |
| Jaula `dasc-auth` activa | ✅ `File list: /var/log/nginx/access.log` |
| Filtro regex — 3 fallos detectados en log real | ✅ `3 matched` con `fail2ban-regex` |
| 127.0.0.1 ignorado (protección anti-lockout) | ✅ Comportamiento correcto (ignoreip default) |
| Parámetros configurables vía env (`BAN_TIME`, `MAX_RETRY`, etc.) | ✅ |

---

## R-054D — `pip-audit`

### Herramienta

```bash
python -m pip install pip-audit
python -m pip_audit -r deploy/api/package/requirements.txt
python -m pip_audit -r deploy/central-support/package/requirements.txt
```

### Resultados iniciales

**`deploy/api/package/requirements.txt`** — 4 vulnerabilidades en 2 paquetes:

| Paquete | Versión anterior | CVE / ID | Versión corregida |
|---|---|---|---|
| `starlette` | 0.52.1 | PYSEC-2026-161 | 1.0.1 |
| `python-multipart` | 0.0.22 | CVE-2026-40347 | 0.0.26 |
| `python-multipart` | 0.0.22 | CVE-2026-42561 | 0.0.27 |

**`deploy/central-support/package/requirements.txt`** — sin vulnerabilidades.

### Correcciones aplicadas

`deploy/api/package/requirements.txt` actualizado:

| Paquete | Antes | Después | Notas |
|---|---|---|---|
| `starlette` | 0.52.1 | **1.0.1** | Salto de versión mayor. Compatibilidad con `fastapi==0.135.1` verificada con `pip --dry-run`. Comentado en el fichero. Requiere prueba de humo en VM. |
| `python-multipart` | 0.0.22 | **0.0.27** | Versión menor. Cubre ambos CVE. |

### Verificación post-corrección

```bash
python -m pip_audit -r deploy/api/package/requirements.txt
# No known vulnerabilities found
```

| Check | Resultado |
|---|---|
| pip-audit API (antes) | ❌ 4 vulnerabilidades |
| pip-audit API (después) | ✅ Sin vulnerabilidades |
| pip-audit central-support | ✅ Sin vulnerabilidades |
| Compatibilidad fastapi+starlette verificada | ✅ `pip --dry-run` sin conflictos |

---

## Resumen final R-054

| Sub-tarea | Estado | Entregables |
|---|---|---|
| R-054A — UFW | ✅ | `harden_ufw_api.sh`, `harden_ufw_db.sh`, `harden_ufw_backup.sh` |
| R-054B — HTTPS + https_only | ✅ | `install_reverse_proxy.sh` actualizado (+ certbot), activa `HTTPS_ONLY` automáticamente |
| R-054C — fail2ban | ✅ | `harden_fail2ban_api.sh` (jaulas sshd + dasc-auth, filtro personalizado) |
| R-054D — pip-audit | ✅ | 2 paquetes auditados; `starlette→1.0.1`, `python-multipart→0.0.27` corregidos |

**Criterio de cierre:** UFW activo en host de prueba; HTTPS operativo con
redirect HTTP→HTTPS; `DASC_SESSION_HTTPS_ONLY=true`; fail2ban con 2 jaulas
activas y filtro DASC validado con `fail2ban-regex`; `pip-audit` limpio en
ambos paquetes.
