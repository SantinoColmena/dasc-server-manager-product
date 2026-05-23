# DASC Server Manager Product

DASC Server Manager es una herramienta local orientada a pequeñas y medianas empresas para centralizar la gestión de copias de seguridad, servicios, logs, restauración, control de servicios, terminal remoto y alertas desde un panel web sencillo.

Este repositorio corresponde a la versión producto del proyecto, separada del repositorio académico original.

## Objetivo

Convertir el MVP académico en una base de producto más limpia, instalable, documentada y adaptable a distintos escenarios de cliente.

## Estado actual

Fase 5 - Pilotos reales: completada a nivel técnico y documental.

Estado:

- Fase 0 cerrada.
- Fase 1 cerrada.
- Fase 2 cerrada y validada en laboratorio real.
- Fase 3 cerrada.
- Fase 4 cerrada a nivel documental.
- Fase 5 cerrada con pilotos técnicos, incidencias, SLA y costes.

## Arquitecturas validadas

| Perfil | Arquitectura | Estado |
|---|---|---|
| Laboratorio original | 3 máquinas Ubuntu | Validado |
| PyME estándar | 2 servidores | Validado en piloto 1 |
| Lite | 1 servidor + copia externa simulada | Validado en piloto 2 |
| Pro | 3 servidores o arquitectura ampliada | Previsto como mejora futura |

## Pilotos realizados

| Piloto | Perfil | Resultado |
|---|---|---|
| Piloto 1 | 2 servidores | Validado |
| Piloto 2 | 1 servidor + copia externa | Validado |
| Piloto 3 | Opcional | Cerrado mediante justificación técnica |

## Fases completadas

| Fase | Estado |
|---|---|
| Fase 0 - Preparación | Cerrada |
| Fase 1 - Núcleo estable | Cerrada |
| Fase 2 - Seguridad y restauración | Cerrada y validada en laboratorio real |
| Fase 3 - Despliegues y copia externa | Cerrada |
| Fase 4 - Demo y validación | Cerrada documentalmente |
| Fase 5 - Pilotos reales | Cerrada |

## Fase 5 - Resumen

Durante la Fase 5 se han validado:

- Instalación piloto en perfil PyME de 2 servidores.
- Medición de incidencias del piloto 1.
- Corrección de fallos detectados en piloto 1.
- Instalación piloto en perfil Lite de 1 servidor + copia externa simulada.
- Cierre justificado del piloto 3 opcional.
- Definición de SLA realista.
- Recalculo de costes reales.
- Correcciones en instaladores y configuración derivadas de pilotos reales.

## Documentación principal

Documentos clave:

- `docs/pilotos/R-040_instalacion_piloto_1_2_servidores.md`
- `docs/pilotos/R-041_medicion_incidencias_piloto_1.md`
- `docs/pilotos/R-042_correccion_fallos_piloto_1.md`
- `docs/pilotos/R-043_instalacion_piloto_2_1_servidor_externo.md`
- `docs/pilotos/R-044_piloto_3_opcional.md`
- `docs/pilotos/R-045_sla_realista.md`
- `docs/pilotos/R-046_recalculo_costes_reales.md`
- `docs/pilotos/cierre_fase_5_pilotos_reales.md`

## Arquitecturas previstas

El producto se diseña para poder adaptarse a diferentes escenarios:

- 1 servidor: instalación Lite, siempre con copia externa obligatoria.
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
- Terminal remoto.
- Alertas.
- Monitorización.
- Documentación de cliente y soporte.

## Aviso

Este repositorio está evolucionando de MVP académico a base de producto. Aunque varias fases han sido documentadas y validadas en laboratorio y pilotos controlados, no debe utilizarse todavía en producción sin una validación adicional de seguridad, red, permisos, copias externas reales y restauración real con datos del cliente.