# R-049N-FIX3 - Enriquecer búsqueda de tickets locales con referencia central

## Objetivo

Corregir definitivamente el listado local `/soporte/tickets` para que muestre la referencia central guardada en SQLite local.

## Estado

Cerrada.

## Problema detectado

Los fixes anteriores no afectaban al listado porque `/soporte/tickets` no usa `list_support_tickets()`.

La ruta usa:

~~~text
search_support_tickets()
~~~

## Solución aplicada

Se modifica directamente:

~~~text
search_support_tickets()
~~~

para enriquecer los tickets antes de devolverlos a la plantilla.

Ahora ejecuta:

~~~text
enrich_support_tickets_with_central(tickets)
~~~

antes de hacer `return tickets`.

## Archivo modificado

~~~text
deploy/api/package/main.py
~~~

## Criterio de validación

Este fix queda preparado cuando:

- `main.py` compila.
- `dasc-api` arranca.
- `/soporte/tickets` muestra `CENTRAL-2026-0003` para `DASC-2026-004`.
- Los tickets antiguos muestran `Sin central`.
- El detalle de `DASC-2026-004` muestra:
  - Ticket central: CENTRAL-2026-0003
  - Estado sincronización: sent
  - Detalle sincronización: Enviado a central: CENTRAL-2026-0003
