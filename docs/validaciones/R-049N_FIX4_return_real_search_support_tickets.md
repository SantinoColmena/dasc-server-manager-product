# R-049N-FIX4 - Corregir listado local con return real de search_support_tickets

## Objetivo

Aplicar el fix real al listado `/soporte/tickets` para que muestre la referencia central del ticket local.

## Estado

En curso.

## Problema

Los fixes anteriores buscaban este retorno:

~~~text
return [dict(row) for row in rows]
~~~

Pero la función real usa:

~~~text
return [support_row_to_dict(row) for row in rows]
~~~

Por eso no se modificaba `main.py`.

## Solución aplicada

Se modifica `search_support_tickets()` para convertir los registros con `support_row_to_dict(row)`, enriquecerlos con la información central y devolverlos a la plantilla.

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
- El detalle de `DASC-2026-004` mantiene la sincronización central.
