# R-049M - Cierre guardar central_ticket_id en ticket local

## Objetivo

Cerrar la validación de trazabilidad entre tickets locales del panel cliente y tickets centrales del panel DASC.

## Estado

Cerrada.

## Funcionalidad implementada

R-049M permite guardar en SQLite local la relación entre un ticket local y su ticket correspondiente en el panel central.

Columnas añadidas dinámicamente a `support_tickets`:

~~~text
central_ticket_id
central_sync_status
central_sync_detail
central_sync_at
~~~

## Archivo modificado

~~~text
deploy/api/package/main.py
~~~

## Documento de validación

~~~text
docs/validaciones/R-049M_guardar_central_ticket_id_local.md
~~~

## Validación realizada

Se creó un nuevo ticket desde el panel local:

~~~text
DASC-2026-004
~~~

El panel central creó el ticket asociado:

~~~text
CENTRAL-2026-0003
~~~

## Validación SQLite central

En la base central `central_support.db` se confirmó:

~~~text
id: CENTRAL-2026-0003
cliente_id: cliente-demo-a
ticket_local_id: DASC-2026-004
tipo: Consulta
prioridad: Alta
servicio: API / Panel
estado: Nuevo
~~~

## Validación SQLite local

En la base local `support_tickets.db` se confirmó:

~~~text
id: DASC-2026-004
central_ticket_id: CENTRAL-2026-0003
central_sync_status: sent
central_sync_detail: Enviado a central: CENTRAL-2026-0003
central_sync_at: 2026-05-25 19:16:32
~~~

## Validación de logs

En `dasc_logs.eventos` se confirmó:

~~~text
POST /soporte central DASC-2026-004
OK
Enviado a central: CENTRAL-2026-0003
~~~

También se confirmó el evento local:

~~~text
POST /soporte DASC-2026-004
OK
Ticket de soporte creado: Consulta / Alta / API / Panel
~~~

## Nota sobre tickets anteriores

Los tickets anteriores a R-049M, como:

~~~text
DASC-2026-003
DASC-2026-002
DASC-2026-001
~~~

pueden tener los campos centrales vacíos porque fueron creados antes de añadir la trazabilidad local-central.

Esto no representa un error.

R-049M aplica correctamente a tickets nuevos creados después de la actualización.

## Resultado

R-049M queda validada correctamente.

El panel local ahora conserva la referencia del ticket central y el estado de sincronización.

## Límites actuales

Esta versión todavía no incluye:

- Mostrar `central_ticket_id` en la interfaz local.
- Reintentos automáticos.
- Cola offline.
- Sincronización de estado central hacia local.
- Búsqueda cruzada local-central.
- Gestión visual de errores de sincronización.
- Panel cliente definitivo separado.
- HTTPS real.
- Tokens rotables desde interfaz.

## Próxima tarea recomendada

~~~text
R-049N - Mostrar referencia central en la vista local de tickets
~~~

Después podrían seguir:

~~~text
R-049O - Cola offline y reintentos de envío central
R-049P - Sincronización de estado central hacia local
R-049Q - Login y roles del panel central
R-049R - Instalador systemd para central-support
~~~

## Conclusión

DASC Server Manager supera R-049M.

El flujo local-central ya no solo crea tickets en ambos lados, sino que mantiene trazabilidad entre el ticket local del cliente y el ticket central gestionado por DASC.
