# R-049X - Documentación global del soporte central/local

## Objetivo

Documentar globalmente el módulo de soporte central/local de DASC Server Manager.

## Estado

En curso.

## Contexto

Después de R-049L a R-049W, el soporte central/local dejó de ser una función aislada y pasó a ser un módulo completo de producto.

Incluye:

- Formulario local de soporte.
- Vista cliente limpia.
- Vista técnica local.
- Cola offline.
- Reintentos.
- Sincronización central-local.
- Panel central DASC.
- Login central.
- Nginx.
- Endurecimiento básico de credenciales.

## Documentos creados

- docs/producto/soporte_central_local.md
- docs/arquitectura/soporte_central_local_arquitectura.md
- docs/validaciones/R-049X_documentacion_global_soporte_central_local.md

## Contenido documentado

Se documenta:

- Objetivo del módulo.
- Separación de responsabilidades.
- Vista cliente.
- Vista técnica local.
- Panel central.
- Rutas principales.
- Flujo de alta de ticket.
- Flujo de reintento offline.
- Flujo de sincronización central-local.
- Estados.
- Prioridades.
- Seguridad aplicada.
- Seguridad futura.
- Nginx.
- DNS local.
- Arquitectura objetivo.
- Variables relevantes.
- Bases de datos.
- Evidencias validadas.
- Limitaciones actuales.

## Criterio de validación

R-049X se considera preparada cuando:

- Existe documentación global del módulo.
- Existe documentación de arquitectura resumida.
- Se diferencia claramente cliente, técnico local y central DASC.
- Se documenta la diferencia entre panel local y panel central.
- Se documenta el criterio de DNS local.
- Se documenta la evolución futura a VPS/dominio.
- Los documentos quedan versionados en GitHub.

## Resultado esperado

El proyecto queda preparado para explicar el módulo de soporte central/local como parte de la evolución de DASC Server Manager hacia producto-servicio.
