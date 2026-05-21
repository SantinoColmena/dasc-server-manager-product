# DASC Server Manager Product

DASC Server Manager es una herramienta local orientada a pequeñas y medianas empresas para centralizar la gestión de copias de seguridad, servicios, logs y alertas desde un panel web sencillo.

Este repositorio corresponde a la versión producto del proyecto, separada del repositorio académico original.

## Objetivo

Convertir el MVP académico en una base de producto más limpia, instalable, documentada y adaptable a distintos escenarios de cliente.

## Estado actual

Fase actual del roadmap:

- R-001 - Separación del proyecto académico y producto.
- R-002 - Definición de propuesta de valor comercial.
- R-003 - Definición de paquetes Lite, PyME y Pro.
- R-004 - Inventario del estado actual del código.
- R-005 - Definición de límites de responsabilidad.

## Arquitecturas previstas

El producto se diseñará para poder adaptarse a diferentes escenarios:

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
- Monitorización con Cacti.

## Aviso

Este repositorio está en fase inicial de preparación de producto. No debe utilizarse todavía en producción sin validación técnica previa.
