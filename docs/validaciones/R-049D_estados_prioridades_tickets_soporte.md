# R-049D - Estados y prioridades de tickets

## Objetivo

Permitir que el equipo DASC pueda cambiar el estado y la prioridad de un ticket desde la vista interna.

## Estado

Cerrada.

## Contexto

R-049A implementó el formulario básico de soporte.

R-049B migró los tickets a SQLite.

R-049C creó la vista interna de tickets y el detalle de cada ticket.

R-049D añade gestión básica de estado y prioridad.

## Ruta añadida

~~~text
POST /soporte/tickets/{ticket_id}/estado
~~~

## Archivo principal modificado

~~~text
deploy/api/package/main.py
~~~

## Template modificado

~~~text
deploy/api/package/templates/soporte_ticket_detalle.html
~~~

## Funciones añadidas

~~~text
ensure_support_history_table
add_support_ticket_history
get_support_ticket_history
update_support_ticket_status_priority
~~~

## Tabla de historial

Se añade tabla SQLite:

~~~text
support_ticket_history
~~~

Campos principales:

~~~text
id
ticket_id
fecha
usuario
accion
valor_anterior
valor_nuevo
detalle
~~~

## Estados soportados

~~~text
Abierto
En análisis
En curso
Esperando cliente
Cerrado
~~~

## Prioridades soportadas

~~~text
Crítica
Alta
Media
Baja
~~~

## Funcionamiento esperado

Desde el detalle de un ticket, el equipo DASC puede:

- Cambiar estado.
- Cambiar prioridad.
- Guardar cambios.
- Ver historial interno.
- Registrar auditoría en `dasc_logs`.

## Criterio de validación

R-049D se considera preparada cuando:

- `main.py` compila.
- `dasc-api` arranca.
- El detalle de un ticket muestra formulario de estado/prioridad.
- Se puede cambiar `DASC-2026-002` de `Abierto` a `En análisis`.
- Se puede cambiar prioridad de `Baja` a `Alta`.
- SQLite actualiza el ticket.
- `support_ticket_history` registra los cambios.
- `dasc_logs` registra el evento de actualización.
- La vista `/soporte/tickets` refleja el nuevo estado y prioridad.

## Límites

Esta tarea todavía no incluye:

- Comentarios internos libres.
- Asignación de responsable.
- Notificación al cliente.
- Exportación Jira/Zammad.
- Historial visual avanzado.

## Próximo paso

Validar en `lab-pruebas` y cerrar R-049D con evidencias.

## Conclusión

R-049D convierte la vista interna de soporte en una herramienta básica de gestión de tickets.
