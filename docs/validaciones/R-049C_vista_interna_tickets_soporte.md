# R-049C - Vista interna de tickets para equipo DASC

## Objetivo

Crear una vista interna para que el equipo DASC pueda consultar tickets de soporte de forma más ordenada.

## Estado

Cerrada.

## Contexto

R-049A implementó el formulario básico de soporte.

R-049B migró el almacenamiento de tickets a SQLite.

R-049C añade una vista interna para consultar tickets, aplicar filtros básicos y abrir el detalle de cada solicitud.

## Rutas añadidas

~~~text
GET /soporte/tickets
GET /soporte/tickets/{ticket_id}
~~~

## Templates añadidos

~~~text
deploy/api/package/templates/soporte_tickets.html
deploy/api/package/templates/soporte_ticket_detalle.html
~~~

## Template actualizado

~~~text
deploy/api/package/templates/soporte.html
~~~

Se añade acceso a:

~~~text
/soporte/tickets
~~~

## Funciones añadidas

~~~text
search_support_tickets
get_support_ticket
support_ticket_counts
~~~

## Funcionalidad incluida

La vista interna permite:

- Ver total de tickets.
- Ver tickets abiertos.
- Ver tickets cerrados.
- Listar tickets.
- Filtrar por estado.
- Filtrar por prioridad.
- Filtrar por tipo.
- Buscar por texto.
- Abrir detalle de un ticket.

## Límites

Esta tarea todavía no implementa:

- Cambio de estado.
- Edición de tickets.
- Asignación de responsable.
- Comentarios internos.
- Exportación a Jira/Zammad.
- Envío automático de email.

## Criterio de validación

R-049C se considera preparada cuando:

- `main.py` compila.
- `dasc-api` arranca.
- `/soporte/tickets` redirige a login sin sesión.
- `/soporte/tickets` carga con sesión.
- Se listan los tickets `DASC-2026-001` y `DASC-2026-002`.
- El filtro por prioridad funciona.
- El detalle `/soporte/tickets/DASC-2026-002` carga correctamente.
- No se rompe la creación de tickets desde `/soporte`.

## Próximo paso

Validar en `lab-pruebas` y cerrar R-049C con evidencias.

## Conclusión

R-049C prepara la primera vista interna real de gestión de soporte para el equipo DASC.
