# R-049W - Panel visual de cola y sincronización local-central

## Objetivo

Crear una vista técnica interna para revisar el estado de sincronización entre el panel local del cliente y el panel central DASC.

## Estado

En curso.

## Contexto

Antes de R-049W ya existían:

- Envío de tickets locales al panel central.
- Guardado de central_ticket_id.
- Cola offline cuando la central no responde.
- Reintento manual.
- Reintento automático con systemd timer.
- Sincronización del estado central hacia el ticket local.

Sin embargo, la información estaba repartida entre listado, detalle, logs y base de datos.

## Decisión aplicada

Se añade una vista técnica interna:

- /soporte/sincronizacion

Esta vista queda protegida por:

- is_admin(request)
- DASC_LOCAL_INTERNAL_SUPPORT_ENABLED=true

Por tanto, no es visible para el cliente normal.

## Funcionalidad añadida

La nueva vista muestra:

- Total de tickets locales.
- Tickets enviados a central.
- Tickets pendientes o con error.
- Tickets con integración central desactivada.
- Tickets sin referencia central.
- Última sincronización.
- Detalle del último intento.
- Ticket central asociado.
- Enlace al detalle local.

## Reintento manual

La vista permite reintentar tickets pendientes mediante:

- POST /soporte/sincronizacion/reintentar-central

Este endpoint ejecuta:

- retry_pending_central_sync_tickets(limit=50)

y registra auditoría en logs.

## Archivos modificados

- deploy/api/package/main.py
- deploy/api/package/templates/soporte_tickets.html

## Archivos añadidos

- deploy/api/package/templates/soporte_sincronizacion.html
- docs/validaciones/R-049W_panel_visual_cola_sincronizacion.md

## Criterio de validación

R-049W se considera preparada cuando:

- main.py compila.
- dasc-api reinicia correctamente.
- /soporte sigue funcionando como vista cliente.
- /soporte/sincronizacion redirige si DASC_LOCAL_INTERNAL_SUPPORT_ENABLED=false.
- Al activar DASC_LOCAL_INTERNAL_SUPPORT_ENABLED=true, /soporte/sincronizacion carga.
- Se muestran métricas de sincronización.
- Se listan tickets con estado central.
- El botón de reintento funciona si hay pendientes.
- El listado interno /soporte/tickets enlaza a la nueva vista.
- El timer R-049S sigue activo.

## Límites

Esta tarea no expone la vista al cliente.

Tampoco añade todavía:

- Contador de intentos.
- Backoff progresivo.
- Columna de siguiente reintento.
- Historial detallado por intento.
- Filtro por fechas.
- Exportación CSV.

## Conclusión

R-049W mejora la observabilidad técnica de la integración local-central sin mezclarla con la experiencia normal del cliente.
