# R-049P - Cierre sincronización de estado central hacia panel local

## Objetivo

Cerrar la validación de la sincronización de estado y prioridad desde el panel central DASC hacia el panel local del cliente.

## Estado

Cerrada.

## Funcionalidad implementada

R-049P permite que un ticket local sincronizado con el panel central pueda actualizar su estado y prioridad consultando el ticket central asociado.

Flujo validado:

~~~text
Panel central DASC
        ↓
Cambio de estado/prioridad del ticket central
        ↓
Endpoint GET /api/v1/support/tickets/{ticket_id}
        ↓
Panel local consulta el ticket central
        ↓
Botón "Sincronizar estado desde central"
        ↓
Ticket local actualiza estado y prioridad
        ↓
Historial local y logs registran la sincronización
~~~

## Archivos modificados

~~~text
deploy/central-support/package/main.py
deploy/api/package/main.py
deploy/api/package/templates/soporte_ticket_detalle.html
~~~

## Documento de validación

~~~text
docs/validaciones/R-049P_sincronizacion_estado_central_local.md
~~~

## Endpoint central validado

Se validó el endpoint:

~~~text
GET /api/v1/support/tickets/CENTRAL-2026-0001
~~~

Con cabeceras:

~~~text
X-DASC-Client-ID: cliente-demo-a
X-DASC-Client-Token: dasc-central-demo-token-lab
~~~

Respuesta validada:

~~~text
ok: true
id: CENTRAL-2026-0001
ticket_local_id: DASC-2026-005
estado: Nuevo
prioridad: Alta
~~~

## Cambio en panel central

El ticket central usado fue:

~~~text
CENTRAL-2026-0001
~~~

Asociado al ticket local:

~~~text
DASC-2026-005
~~~

Se actualizó el ticket central a:

~~~text
Estado: En curso
Prioridad: Media
~~~

## Sincronización desde panel local

En el detalle local del ticket:

~~~text
/soporte/tickets/DASC-2026-005
~~~

se validó el botón:

~~~text
Sincronizar estado desde central
~~~

Tras pulsarlo, el panel local actualizó correctamente el ticket.

## Resultado local validado

El ticket local quedó así:

~~~text
id: DASC-2026-005
estado: En curso
prioridad: Media
central_ticket_id: CENTRAL-2026-0001
central_sync_status: sent
central_sync_detail: Sincronizado desde central CENTRAL-2026-0001: estado central=En curso, estado local=En curso, prioridad=Media
central_sync_at: 2026-05-26 11:52:31
fecha_actualizacion: 2026-05-26 11:52:31
~~~

## Historial local validado

El historial local registró:

~~~text
Cambio de prioridad
Alta -> Media

Cambio de estado
Abierto -> En curso
~~~

Usuario:

~~~text
admin
~~~

## Resultado central validado

El ticket central quedó así:

~~~text
id: CENTRAL-2026-0001
ticket_local_id: DASC-2026-005
estado: En curso
prioridad: Media
fecha_actualizacion: 2026-05-26 11:51:41
~~~

## Validación de logs

En `dasc_logs.eventos` se confirmó:

~~~text
POST /soporte/tickets/DASC-2026-005/sync-central
OK
Sincronizado desde central CENTRAL-2026-0001: estado central=En curso, estado local=En curso, prioridad=Media
~~~

También se registró el acceso posterior:

~~~text
GET /soporte/tickets/DASC-2026-005
OK
HTTP 200
~~~

## Nota sobre "Sin cambios"

Durante la prueba, el `curl` contra el panel central devolvió:

~~~text
msg=Sin cambios
~~~

Esto no representa un error.

Significa que el ticket central ya estaba en:

~~~text
Estado: En curso
Prioridad: Media
~~~

cuando se ejecutó de nuevo el comando.

La sincronización local posterior confirmó correctamente esos valores.

## Validación técnica

Se comprobó:

~~~text
main.py central R-049P compila: OK
central-support arranca: OK
health central: OK
main.py local R-049P compila: OK
main.py instalado R-049P compila: OK
dasc-api activo: OK
endpoint central GET funciona: OK
botón local sync-central visible: OK
sincronización central -> local ejecutada: OK
historial local actualizado: OK
logs MariaDB registrados: OK
~~~

## Resultado

R-049P queda validada correctamente.

El flujo de soporte local-central ya permite:

~~~text
1. Crear ticket local.
2. Enviarlo al panel central.
3. Reintentarlo si el panel central estaba caído.
4. Gestionar estado/prioridad en el panel central.
5. Reflejar estado/prioridad en el panel local.
~~~

## Límites actuales

Esta versión todavía no incluye:

- Sincronización automática programada.
- Webhooks desde el panel central.
- Sincronización de comentarios.
- Sincronización completa del historial central.
- Resolución avanzada de conflictos local-central.
- Login y roles reales en el panel central.
- Instalador systemd definitivo para central-support.

## Próxima tarea recomendada

~~~text
R-049Q - Login y roles del panel central
~~~

También queda pendiente:

~~~text
R-049R - Instalador systemd para central-support
R-049S - Reintento automático mediante systemd timer
R-049T - Mejoras visuales del panel central
~~~

## Conclusión

DASC Server Manager supera R-049P.

El panel local ya puede recibir el estado operativo gestionado desde el panel central DASC, manteniendo trazabilidad local, historial y logs de auditoría.
