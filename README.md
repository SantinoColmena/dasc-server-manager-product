# DASC Server Manager Product

DASC Server Manager es una herramienta local orientada a pequeñas y medianas empresas para centralizar la gestión de copias de seguridad, servicios, logs, restauración, control de servicios y alertas desde un panel web sencillo.

Este repositorio corresponde a la versión producto del proyecto, separada del repositorio académico original.

## Objetivo

Convertir el MVP académico en una base de producto más limpia, instalable, documentada y adaptable a distintos escenarios de cliente.

El objetivo comercial no es vender solo una licencia, sino ofrecer instalación, mantenimiento, backups verificados, restauración, alertas, informes mensuales y soporte para PYMES que no tienen equipo técnico interno.

## Estado actual

Fase 6 - Primeras ventas: **en curso**.

Estado:

- Fase 0 cerrada.
- Fase 1 cerrada.
- Fase 2 cerrada y validada.
- Fase 3 cerrada.
- Fase 4 cerrada.
- Fase 5 cerrada.
- Fase 6 iniciada con preparación de release candidate.

Versión candidata actual:

- `v1.0-rc1`

Esta versión candidata no se considera todavía una versión final de producción. Se usará como base controlada para primeros pilotos de pago o primer cliente real.

## Arquitectura validada en laboratorio

| Máquina | Rol | IP laboratorio | IP acceso desde Windows |
|---|---|---|---|
| lab-api | API / Panel / Reverse proxy HTTPS | 192.168.60.10 | 192.168.1.244 |
| lab-db | MariaDB / Logs / Datos | 192.168.60.20 | 192.168.1.243 |
| lab-backup | Backups + Servicios | 192.168.60.30 | 192.168.1.245 |

## Arquitecturas comerciales previstas

| Perfil | Infraestructura | Uso previsto |
|---|---|---|
| Lite | 1 servidor + copia externa obligatoria | Microempresa o piloto inicial |
| PyME | 2 servidores o servidor + nodo de backups | Perfil recomendado |
| Pro | 3 servidores separados | Separación completa de responsabilidades |

## Módulos principales

- Panel web FastAPI.
- Gestión de usuarios y permisos.
- Backups completos, incrementales y diferenciales.
- Historial de backups.
- Restauración controlada.
- Descarga y eliminación de copias.
- Validación SHA256.
- Logs de actividad.
- Control de servicios.
- Alertas.
- Monitorización.
- Instaladores automatizados.
- Documentación de soporte y despliegue.

## Documentación principal

Documentos clave:

- `docs/release/v1.0-rc1.md`
- `docs/validaciones/R-047_validacion_release_candidate_v1_0_rc1.md`
- `docs/validaciones/Fase_5_cierre_pilotos_reales.md`
- `docs/producto/sla_realista.md`
- `docs/producto/costes_reales.md`
- `docs/producto/paquetes_comerciales.md`

## Aviso

Este repositorio está evolucionando de MVP académico a base de producto.

Aunque existen validaciones reales en laboratorio, DASC Server Manager no debe utilizarse en producción crítica sin una validación adicional del entorno, permisos, red, restauración y copias externas.
