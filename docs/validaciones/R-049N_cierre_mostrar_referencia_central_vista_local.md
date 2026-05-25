# R-049N - Cierre mostrar referencia central en la vista local de tickets

## Objetivo

Cerrar la validación de la visualización de la referencia central dentro del panel local de soporte.

## Estado

Cerrada.

## Funcionalidad implementada

R-049N permite que el panel local muestre la relación entre un ticket local y su ticket correspondiente en el panel central DASC.

Campos usados:

~~~text
central_ticket_id
central_sync_status
central_sync_detail
central_sync_at
~~~

## Archivos modificados

~~~text
deploy/api/package/main.py
deploy/api/package/templates/soporte_tickets.html
deploy/api/package/templates/soporte_ticket_detalle.html
~~~

## Documentos relacionados

~~~text
docs/validaciones/R-049N_mostrar_referencia_central_vista_local.md
docs/validaciones/R-049N_FIX_visualizacion_referencia_central.md
docs/validaciones/R-049N_FIX2_listado_referencia_central.md
docs/validaciones/R-049N_FIX3_search_support_tickets_referencia_central.md
docs/validaciones/R-049N_FIX4_return_real_search_support_tickets.md
~~~

## Validación del listado local

Se validó la ruta:

~~~text
/soporte/tickets
~~~

Resultado esperado y confirmado:

~~~text
DASC-2026-004 -> CENTRAL-2026-0003 / sent
DASC-2026-003 -> Sin central
DASC-2026-002 -> Sin central
DASC-2026-001 -> Sin central
~~~

## Validación del detalle local

Se validó la ruta:

~~~text
/soporte/tickets/DASC-2026-004
~~~

En el bloque `Sincronización central` se confirmó:

~~~text
Ticket central: CENTRAL-2026-0003
Estado sincronización: sent
Última sincronización: 2026-05-25 19:16:32
Detalle sincronización: Enviado a central: CENTRAL-2026-0003
~~~

## Problema encontrado durante la implementación

Durante R-049N se detectó que el listado local no usaba una función llamada `list_support_tickets`.

La ruta real `/soporte/tickets` usaba:

~~~text
search_support_tickets()
~~~

Además, el retorno real de la función era:

~~~text
return [support_row_to_dict(row) for row in rows]
~~~

Por eso los primeros fixes no modificaban correctamente el listado.

## Fix efectivo

El fix funcional fue el aplicado en:

~~~text
650f542 fix: aplicar referencia central en busqueda soporte
~~~

Este cambio modifica `search_support_tickets()` para enriquecer los tickets con los datos centrales antes de devolverlos a la plantilla.

## Validación técnica

Se comprobó:

~~~text
main.py compila: OK
dasc-api arranca: OK
/soporte/tickets carga: OK
DASC-2026-004 muestra CENTRAL-2026-0003: OK
DASC-2026-004 muestra sent: OK
Tickets antiguos muestran Sin central: OK
Detalle de DASC-2026-004 muestra sincronización central: OK
SQLite local contiene los datos correctos: OK
~~~

## Resultado

R-049N queda validada correctamente.

El panel local ahora permite ver de forma clara si un ticket fue sincronizado con el panel central DASC.

## Límites actuales

Esta versión todavía no incluye:

- Enlace directo desde el panel local al panel central.
- Sincronización de estado central hacia el panel local.
- Reintentos automáticos.
- Cola offline de tickets pendientes.
- Gestión visual avanzada de errores de sincronización.
- Panel cliente definitivo separado.

## Próxima tarea recomendada

~~~text
R-049O - Cola offline y reintentos de envío central
~~~

También se puede plantear:

~~~text
R-049P - Sincronización de estado central hacia local
R-049Q - Login y roles del panel central
R-049R - Instalador systemd para central-support
~~~

## Conclusión

DASC Server Manager supera R-049N.

El flujo local-central ya tiene trazabilidad técnica y visual: el ticket local muestra su referencia central y el estado de sincronización.
