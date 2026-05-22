# Validación real de Fase 2 en laboratorio Ubuntu

## Objetivo

Validar en máquinas Ubuntu reales la Fase 2 de DASC Server Manager: seguridad, restauración, integridad, retención, auditoría y reverse proxy.

## Arquitectura de laboratorio

| Máquina | Rol | IP |
|---|---|---|
| VM 1 | API / Panel | 192.168.60.10 |
| VM 2 | Base de datos MariaDB | 192.168.60.20 |
| VM 3 | Backups + Servicios | 192.168.60.30 |

## Estado inicial

| Comprobación | Estado |
|---|---|
| Repo actualizado en Windows | Pendiente |
| Rama de validación creada | Pendiente |
| Máquinas Ubuntu disponibles | Pendiente |
| Conectividad entre máquinas | Pendiente |
| Usuario con sudo disponible | Pendiente |

## Validación por bloques

| Bloque | Estado |
|---|---|
| Instalación DB | Pendiente |
| Instalación backup-services | Pendiente |
| Instalación API | Pendiente |
| SSH endurecido | Pendiente |
| Hash de usuarios | Pendiente |
| config.env seguro | Pendiente |
| Backup completo | Pendiente |
| Backup incremental/diferencial | Pendiente |
| Integridad SHA256 | Pendiente |
| Simulacro de recuperación | Pendiente |
| Restauración controlada | Pendiente |
| Retención segura | Pendiente |
| Auditoría local | Pendiente |
| Reverse proxy HTTPS | Pendiente |

## Evidencias pendientes

- Captura o salida de `systemctl status mariadb`.
- Captura o salida de `systemctl status dasc-api`.
- Captura o salida de `systemctl status ssh`.
- Captura o salida de `/usr/local/bin/backups_api.sh`.
- Captura o salida de `history.tsv`.
- Captura o salida de `checksums.sha256`.
- Captura o salida de `audit.log`.
- Captura o salida de `restore_drill_api.sh`.
- Captura o salida de `restore_api.sh`.
- Captura o salida de `nginx -t`.
- Captura de acceso al panel por HTTPS.

## Resultado final

Pendiente.
