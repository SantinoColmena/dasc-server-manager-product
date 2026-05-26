# R-049W-FIX1 - Separar vista cliente y vista técnica de ticket

## Objetivo

Separar la experiencia del cliente de la vista técnica interna del equipo DASC.

## Estado

Cerrada.

## Problema detectado

Tras R-049W, el listado técnico interno de tickets enlaza a la vista:

- /soporte/tickets/{ticket_id}

Esa vista está pensada para el equipo DASC y contiene elementos que no debe ver un cliente normal:

- Actualizar estado y prioridad.
- Resumen para Jira/Zammad.
- Plantillas de respuesta.
- Historial interno.
- Sincronización central.
- Botón para sincronizar desde central.
- Detalles técnicos de central_sync.

## Decisión aplicada

Se crea una vista limpia de seguimiento para cliente:

- /soporte/estado/{ticket_id}

Esta vista es solo lectura y muestra:

- Estado actual.
- Prioridad.
- Tipo.
- Servicio afectado.
- Fecha de apertura.
- Última actualización.
- Datos básicos de la solicitud.
- Descripción enviada.
- Evidencia aportada.
- Seguimiento básico.

## Vista interna mantenida

Se mantiene la vista técnica interna:

- /soporte/tickets/{ticket_id}

Esta vista sigue reservada al equipo DASC y permite:

- Gestión de estado y prioridad.
- Plantillas.
- Resumen externo.
- Historial interno.
- Sincronización central.
- Diagnóstico técnico.

## Archivos modificados

- deploy/api/package/main.py
- deploy/api/package/templates/soporte.html

## Archivos añadidos

- deploy/api/package/templates/soporte_ticket_estado_cliente.html
- docs/validaciones/R-049W_FIX1_vista_cliente_estado_ticket.md

## Criterio de validación

R-049W-FIX1 se considera preparado cuando:

- main.py compila.
- dasc-api reinicia correctamente.
- /soporte sigue funcionando.
- Al crear un ticket aparece enlace Ver estado.
- /soporte/estado/{ticket_id} carga una vista limpia.
- La vista cliente no muestra botones técnicos.
- La vista cliente no muestra resumen Jira/Zammad.
- La vista cliente no muestra plantillas.
- La vista cliente no muestra sincronización central.
- La vista interna /soporte/tickets/{ticket_id} sigue funcionando para admin.

## Resultado esperado

El cliente puede consultar el estado de su ticket sin entrar en herramientas internas del equipo DASC.
