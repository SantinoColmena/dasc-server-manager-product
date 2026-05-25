# R-049K - Cambiar estado y prioridad desde panel central

## Objetivo

Permitir que el equipo técnico DASC pueda cambiar el estado y la prioridad de un ticket recibido en el panel central.

## Estado

Cerrada.

## Contexto

R-049I creó la API central local de soporte.

R-049J añadió el detalle de ticket central.

R-049K añade gestión básica interna del ticket desde el panel central.

## Archivos modificados

~~~text
deploy/central-support/package/main.py
deploy/central-support/package/templates/central_ticket_detail.html
~~~

## Ruta añadida

~~~text
POST /tickets/{ticket_id}/estado
~~~

## Funciones añadidas

~~~text
ensure_central_history_table
get_central_ticket_history
add_central_ticket_history
update_central_ticket_status_priority
~~~

## Estados permitidos

~~~text
Nuevo
En análisis
Pendiente cliente
En curso
Resuelto
Cerrado
~~~

## Prioridades permitidas

~~~text
Baja
Media
Alta
Crítica
~~~

## Historial interno central

Se añade una tabla SQLite para registrar cambios internos:

~~~text
central_ticket_history
~~~

Registra:

- Ticket.
- Fecha.
- Usuario.
- Acción.
- Valor anterior.
- Valor nuevo.
- Detalle.

## Usuario temporal

Hasta implementar login propio del panel central, se registra el usuario:

~~~text
dasc_tecnico_lab
~~~

Esto es temporal y de laboratorio.

## Criterio de validación

R-049K se considera preparada cuando:

- `main.py` compila.
- La API central arranca.
- El detalle de `CENTRAL-2026-0001` carga.
- Aparece el bloque `Actualizar estado y prioridad`.
- Se puede cambiar el estado.
- Se puede cambiar la prioridad.
- El ticket se actualiza en SQLite.
- El historial interno central registra los cambios.
- El dashboard refleja el nuevo estado/prioridad.
- No se rompe `/health`.
- No se rompe la recepción de tickets.

## Límites

Esta tarea todavía no incluye:

- Login real del panel central.
- Roles reales `dasc_tecnico`, `dasc_admin`, `dasc_superadmin`.
- Comentarios internos manuales.
- Notificación al cliente.
- Sincronización con panel local.
- Integración Jira/Zammad.

## Próximo paso

Validar en `lab-pruebas`.

## Conclusión

R-049K convierte el panel central en una herramienta de gestión básica de incidencias, no solo de consulta.
