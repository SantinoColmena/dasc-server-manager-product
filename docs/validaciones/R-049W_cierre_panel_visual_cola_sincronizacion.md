# R-049W - Cierre panel visual de cola y sincronización local-central

## Objetivo

Cerrar la validación del panel visual de cola y sincronización entre el panel local del cliente y el panel central DASC.

## Estado

Cerrada.

## Contexto

Antes de R-049W, la integración local-central ya existía técnicamente:

- Envío de tickets locales al panel central.
- Guardado de central_ticket_id.
- Cola offline cuando la central no responde.
- Reintento manual.
- Reintento automático con systemd timer.
- Sincronización desde central hacia local.

Sin embargo, faltaba una vista visual clara para revisar el estado de esa sincronización desde el panel local técnico.

## Cambios principales

Se añadió una vista técnica interna:

- /soporte/sincronizacion

Esta vista muestra:

- Total de tickets locales.
- Tickets enviados a central.
- Tickets pendientes o con error.
- Tickets con integración central desactivada.
- Tickets sin referencia central.
- Última sincronización.
- Detalle del último intento.
- Ticket central asociado.
- Enlace al detalle local.

## Protección aplicada

La vista de sincronización queda reservada al equipo técnico DASC mediante:

- is_admin(request)
- DASC_LOCAL_INTERNAL_SUPPORT_ENABLED=true

No forma parte de la experiencia normal del cliente.

## Reintento manual

Se añadió el endpoint:

- POST /soporte/sincronizacion/reintentar-central

Este endpoint ejecuta el reintento de tickets pendientes y registra auditoría en logs.

## R-049W-FIX1

Durante la revisión visual se detectó que el enlace Ver del listado técnico llevaba a una vista demasiado interna para un cliente.

Esa vista contenía:

- Actualización de estado y prioridad.
- Resumen para Jira/Zammad.
- Plantillas de respuesta.
- Historial interno.
- Sincronización central.
- Botones técnicos.

Por tanto, se separaron las vistas.

## Vista cliente añadida

Se creó una vista limpia de seguimiento:

- /soporte/estado/{ticket_id}

Esta vista muestra solo:

- ID del ticket.
- Estado actual.
- Prioridad.
- Tipo.
- Progreso visual.
- Datos básicos.
- Descripción enviada.
- Evidencia aportada.
- Seguimiento básico.
- Información para el cliente.

## Vista técnica mantenida

Se mantiene la vista interna:

- /soporte/tickets/{ticket_id}

Esta vista sigue reservada al equipo DASC y permite gestión técnica completa.

## Archivos modificados

- deploy/api/package/main.py
- deploy/api/package/templates/soporte.html
- deploy/api/package/templates/soporte_tickets.html

## Archivos añadidos

- deploy/api/package/templates/soporte_sincronizacion.html
- deploy/api/package/templates/soporte_ticket_estado_cliente.html
- docs/validaciones/R-049W_panel_visual_cola_sincronizacion.md
- docs/validaciones/R-049W_FIX1_vista_cliente_estado_ticket.md

## Commits relacionados

- c07011f feat: añadir panel visual sincronizacion soporte
- c40d5ea fix: separar vista cliente de ticket soporte

## Validación técnica

Se validó en lab-pruebas:

- Repo actualizado a c40d5ea.
- main.py R-049W compila.
- main.py R-049W-FIX1 compila.
- Archivos copiados a /opt/dasc/api.
- dasc-api reinicia correctamente.
- dasc-api queda activo.
- Ruta /soporte/sincronizacion instalada.
- Ruta /soporte/estado/{ticket_id} instalada.
- Timer dasc-central-retry sigue activo.

## Validación de sincronización

Se validó en SQLite local:

- 6 tickets locales.
- 3 enviados a central.
- 3 sin central.
- 0 pendientes/error.
- 0 desactivados.

La vista /soporte/sincronizacion muestra correctamente estos contadores.

## Validación de vista cliente

Se validó visualmente:

- /soporte/estado/DASC-2026-006 carga correctamente.
- Muestra el estado actual del ticket.
- Muestra datos básicos de la solicitud.
- Muestra descripción y evidencia.
- Muestra seguimiento básico.
- No muestra herramientas internas.

## Validación de separación de vistas

Vista cliente:

- /soporte/estado/DASC-2026-006

Vista interna:

- /soporte/tickets/DASC-2026-006

Resultado:

- La vista cliente queda limpia.
- La vista interna conserva gestión técnica.

## Validación de elementos no visibles en cliente

Se comprobó que la vista cliente no muestra:

- Resumen para Jira/Zammad.
- Plantillas de respuesta.
- Sincronización central.
- Guardar cambios.
- Diagnóstico técnico.

## Resultado

R-049W queda validada correctamente.

El panel local ahora tiene una vista técnica de sincronización para el equipo DASC y una vista limpia de seguimiento para cliente.

## Límites actuales

Esta tarea no implementa todavía:

- Comentarios bidireccionales cliente-DASC.
- Adjuntos reales por ticket.
- Portal público por código y email.
- Historial visible completo para cliente.
- Notificaciones automáticas por email.
- SLA visual.
- Exportación CSV.

## Conclusión

DASC Server Manager supera R-049W.

La integración local-central queda más observable para el equipo técnico y más limpia para el cliente.
