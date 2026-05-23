# DASC Server Manager Product

DASC Server Manager es una herramienta local orientada a pequeñas y medianas empresas para centralizar la gestión de copias de seguridad, servicios, logs, restauración, control de servicios y alertas desde un panel web sencillo.

Este repositorio corresponde a la versión producto del proyecto, separada del repositorio académico original.

## Objetivo

Convertir el MVP académico en una base de producto más limpia, instalable, documentada y adaptable a distintos escenarios de cliente.

## Estado actual

Fase 4 - Demo y validación: cerrada documentalmente.

Estado:

- Fase 0 cerrada.
- Fase 1 cerrada.
- Fase 2 cerrada y validada en laboratorio real.
- Fase 3 cerrada.
- Fase 4 cerrada a nivel documental.
- Pendiente futuro: ejecución de piloto técnico real.

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
| Fase 3 - Despliegues y copia externa | Cerrada |
| Fase 4 - Demo y validación | Cerrada documentalmente |

## Fase 4 - Resumen

Durante la Fase 4 se han preparado:

- Modo demo sin datos sensibles.
- Propuesta de dominio y web mínima.
- Manual rápido para cliente.
- Base de conocimiento inicial.
- Lista de 30 posibles perfiles de cliente.
- Guion de llamada y demo.
- Checklist de instalación en cliente.
- Selección del primer piloto técnico.
- Documento de cierre de fase.

## Documentación principal

Documentos clave:

- `docs/validaciones/cierre_fase_4_demo_validacion.md`
- `docs/demo/R-032_modo_demo_sin_datos_sensibles.md`
- `docs/web/R-033_dominio_y_web_minima.md`
- `docs/cliente/R-034_manual_rapido_cliente.md`
- `docs/soporte/R-035_base_conocimiento_inicial.md`
- `docs/comercial/R-036_lista_30_posibles_clientes.md`
- `docs/comercial/R-037_guion_llamada_demo.md`
- `docs/cliente/R-038_checklist_instalacion_cliente.md`
- `docs/pilotos/R-039_seleccion_primer_piloto_tecnico.md`

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
- Documentación de cliente y soporte.

## Aviso

Este repositorio está evolucionando de MVP académico a base de producto. Aunque varias fases han sido documentadas y validadas en laboratorio, no debe utilizarse todavía en producción sin una validación adicional de seguridad, red, permisos, copias externas y restauración real.
