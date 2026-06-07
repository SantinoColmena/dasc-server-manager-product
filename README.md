# DASC Server Manager

Panel web autohospedado para que una PyME centralice copias de seguridad, logs, servicios, restauración y alertas en uno o varios servidores Linux, sin depender de soluciones cloud externas.

---

## Estado actual

**Fase 7 en curso — Madurez del producto · Release candidate `v1.0-rc1`**

| Hito | Estado |
|---|---|
| Fases 0-5 (MVP → pilotos reales) | ✅ Cerradas |
| Fase 6 — Hardening, validación 3 perfiles, guías, freeze | ✅ Cerrada 2026-06-07 |
| Fase 7 — Madurez del producto (UI/UX, dashboard, informes, monitorización) | 🔵 En curso |
| Fase 8 — Madurez operacional (instalador v2, actualizador, soporte real, IA) | ▶️ Siguiente |
| Fase 9 — Infraestructura de negocio (dominio, web, planes, legal) | ▶️ Siguiente |
| **F9-GATE — Primer cliente de pago** | 🔒 Bloqueado hasta Fases 7+8+9 |

Seguimiento completo: [`docs/ROADMAP.md`](docs/ROADMAP.md)

---

## Arquitectura

El despliegue se divide en hasta tres hosts según el perfil:

| Perfil | Hosts | Uso previsto |
|---|---|---|
| **Lite** | 1 servidor + copia externa obligatoria | Microempresa o piloto inicial |
| **Standard** | 2 servidores (panel+backup / DB) | Perfil recomendado para PyME |
| **Pro** | 3 servidores separados | Separación completa de responsabilidades |

El panel (FastAPI/Uvicorn) se comunica con los otros hosts **exclusivamente por SSH hardened** (ed25519, BatchMode, known_hosts dedicado, lista blanca de comandos permitidos).

---

## Módulos implementados

- Panel web FastAPI con autenticación por sesión (bcrypt, rate-limiting).
- Gestión de usuarios y permisos por módulo.
- Copias de seguridad completas, incrementales y diferenciales (via `backups_api.sh`).
- Validación SHA256 de cada copia generada.
- Historial persistente de backups.
- Restauración controlada con verificación de integridad.
- Descarga y eliminación de copias desde el panel.
- Logs de auditoría (MariaDB).
- Control de servicios del sistema (start/stop/status).
- Alertas por Telegram (configurables).
- Enlace a herramienta de monitorización externa (Cacti, configurable via `CACTI_URL`).
- Soporte con sistema de tickets local + sincronización con DASC Central Support.
- Informes mensuales automáticos.
- Instaladores bash automatizados e idempotentes por perfil.

---

## Seguridad implementada

- Usuario de sistema sin shell (`dasc-api`, no login).
- Uvicorn escucha solo en `127.0.0.1:8000` — expuesto vía nginx.
- Reverse proxy nginx con TLS 1.2/1.3 (autofirmado o Let's Encrypt).
- `DASC_SESSION_HTTPS_ONLY=true` cuando HTTPS está activo.
- UFW activo por host (scripts en `deploy/*/harden_ufw_*.sh`).
- fail2ban: jaulas `sshd` + `dasc-auth` (bloqueo de IPs con intentos fallidos).
- SSH hardened: ed25519, BatchMode, StrictHostKeyChecking, known_hosts dedicado.
- `config.env` protegido (640, root:dasc-api), nunca commiteado.
- Dependencias auditadas con `pip-audit` (sin CVEs conocidos en `v1.0-rc1`).

---

## Estructura del repositorio

```
deploy/
  api/             → Panel FastAPI: instalador, hardening, package/
  backup-services/ → Scripts de backup/restore/servicios + instalador
  db/              → Instalador MariaDB + hardening
  proxy/           → Reverse proxy nginx (HTTPS)
  central-support/ → DASC Central Support (agregador multi-cliente)
config/
  perfiles/        → Plantillas config.env por perfil (Lite/Standard/Pro)
docs/
  guias/           → Guías de uso desde Windows (R-055A/B)
  validaciones/    → Evidencias de validación por requisito
  ROADMAP.md       → Seguimiento completo del proyecto
tools/
  windows/         → Scripts PowerShell de auditoría y validación
scripts/           → Utilidades de configuración y soporte
```

> `app/` es un placeholder vacío de la arquitectura inicial — todo el código
> deployable está en `deploy/`.

---

## Despliegue rápido

**Desde un PC Windows** — guía completa en [`docs/guias/R-055B_despliegue_desde_windows.md`](docs/guias/R-055B_despliegue_desde_windows.md).

**Comandos de referencia (perfil Lite, en la VM/servidor Linux):**

```bash
# 1. Base de datos
cd deploy/db
sudo -E DASC_PROFILE=lite APP_PASSWORD='<pass>' \
    BACKUP_ALLOWED_HOST=127.0.0.1 LOGS_ALLOWED_HOST=127.0.0.1 \
    bash install_db.sh

# 2. Scripts de backup y servicios
cd ../backup-services
sudo -E DASC_PROFILE=lite APP_PASSWORD='<pass>' bash install_backup_services.sh

# 3. Panel API
cd ../api
sudo -E DASC_PROFILE=lite ADMIN_PASSWORD_INPUT='<pass-admin>' \
    DASC_PASS='<pass>' bash install_dasc_api.sh </dev/null

# 4. Proxy HTTPS
cd ../proxy
sudo bash install_reverse_proxy.sh   # activa HTTPS + DASC_SESSION_HTTPS_ONLY=true

# 5. Firewall y fail2ban
cd ../api
sudo bash harden_ufw_api.sh
sudo bash harden_fail2ban_api.sh
```

Checklist completo por perfil: [`docs/validaciones/R-053D_checklist_instalacion_desde_cero.md`](docs/validaciones/R-053D_checklist_instalacion_desde_cero.md)

---

## Documentación principal

| Documento | Descripción |
|---|---|
| [`CHANGELOG.md`](CHANGELOG.md) | Historial de cambios por versión |
| [`docs/ROADMAP.md`](docs/ROADMAP.md) | Estado y progreso de todos los requisitos |
| [`docs/validaciones/R-053D_checklist_instalacion_desde_cero.md`](docs/validaciones/R-053D_checklist_instalacion_desde_cero.md) | Checklist reproducible de instalación por perfil |
| [`docs/guias/R-055A_acceso_navegador_windows.md`](docs/guias/R-055A_acceso_navegador_windows.md) | Guía para el usuario final (navegador Windows) |
| [`docs/guias/R-055B_despliegue_desde_windows.md`](docs/guias/R-055B_despliegue_desde_windows.md) | Guía de despliegue desde Windows para técnicos |
| [`docs/cliente/R-034_manual_rapido_cliente.md`](docs/cliente/R-034_manual_rapido_cliente.md) | Manual rápido para el cliente final |
| [`docs/release/v1.0-rc1.md`](docs/release/v1.0-rc1.md) | Notas de la release candidate actual |

---

## Aviso

DASC Server Manager es un producto en fase de primeras ventas (`v1.0-rc1`).
Ha sido instalado y validado en entornos de laboratorio (3 perfiles, VM Ubuntu 22.04)
y en pilotos reales. Antes de usar en producción crítica se recomienda:

- Revisar la configuración de red y firewall del entorno específico.
- Verificar la restauración de backups en un entorno de prueba.
- Confirmar que las copias externas funcionan y son recuperables.
- Revisar los permisos y usuarios según el principio de mínimo privilegio.
