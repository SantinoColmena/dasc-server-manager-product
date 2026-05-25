# R-049N-FIX2 - Enriquecer listado local con referencia central

## Objetivo

Corregir definitivamente el listado local `/soporte/tickets` para que muestre la referencia del ticket central.

## Estado

Cerrada.

## Problema

El fix anterior añadió funciones para leer la sincronización central, pero no consiguió insertar el enriquecimiento en la ruta del listado.

El error detectado fue:

~~~text
No se encontró asignación tickets = list_support_tickets(...).
~~~

## Solución

Se modifica directamente la función:

~~~text
list_support_tickets()
~~~

para que antes de devolver los tickets ejecute:

~~~text
enrich_support_tickets_with_central(tickets)
~~~

si la función existe.

## Archivo modificado

~~~text
deploy/api/package/main.py
~~~

## Criterio de validación

Este fix queda preparado cuando:

- `main.py` compila.
- `/soporte/tickets` muestra `CENTRAL-2026-0003` para `DASC-2026-004`.
- Los tickets antiguos muestran `Sin central`.
- El detalle de `DASC-2026-004` mantiene los datos de sincronización central.
