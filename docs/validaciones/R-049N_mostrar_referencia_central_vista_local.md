# R-049N - Mostrar referencia central en la vista local de tickets

## Objetivo

Mostrar en el panel local la referencia del ticket central asociado a cada ticket de soporte.

## Estado

En curso.

## Contexto

R-049M guardó en SQLite local la relación entre el ticket local y el ticket central mediante:

~~~text
central_ticket_id
central_sync_status
central_sync_detail
central_sync_at
~~~

R-049N hace visible esa información en la interfaz local.

## Archivos modificados

~~~text
deploy/api/package/main.py
deploy/api/package/templates/soporte_tickets.html
deploy/api/package/templates/soporte_ticket_detalle.html
~~~

## Vista de listado

En la vista local de tickets se añade la columna:

~~~text
CENTRAL
~~~

Debe verse, cuando exista:

~~~text
CENTRAL-2026-0003
sent
~~~

Si no existe referencia central:

~~~text
Sin central
~~~

## Vista de detalle

En el detalle del ticket local se añade el bloque:

~~~text
Sincronización central
~~~

Con los campos:

~~~text
Ticket central
Estado sincronización
Última sincronización
Detalle sincronización
~~~

## Criterio de validación

R-049N se considera preparada cuando:

- `main.py` compila.
- `dasc-api` arranca.
- `/soporte/tickets` carga correctamente.
- El ticket `DASC-2026-004` muestra `CENTRAL-2026-0003`.
- El detalle de `DASC-2026-004` muestra bloque de sincronización central.
- Tickets antiguos sin referencia central muestran `Sin central` o equivalente.
- No se rompe la creación de tickets.
- No se rompe el envío a la API central.

## Límites

Esta tarea todavía no incluye:

- Enlace directo desde panel local al panel central.
- Sincronización de estado central hacia local.
- Reintentos automáticos.
- Cola offline.
- Gestión visual avanzada de errores.

## Próximo paso

Validar en `lab-pruebas`.

## Conclusión

R-049N mejora la trazabilidad visual entre el panel local del cliente y el panel central DASC.
