# R-049O - Cola offline y reintentos de envío central

## Objetivo

Permitir que los tickets locales que no pudieron enviarse al panel central puedan reintentarse posteriormente sin perderse.

## Estado

Cerrada.

## Contexto

R-049L permitió enviar tickets desde el panel local hacia la API central.

R-049M guardó `central_ticket_id` y estado de sincronización en SQLite local.

R-049N mostró esa referencia central en la interfaz local.

R-049O añade recuperación ante fallo del panel central.

## Archivos modificados

~~~text
deploy/api/package/main.py
deploy/api/package/templates/soporte_tickets.html
~~~

## Funcionamiento

Si la API central falla al crear un ticket:

~~~text
El ticket local se crea igualmente.
central_ticket_id queda vacío.
central_sync_status queda en error.
central_sync_detail guarda el error.
~~~

Después, desde `/soporte/tickets`, el equipo técnico puede pulsar un botón para reintentar el envío.

## Ruta añadida

~~~text
POST /soporte/tickets/reintentar-central
~~~

## Funciones añadidas

~~~text
get_pending_central_sync_tickets
retry_support_ticket_to_central
retry_pending_central_sync_tickets
soporte_retry_central_pending
~~~

## Criterio de validación

R-049O se considera preparada cuando:

- `main.py` compila.
- `dasc-api` arranca.
- Se crea un ticket local con el panel central parado.
- El ticket local queda con `central_sync_status=error`.
- El ticket aparece como pendiente de sincronización.
- Al arrancar de nuevo el panel central, el botón de reintento envía el ticket.
- El ticket recibe un `central_ticket_id`.
- El estado local cambia a `sent`.
- Los logs registran el reintento.

## Límites

Esta tarea todavía no incluye:

- Reintento automático programado por cron/systemd timer.
- Cola avanzada con número de intentos.
- Backoff progresivo.
- Sincronización de estado central hacia local.
- Alertas automáticas por fallo prolongado.

## Próximo paso

Validar en `lab-pruebas`.

## Conclusión

R-049O mejora la resiliencia del sistema: el panel local no depende de que el panel central esté disponible en el momento exacto de crear el ticket.
