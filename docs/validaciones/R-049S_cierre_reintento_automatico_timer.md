# R-049S - Cierre reintento automático mediante systemd timer

## Objetivo

Cerrar la validación del reintento automático de tickets locales pendientes hacia el panel central DASC mediante systemd timer.

## Estado

Cerrada.

## Funcionalidad implementada

R-049S automatiza el reintento de envío de tickets locales que quedaron pendientes por fallo temporal del panel central.

Hasta R-049O, el reintento podía hacerse manualmente desde la vista /soporte/tickets mediante el botón "Reintentar envío central pendiente".

Con R-049S, esa misma lógica se ejecuta de forma automática mediante systemd.

## Archivos añadidos

- deploy/api/package/scripts/retry_central_pending.py
- deploy/api/install_central_retry_timer.sh
- deploy/api/uninstall_central_retry_timer.sh
- docs/validaciones/R-049S_reintento_automatico_timer.md

## Servicio systemd creado

Servicio:

- dasc-central-retry.service

Tipo:

- oneshot

## Timer systemd creado

Timer:

- dasc-central-retry.timer

Estado validado:

- enabled
- active

## Script instalado

El instalador copió el script en:

- /opt/dasc/api/scripts/retry_central_pending.py

Validación:

- retry_central_pending.py compila correctamente

## Función ejecutada

El script importa main.py del panel local y ejecuta:

- retry_pending_central_sync_tickets(limit=50)

Después registra auditoría con:

- log_event()

Usuario usado en auditoría:

- systemd-timer

## Validación sin pendientes

Se ejecutó manualmente:

- sudo systemctl start dasc-central-retry.service

Resultado:

- Reintento automatico central: total=0, enviados=0, errores=0, omitidos=0

Esto confirma que el servicio oneshot funciona aunque no haya tickets pendientes.

## Simulación de fallo central

Se detuvo el panel central:

- sudo systemctl stop dasc-central-support

La comprobación confirmó:

- central-support no responde

## Ticket pendiente creado

Se creó el ticket local:

- DASC-2026-006

Datos principales:

- Cliente: Cliente Demo Timer
- Contacto: Responsable IT Timer
- Email: timer-demo@dasc.local
- Tipo: Incidencia
- Prioridad: Crítica
- Servicio: API / Panel

Estado inicial validado:

- central_ticket_id: vacío
- central_sync_status: error
- central_sync_detail: urlopen error Errno 111 Connection refused
- central_sync_at: 2026-05-26 13:32:59

## Reintento automático validado

Se levantó de nuevo el panel central:

- sudo systemctl start dasc-central-support

Después se ejecutó:

- sudo systemctl start dasc-central-retry.service

Resultado del servicio:

- Reintento automatico central: total=1, enviados=1, errores=0, omitidos=0

Detalle registrado por el servicio:

- ticket_id: DASC-2026-006
- central_ticket_id: CENTRAL-2026-0003
- status: sent
- detail: Reintento enviado a central: CENTRAL-2026-0003

## Resultado local validado

El ticket local quedó así:

- id: DASC-2026-006
- cliente: Cliente Demo Timer
- central_ticket_id: CENTRAL-2026-0003
- central_sync_status: sent
- central_sync_detail: Reintento enviado a central: CENTRAL-2026-0003
- central_sync_at: 2026-05-26 13:35:41

## Resultado central validado

En la base central systemd se creó:

- CENTRAL-2026-0003

Asociado a:

- ticket_local_id: DASC-2026-006
- cliente: Cliente Demo Timer
- tipo: Incidencia
- prioridad: Crítica
- servicio: API / Panel
- estado: Nuevo
- contacto: Responsable IT Timer
- email: timer-demo@dasc.local
- fecha_recepcion: 2026-05-26 13:35:41

## Validación de logs MariaDB

En dasc_logs.eventos se confirmó:

- usuario: systemd-timer
- recurso: SYSTEMD TIMER /soporte/tickets/reintentar-central
- resultado: OK
- detalle: Reintento automatico central: total=1, enviados=1, errores=0, omitidos=0

También se validaron ejecuciones anteriores sin pendientes:

- Reintento automatico central: total=0, enviados=0, errores=0, omitidos=0

## Validación técnica

Se comprobó:

- Repo estable usado en /home/santino/dasc-server-manager-product: OK
- Timer instalado: OK
- Timer enabled: OK
- Timer active: OK
- Servicio oneshot creado: OK
- Script instalado: OK
- Script compila: OK
- Ejecución sin pendientes: OK
- Creación de pendiente con central caído: OK
- Reintento automático tras levantar central: OK
- Actualización local a sent: OK
- Creación de ticket central: OK
- Auditoría MariaDB con systemd-timer: OK

## Resultado

R-049S queda validada correctamente.

El sistema ya no depende únicamente de que un técnico pulse manualmente el botón de reintento.

## Límites actuales

Esta versión todavía no incluye:

- Backoff progresivo.
- Número máximo de intentos por ticket.
- Campo separado para último intento automático.
- Contador de intentos.
- Panel visual específico de cola automática.
- Alertas por fallo prolongado del panel central.
- Control avanzado de duplicados si se modifican datos manualmente.

## Próxima tarea recomendada

R-049T - Mejoras visuales del panel central

También queda pendiente:

- R-049U - Endurecimiento de credenciales del panel central
- R-049V - Reverse proxy Nginx para central-support
- R-049W - Panel visual de cola/sincronización

## Conclusión

DASC Server Manager supera R-049S.

La integración local-central ya tiene cola offline, reintento manual y reintento automático mediante systemd timer, manteniendo trazabilidad en SQLite local, panel central y MariaDB de auditoría.
