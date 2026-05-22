# DASC Server Manager Product

DASC Server Manager es una herramienta local orientada a pequeñas y medianas empresas para centralizar la gestión de copias de seguridad, servicios, logs, restauración, control de servicios y alertas desde un panel web sencillo.

Este repositorio corresponde a la versión producto del proyecto, separada del repositorio académico original.

## Objetivo

Convertir el MVP académico en una base de producto más limpia, instalable, documentada y adaptable a distintos escenarios de cliente.

## Estado actual

Fase 2 - Seguridad y restauración: **cerrada**.

Estado:

- Implementada.
- Documentada.
- Validada en laboratorio real Ubuntu con tres máquinas.
- Fusionada en `main`.

## Arquitectura validada en laboratorio

| Máquina | Rol | IP laboratorio | IP acceso desde Windows |
|---|---|---|---|
| lab-api | API / Panel / Reverse proxy HTTPS | 192.168.60.10 | 192.168.1.244 |
| lab-db | MariaDB / Logs / Datos | 192.168.60.20 | 192.168.1.243 |
| lab-backup | Backups + Servicios | 192.168.60.30 | 192.168.1.245 |

## Fases completadas

| Fase | Estado |
|---|---|
| Fase 0 - Preparación | Cerrada |
| Fase 1 - Núcleo estable | Cerrada |
| Fase 2 - Seguridad y restauración | Cerrada y validada en laboratorio real |

## Fase 2 - Resumen

Durante la Fase 2 se han validado:

- Hash de contraseñas con bcrypt.
- Protección de `config.env`.
- Instaladores reales para API, DB y backup-services.
- SSH dedicado para DASC.
- Backups completos reales.
- Historial de backups.
- Validación SHA256.
- Simulacro de recuperación.
- Restauración controlada.
- Retención segura.
- Auditoría local.
- Logs remotos en MariaDB.
- Reverse proxy Nginx con HTTPS autofirmado.
- Acceso real desde navegador Windows.

## Documentación principal

Documentos clave:

- `docs/tecnico/fase_2_seguridad_restauracion.md`
- `docs/validaciones/Fase_2_validacion_real_laboratorio.md`
- `docs/validaciones/Fase_2_validacion_visual_panel.md`
- `docs/validaciones/R-021_retencion_limpieza_backups_real.md`

## Arquitecturas previstas

El producto se diseña para poder adaptarse a diferentes escenarios:

- 1 servidor: instalación Lite.
- 2 servidores: instalación PyME recomendada.
- 3 servidores: instalación Pro con separación completa.

## Módulos previstos

- Panel web FastAPI.
- Gestión de usuarios y permisos.
- Backups completos, incrementales y diferenciales.
- Historial de backups.
- Restauración y descarga de copias.
- Logs de actividad.
- Control de servicios.
- Alertas.
- Monitorización.

## Aviso

Este repositorio está evolucionando de MVP académico a base de producto. Aunque la Fase 2 ha sido validada en laboratorio real, no debe utilizarse todavía en producción sin una validación adicional de seguridad, red, permisos y copias externas.
