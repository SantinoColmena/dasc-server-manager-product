# R-049N-FIX - Corregir visualización de referencia central en soporte local

## Objetivo

Corregir la visualización de la referencia central en el listado y detalle local de tickets.

## Estado

Cerrada.

## Problema detectado

R-049N añadió la columna y el bloque visual de sincronización central, pero la interfaz seguía mostrando:

~~~text
Sin central
Sin referencia central
No sincronizado
~~~

aunque SQLite local sí contenía los datos correctos:

~~~text
central_ticket_id: CENTRAL-2026-0003
central_sync_status: sent
central_sync_detail: Enviado a central: CENTRAL-2026-0003
~~~

## Causa

Los campos existían en SQLite local, pero los objetos `ticket` usados por las plantillas no estaban recibiendo correctamente esos campos.

## Solución aplicada

Se añade un helper robusto que consulta SQLite por `ticket_id` y enriquece los tickets antes de renderizar la plantilla.

Funciones añadidas:

~~~text
get_support_ticket_central_sync
enrich_support_ticket_with_central
enrich_support_tickets_with_central
~~~

## Archivo modificado

~~~text
deploy/api/package/main.py
~~~

## Criterio de validación

Este fix se considera preparado cuando:

- `main.py` compila.
- `dasc-api` arranca.
- `/soporte/tickets` muestra `CENTRAL-2026-0003` para `DASC-2026-004`.
- `/soporte/tickets/DASC-2026-004` muestra:
  - Ticket central: CENTRAL-2026-0003
  - Estado sincronización: sent
  - Detalle sincronización: Enviado a central: CENTRAL-2026-0003
- Tickets antiguos siguen mostrando `Sin central`.
