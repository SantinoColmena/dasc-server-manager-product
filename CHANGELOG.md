# Changelog — Vigex

Formato basado en [Keep a Changelog](https://keepachangelog.com/es/1.1.0/).
Versiones en `MAJOR.MINOR-STAGE` según el ciclo del producto.

---

## [v1.0-rc1] — 2026-06-07 (freeze Fase 6)

> Tag movido al commit de cierre de R-057 (2026-06-07).
> El tag original de 2026-05-23 (`7fc07a1`) marcaba el fin de Fase 5.
> Esta entrada documenta todo lo incorporado durante la Fase 6.

### Sistema de soporte integrado en el panel (R-044 / R-045 / R-046)

- Formulario de tickets de soporte accesible desde el panel web.
- Almacenamiento local de tickets en SQLite (`data/soporte.db`).
- Vista interna de tickets con filtros por estado y prioridad.
- Gestión de estados (Abierto → En progreso → Resuelto → Cerrado) y prioridades.
- Plantillas de respuesta configurables para el técnico.
- Separación de roles: vista cliente / acceso técnico Vigex.

### Vigex Central (R-049)

- Nueva aplicación independiente (`deploy/central-support/`) — agregador multi-cliente.
- API REST con autenticación por `X-Vigex-Client-Token` por cliente.
- Panel web propio con login, lista de tickets y gestión de estado/prioridad.
- Sincronización bidireccional: el panel local envía tickets al central; el estado
  actualizado en el central se sincroniza de vuelta al panel local.
- Cola offline con reintentos automáticos (`scripts/retry_central_pending.py`),
  gestionada por systemd timer (`install_central_retry_timer.sh`).
- Referencia cruzada: cada ticket local muestra el ID central asignado.
- Instalador systemd (`install_central_support.sh`), servicio en puerto 8010.
- Reverse proxy nginx para el panel central.
- Credenciales endurecidas: hash PBKDF2 generado en el instalador (M-4).

### Herramientas operativas (R-040 / R-041 / R-042)

- **Informe operativo mensual** (`tools/windows/generate_monthly_report.ps1`):
  genera Markdown con resumen de backups, estado de servicios y alertas del mes.
- **Backup completo automatizado** (`scripts/run_backup_completo.sh`):
  script invocable vía cron para lanzar backups sin intervención manual.
- **Retención y limpieza automática de backups**: configurable por número de copias
  a conservar; elimina las más antiguas respetando el mínimo definido.
- Informe operativo integrado en el panel web (`/informe`).
- **Restauración controlada**: interfaz de restauración con verificación de
  integridad SHA256 antes de restaurar.

### Instaladores adaptables por perfil (R-036 / R-047)

- `install_vigex_api.sh`, `install_db.sh`, `install_backup_services.sh` adaptan
  su comportamiento según `VIGEX_PROFILE` (lite / standard / pro / custom).
- Plantillas de `config.env` por perfil en `config/perfiles/`.
- `scripts/generar_config_perfil.sh` genera `config.env` a partir de la plantilla.
- Parámetros de host (DB, backup) completamente parametrizados; sin IPs de
  laboratorio en los instaladores de producción.
- Generación de fichero de secretos `/root/vigex-db-install-secrets.env` por el
  instalador de DB para coordinar instalaciones multi-host.

### Hardening de seguridad — auditoría interna

Hallazgos corregidos durante la auditoría de Fase 6 (antes de R-053):

| ID | Severidad | Descripción | Corrección |
|---|---|---|---|
| H-1 | Alta | Inyección de comandos por SSH: parámetros sin sanitizar en `validate_ssh_run()` | Validación estricta de allowlist; args tipados |
| M-1 | Media | Ausencia de protección CSRF en formularios POST | Token CSRF generado por sesión en todos los formularios |
| M-2/M-3 | Media | Headers de seguridad HTTP faltantes | `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy` añadidos |
| M-4 | Media | Hash PBKDF2 de contraseña admin del Central Support generado en texto plano | Instalador genera hash en instalación |
| M-5 | Media | `config.env` del Central Support con permisos excesivos | Protegido a 600, propiedad root |
| L-2 | Baja | SECRET_KEY débil en algunos entornos de prueba | Generación forzada aleatoria en instalador |
| L-3 | Baja | Versión bcrypt incompatible con passlib | Fijado `bcrypt==4.0.1` |
| L-5 | Baja | Información de versión expuesta en cabeceras | Cabecera `Server` eliminada |

### R-053 — Validación de instalación en 3 perfiles

- **B1**: `requirements.txt` con dependencias fijadas; `.python-version` añadido.
- **B2**: virtualenv creado en directorio relativo al paquete (`package/venv/`).
- **B3**: detección de distribución Linux en instaladores (`/etc/os-release`).
- **B4**: paso de `DB_HOST` vía variable de entorno en Standard (antes hardcodeado).
- **B5**: instalador de backup-services solicita `DB_HOST` interactivamente si no
  está en el entorno.
- Checklist reproducible por perfil: `docs/validaciones/R-053D_checklist_instalacion_desde_cero.md`.
- Validación completa documentada en `docs/validaciones/R-053_*` (Lite, Standard, Pro).

### R-054 — Endurecimiento de infraestructura

- **UFW**: scripts `harden_ufw_api.sh`, `harden_ufw_db.sh`, `harden_ufw_backup.sh`
  con política `deny incoming / allow outgoing` y apertura mínima por host.
- **HTTPS**: `install_reverse_proxy.sh` actualizado con soporte `CERT_TYPE=selfsigned`
  (autofirmado RSA-4096) y `CERT_TYPE=certbot` (Let's Encrypt). Activa automáticamente
  `VIGEX_SESSION_HTTPS_ONLY=true` en `config.env` y reinicia el servicio.
- **fail2ban**: `harden_fail2ban_api.sh` — jaulas `sshd` + `vigex-auth`; filtro
  personalizado que detecta `GET /login?error=[12]` en el log de nginx.
- **pip-audit**: dependencias API auditadas; vulnerabilidades corregidas:
  - `starlette` 0.52.1 → 1.0.1 (PYSEC-2026-161)
  - `python-multipart` 0.0.22 → 0.0.27 (CVE-2026-40347, CVE-2026-42561)

### R-055 — Guías de uso desde Windows

- `docs/guias/R-055A_acceso_navegador_windows.md` — guía usuario final: URL,
  aviso certificado autofirmado por navegador, secciones del panel.
- `docs/guias/R-055B_despliegue_desde_windows.md` — guía técnico/reseller:
  SSH nativo de Windows, dos métodos de transferencia del repo, transferencia de
  secretos entre servidores vía Windows como intermediario, hardening post-instalación.
- `docs/guias/R-055C_decision_script_auxiliar.md` — decisión documentada: no se
  crea wrapper PowerShell de despliegue; SSH nativo es suficiente para el perfil objetivo.

### R-056 — Limpieza de repositorio y documentación

- `README.md` completamente reescrito: estado actual por hitos, arquitectura,
  módulos reales implementados, seguridad, estructura del repo, despliegue rápido.
- Módulo "Monitorización" corregido: no es un módulo del panel sino un enlace
  externo configurable vía `CACTI_URL` (Cacti o equivalente).
- Sin IPs de laboratorio en documentación pública.
- `docs/ROADMAP.md` actualizado como fuente de verdad única de Fase 6.
- `tools/windows/check_repo_clean.ps1` y `check_api_package_installable.ps1`
  en verde tras la limpieza.

---

## [v0.1-interna] — 2025 (histórico)

Primera versión interna del MVP académico. Incluía:

- Panel FastAPI básico con autenticación por sesión.
- Gestión de usuarios y permisos por módulo.
- Backups completos via SSH a host de backup.
- Logs de auditoría en MariaDB.
- Control de servicios.
- Alertas básicas por Telegram.
- Instaladores bash para Ubuntu (versión inicial, perfil único).

Esta versión evolucionó hacia `v1.0-rc1` a través de las Fases 1-5 del proyecto,
que añadieron backups incrementales y diferenciales, SHA256, historial, restauración,
pilotos reales, SLA, costes y la base de documentación comercial.

---

[v1.0-rc1]: https://github.com/colme/vigex-server-manager-product/releases/tag/v1.0-rc1
[v0.1-interna]: https://github.com/colme/vigex-server-manager-product/releases/tag/v0.1-interna
