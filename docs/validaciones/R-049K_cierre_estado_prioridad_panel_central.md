# R-049K - Cierre gestión de estado y prioridad desde panel central

## Objetivo

Cerrar la validación de la gestión básica de estado y prioridad desde el panel central DASC.

## Estado

Cerrada.

## Funcionalidad implementada

R-049K permite que el equipo técnico DASC pueda modificar desde el panel central:

~~~text
Estado del ticket
Prioridad del ticket
~~~

Ruta añadida:

~~~text
POST /tickets/{ticket_id}/estado
~~~

Funciones añadidas:

~~~text
ensure_central_history_table
get_central_ticket_history
add_central_ticket_history
update_central_ticket_status_priority
~~~

## Tabla añadida

Se añadió la tabla SQLite:

~~~text
central_ticket_history
~~~

Esta tabla registra los cambios internos realizados sobre cada ticket central.

## Validación realizada

La validación se realizó sobre el ticket:

~~~text
CENTRAL-2026-0001
~~~

URL de detalle:

~~~text
http://192.168.1.250:8010/tickets/CENTRAL-2026-0001
~~~

## Resultado del ticket

El ticket quedó actualizado con:

~~~text
prioridad: Crítica
estado: En análisis
~~~

## Historial registrado

Se confirmó en SQLite que el historial interno contiene:

~~~text
Cambio de prioridad: Alta -> Crítica
Cambio de estado: Nuevo -> En análisis
usuario: dasc_tecnico_lab
detalle: Actualización realizada desde panel central DASC
~~~

## Validación visual

El dashboard central muestra correctamente:

~~~text
CENTRAL-2026-0001
Cliente Demo A
DASC-2026-002
Consulta
Crítica
En análisis
Soporte
Responsable IT
~~~

## Validación técnica

Se comprobó:

~~~text
main.py central compila: OK
API central arranca: OK
GET /health responde: OK
Detalle del ticket carga: OK
Formulario de estado/prioridad aparece: OK
Cambio de prioridad funciona: OK
Cambio de estado funciona: OK
Historial interno central funciona: OK
Dashboard refleja los cambios: OK
SQLite refleja los cambios: OK
~~~

## Nota sobre mensaje "Sin cambios"

Durante una prueba posterior con `curl`, la API devolvió:

~~~text
msg=Sin+cambios
~~~

Esto es correcto porque el ticket ya estaba en el estado y prioridad solicitados.

No representa un error.

## Límites actuales

Esta versión todavía no incluye:

- Login real del panel central.
- Roles reales `dasc_tecnico`, `dasc_admin`, `dasc_superadmin`.
- Comentarios internos manuales.
- Notificación al cliente.
- Sincronización con panel local.
- Integración Jira/Zammad.
- HTTPS real.
- Despliegue systemd del panel central.

## Próxima tarea recomendada

~~~text
R-049L - Enviar tickets desde panel local hacia API central
~~~

También quedan como tareas futuras:

~~~text
R-049M - Login y roles del panel central
R-049N - Instalador systemd para central-support
R-049O - Comentarios internos en tickets centrales
~~~

## Conclusión

DASC Server Manager supera R-049K.

El panel central ya no solo recibe y muestra incidencias, sino que permite gestionarlas internamente mediante estado, prioridad e historial técnico central.
