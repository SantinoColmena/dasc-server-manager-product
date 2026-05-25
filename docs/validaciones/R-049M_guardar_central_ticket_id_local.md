# R-049M - Guardar central_ticket_id en el ticket local

## Objetivo

Guardar en la base SQLite local la relación entre un ticket creado en el panel local y su ticket correspondiente en el panel central DASC.

## Estado

En curso.

## Contexto

R-049L validó que un ticket creado en `/soporte` se envía correctamente a la API central.

El ticket local creado fue:

~~~text
DASC-2026-003
~~~

Y el ticket central correspondiente fue:

~~~text
CENTRAL-2026-0002
~~~

Hasta ahora esa relación no quedaba guardada de forma persistente dentro del ticket local.

## Archivo modificado

~~~text
deploy/api/package/main.py
~~~

## Columnas añadidas a SQLite local

Se añaden dinámicamente a la tabla local `support_tickets`:

~~~text
central_ticket_id
central_sync_status
central_sync_detail
central_sync_at
~~~

## Estados de sincronización

~~~text
sent
disabled
error
~~~

## Funcionamiento

Cuando se crea un ticket local:

~~~text
1. Se guarda el ticket en SQLite local.
2. Se intenta enviar a la API central.
3. Se obtiene el central_ticket_id si el envío funciona.
4. Se actualiza el ticket local con la información central.
5. Se registra el resultado en logs.
~~~

## Comportamiento esperado

Si el envío central funciona:

~~~text
central_ticket_id = CENTRAL-2026-XXXX
central_sync_status = sent
~~~

Si la integración está desactivada:

~~~text
central_ticket_id = vacío
central_sync_status = disabled
~~~

Si falla la API central:

~~~text
central_ticket_id = vacío
central_sync_status = error
~~~

## Seguridad

La creación local sigue siendo prioritaria.

Si la API central falla, el ticket local no se pierde.

## Criterio de validación

R-049M se considera preparada cuando:

- `main.py` compila.
- `dasc-api` arranca.
- Se crea un nuevo ticket desde `/soporte`.
- El ticket aparece en SQLite local.
- El ticket aparece en SQLite central.
- El ticket local guarda `central_ticket_id`.
- El ticket local guarda `central_sync_status=sent`.
- El ticket local guarda detalle del envío.
- Los logs siguen registrando el envío central.

## Límites

Esta tarea todavía no incluye:

- Mostrar central_ticket_id en la interfaz local.
- Reintentos automáticos.
- Cola offline.
- Sincronización de estado central hacia local.
- Búsqueda cruzada local-central.
- Panel cliente definitivo separado.

## Próximo paso

Validar en `lab-pruebas`.

## Conclusión

R-049M mejora la trazabilidad entre el panel local del cliente y el panel central DASC.
