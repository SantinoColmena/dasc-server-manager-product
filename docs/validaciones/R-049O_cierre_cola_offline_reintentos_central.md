# R-049O - Cierre cola offline y reintentos de envío central

## Objetivo

Cerrar la validación de la cola offline y el reintento manual de envío de tickets desde el panel local hacia el panel central DASC.

## Estado

Cerrada.

## Funcionalidad implementada

R-049O permite que un ticket local no se pierda aunque el panel central DASC esté caído en el momento de creación.

Flujo validado:

~~~text
Panel central apagado
        ↓
Creación de ticket local
        ↓
Error de envío central registrado
        ↓
Ticket local queda pendiente
        ↓
Panel central vuelve a estar disponible
        ↓
Botón de reintento desde /soporte/tickets
        ↓
Ticket enviado correctamente al panel central
        ↓
Ticket local actualizado como sent
~~~

## Archivos modificados

~~~text
deploy/api/package/main.py
deploy/api/package/templates/soporte_tickets.html
~~~

## Documentos relacionados

~~~text
docs/validaciones/R-049O_cola_offline_reintentos_central.md
docs/validaciones/R-049O_FIX1_contador_pendientes.md
~~~

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

## Fix aplicado antes de validar

Durante la implementación se detectó que:

~~~text
central_pending_count
~~~

no se estaba pasando correctamente al template.

También se corrigió el filtro para que solo se consideren pendientes los tickets con:

~~~text
central_sync_status = error
~~~

Esto evita que tickets antiguos creados antes de R-049M aparezcan como pendientes.

## Validación inicial

Antes de simular la caída del panel central se comprobó que no había pendientes antiguos:

~~~text
OK: no hay pendientes antiguos
~~~

## Simulación de caída central

Se apagó el panel central en el puerto:

~~~text
8010
~~~

La comprobación devolvió:

~~~text
central-support no responde
~~~

## Ticket creado con central apagado

Se creó el ticket local:

~~~text
DASC-2026-005
~~~

Datos principales:

~~~text
Cliente: Cliente Demo Offline
Tipo: Incidencia
Prioridad: Alta
Servicio: API / Panel
Contacto: Responsable IT Offline
Email: soporte-offline-demo@dasc.local
~~~

## Estado local tras fallo central

El ticket quedó correctamente en error:

~~~text
id: DASC-2026-005
central_ticket_id: vacío
central_sync_status: error
central_sync_detail: <urlopen error [Errno 111] Connection refused>
central_sync_at: 2026-05-26 11:37:00
~~~

## Reintento validado

Tras levantar de nuevo el panel central, se pulsó el botón:

~~~text
Reintentar envío central pendiente (1)
~~~

El resultado local fue:

~~~text
id: DASC-2026-005
central_ticket_id: CENTRAL-2026-0001
central_sync_status: sent
central_sync_detail: Reintento enviado a central: CENTRAL-2026-0001
central_sync_at: 2026-05-26 11:43:30
~~~

## Ticket creado en panel central

El panel central creó correctamente:

~~~text
CENTRAL-2026-0001
~~~

Asociado al ticket local:

~~~text
ticket_local_id: DASC-2026-005
cliente: Cliente Demo Offline
estado: Nuevo
prioridad: Alta
servicio: API / Panel
~~~

## Nota sobre numeración central

Durante la validación se recreó el entorno central en `/tmp/dasc-server-manager-product`.

Por ese motivo, la base central usada en la prueba estaba limpia y el ticket central generado fue:

~~~text
CENTRAL-2026-0001
~~~

Esto no representa un error.

Lo importante validado es la sincronización local-central después del reintento.

## Validación de logs

En `dasc_logs.eventos` se confirmó el fallo inicial:

~~~text
POST /soporte central DASC-2026-005
ERROR
<urlopen error [Errno 111] Connection refused>
~~~

También se confirmó la creación local:

~~~text
POST /soporte DASC-2026-005
OK
Ticket de soporte creado: Incidencia / Alta / API / Panel
~~~

Y se confirmó el reintento:

~~~text
POST /soporte/tickets/reintentar-central
OK
Reintentos central: total=1, enviados=1, errores=0
~~~

## Validación técnica

Se comprobó:

~~~text
main.py R-049O compila: OK
main.py instalado compila: OK
dasc-api activo: OK
HTTP 303 hacia /login: OK
central-support apagado para prueba: OK
ticket local creado con central caído: OK
central_sync_status=error: OK
botón de reintento visible: OK
central-support levantado de nuevo: OK
health central: OK
reintento ejecutado: OK
central_sync_status=sent: OK
central_ticket_id guardado: OK
ticket creado en central: OK
logs registrados en MariaDB: OK
~~~

## Resultado

R-049O queda validada correctamente.

El sistema ya soporta caída temporal del panel central sin perder tickets locales.

## Límites actuales

Esta versión todavía no incluye:

- Reintento automático programado.
- Cola avanzada con número de intentos.
- Backoff progresivo.
- Fecha del último intento separada de `central_sync_at`.
- Sincronización de estado central hacia local.
- Alertas automáticas por fallo prolongado.
- Gestión visual avanzada de errores de sincronización.

## Próxima tarea recomendada

~~~text
R-049P - Sincronización de estado central hacia panel local
~~~

También queda pendiente:

~~~text
R-049Q - Login y roles del panel central
R-049R - Instalador systemd para central-support
R-049S - Reintento automático mediante systemd timer
~~~

## Conclusión

DASC Server Manager supera R-049O.

El soporte local-central ya es resiliente: si el panel central falla, el ticket queda guardado localmente, marcado como error y puede reenviarse después sin perder trazabilidad.
