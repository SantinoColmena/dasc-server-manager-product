# R-049L - Cierre envío de tickets desde panel local hacia API central

## Objetivo

Cerrar la validación de la conexión entre el panel local del cliente y la API central DASC.

## Estado

Cerrada.

## Funcionalidad implementada

R-049L permite que un ticket creado en el panel local se envíe automáticamente al panel central DASC.

Flujo validado:

~~~text
Panel local /soporte
        ↓
SQLite local support_tickets.db
        ↓
POST /api/v1/support/tickets
        ↓
API central DASC
        ↓
SQLite central central_support.db
        ↓
Dashboard central
~~~

## Archivos modificados

~~~text
deploy/api/package/main.py
~~~

## Documento de validación

~~~text
docs/validaciones/R-049L_envio_panel_local_api_central.md
~~~

## Variables usadas en laboratorio

~~~text
CENTRAL_SUPPORT_ENABLED=true
CENTRAL_SUPPORT_URL=http://127.0.0.1:8010/api/v1/support/tickets
CENTRAL_SUPPORT_CLIENT_ID=cliente-demo-a
CENTRAL_SUPPORT_CLIENT_NAME=Cliente Demo A
CENTRAL_SUPPORT_TOKEN=dasc-central-demo-token-lab
CENTRAL_SUPPORT_TIMEOUT=5
~~~

## Ticket local creado

Se creó correctamente el ticket local:

~~~text
DASC-2026-003
~~~

Datos principales:

~~~text
Cliente: Cliente Demo A
Tipo: Incidencia
Prioridad local: Media
Servicio: API / Panel
Contacto: Responsable IT Central
Email: soporte-central-demo@dasc.local
~~~

## Ticket central creado

El panel central recibió correctamente el ticket:

~~~text
CENTRAL-2026-0002
~~~

Datos principales:

~~~text
cliente_id: cliente-demo-a
nombre_cliente: Cliente Demo A
ticket_local_id: DASC-2026-003
tipo: Incidencia
prioridad: Media
estado: Nuevo
servicio: API / Panel
contacto: Responsable IT Central
email: soporte-central-demo@dasc.local
~~~

## Validación visual

El panel central mostró:

~~~text
Total tickets: 2
CENTRAL-2026-0002
DASC-2026-003
Incidencia
Media
Nuevo
API / Panel
Responsable IT Central
~~~

## Validación de logs

En la base `dasc_logs`, tabla `eventos`, se registró:

~~~text
POST /soporte central DASC-2026-003
OK
Enviado a central: CENTRAL-2026-0002
~~~

También se registró el evento local:

~~~text
POST /soporte DASC-2026-003
OK
Ticket de soporte creado: Incidencia / Media / API / Panel
~~~

## Resultado

R-049L queda validada correctamente.

El panel local ya puede enviar tickets al panel central DASC sin depender de Jira, Zammad ni herramientas externas de pago.

## Comportamiento seguro

La creación local se mantiene como fuente segura inicial.

Si el panel central falla, el ticket local no debe perderse.

Este comportamiento queda documentado como requisito de continuidad.

## Límites actuales

Esta versión todavía no incluye:

- Guardar `central_ticket_id` dentro del SQLite local.
- Reintentos automáticos si la API central está caída.
- Cola offline de tickets pendientes.
- Sincronización de estado central hacia panel local.
- Login real del panel central.
- Roles reales del panel central.
- HTTPS real.
- Servicio systemd para central-support.
- Tokens rotables desde interfaz.
- Integración Jira/Zammad.

## Próxima tarea recomendada

~~~text
R-049M - Guardar central_ticket_id en el ticket local
~~~

Después podrían seguir:

~~~text
R-049N - Cola offline y reintentos de envío central
R-049O - Login y roles del panel central
R-049P - Instalador systemd para central-support
~~~

## Conclusión

DASC Server Manager supera R-049L.

El proyecto ya tiene una primera integración real entre el panel local del cliente y el panel central DASC multi-cliente, manteniendo coste de licencia cero.
