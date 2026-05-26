# R-049P - Sincronización de estado central hacia panel local

## Objetivo

Permitir que el panel local actualice el estado y la prioridad de un ticket local consultando su ticket asociado en el panel central DASC.

## Estado

Cerrada.

## Contexto

R-049L permitió enviar tickets locales al panel central.

R-049M guardó `central_ticket_id` en SQLite local.

R-049N mostró la referencia central en la interfaz local.

R-049O añadió cola offline y reintentos.

R-049P añade sincronización inversa: central -> local.

## Archivos modificados

~~~text
deploy/central-support/package/main.py
deploy/api/package/main.py
deploy/api/package/templates/soporte_ticket_detalle.html
~~~

## Endpoint central añadido

~~~text
GET /api/v1/support/tickets/{ticket_id}
~~~

Este endpoint devuelve:

~~~text
id
cliente_id
ticket_local_id
estado
prioridad
servicio
fecha_recepcion
fecha_actualizacion
~~~

## Seguridad

La consulta exige:

~~~text
X-DASC-Client-ID
X-DASC-Client-Token
~~~

El endpoint valida que el ticket pertenece al cliente indicado y que el token coincide.

## Ruta local añadida

~~~text
POST /soporte/tickets/{ticket_id}/sync-central
~~~

## Funciones locales añadidas

~~~text
get_central_ticket_status_url
fetch_central_ticket_status
map_central_status_to_local
sync_support_ticket_from_central
soporte_ticket_sync_central_status
~~~

## Mapeo de estados

El estado central:

~~~text
Nuevo
~~~

se convierte en el estado local:

~~~text
Abierto
~~~

El resto de estados se mantienen si existen también en el panel local.

## Vista local

En el detalle del ticket local se añade un botón:

~~~text
Sincronizar estado desde central
~~~

Solo aparece si el ticket tiene `central_ticket_id`.

## Criterio de validación

R-049P se considera preparada cuando:

- `main.py` central compila.
- `main.py` local compila.
- `central-support` arranca.
- `dasc-api` arranca.
- El endpoint central devuelve JSON para un ticket existente.
- Se cambia estado/prioridad en el panel central.
- Se pulsa el botón de sincronización desde el detalle local.
- El ticket local actualiza estado y prioridad.
- El historial local registra el cambio.
- Los logs MariaDB registran la sincronización.

## Caso de prueba recomendado

Usar el ticket local:

~~~text
DASC-2026-005
~~~

Asociado en laboratorio al ticket central:

~~~text
CENTRAL-2026-0001
~~~

## Límites

Esta tarea todavía no incluye:

- Sincronización automática programada.
- Webhooks desde central.
- Resolución de conflictos si local y central cambian a la vez.
- Sincronización de comentarios.
- Sincronización de historial completo.

## Próximo paso

Validar en `lab-pruebas`.

## Conclusión

R-049P prepara el flujo completo de gestión centralizada: el equipo DASC puede cambiar el estado en el panel central y reflejarlo después en el panel local.
