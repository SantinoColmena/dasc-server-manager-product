# R-049O-FIX1 - Corregir contador de pendientes y filtro de cola offline

## Objetivo

Corregir la primera implementación de R-049O antes de validarla en laboratorio.

## Estado

En curso.

## Problemas detectados

Durante la implementación inicial de R-049O se detectó:

~~~text
No se encontró bloque context counts en soporte_tickets_page.
~~~

Por ese motivo podía no pasarse `central_pending_count` al template `soporte_tickets.html`.

También se detectó que la consulta de pendientes incluía tickets con `central_sync_status` vacío, lo que podía marcar como pendientes tickets antiguos creados antes de R-049M.

## Solución aplicada

Se modifica el filtro de pendientes para contar solo tickets con:

~~~text
central_sync_status = error
~~~

También se añade:

~~~text
context["central_pending_count"]
~~~

antes de renderizar:

~~~text
soporte_tickets.html
~~~

## Archivo modificado

~~~text
deploy/api/package/main.py
~~~

## Criterio de validación

Este fix queda preparado cuando:

- `main.py` compila.
- `/soporte/tickets` carga.
- Los tickets antiguos sin central no aparecen como pendientes.
- Si se crea un ticket con el panel central caído, aparece el botón de reintento.
