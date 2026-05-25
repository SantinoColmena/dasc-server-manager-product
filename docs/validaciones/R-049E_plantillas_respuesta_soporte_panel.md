# R-049E - Usar plantillas de respuesta desde el panel

## Objetivo

Permitir que el equipo DASC pueda generar respuestas tipo desde el detalle de un ticket de soporte.

## Estado

En curso.

## Contexto

F6-GATE-05D documentó plantillas de respuesta al cliente.

R-049A implementó el formulario de soporte.

R-049B migró tickets a SQLite.

R-049C añadió vista interna de tickets.

R-049D añadió cambio de estado, prioridad e historial.

R-049E conecta el trabajo documental de plantillas con la interfaz del panel.

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
get_support_response_templates
get_support_response_template
render_support_response_template
~~~

## Plantillas incluidas

~~~text
Confirmación de recepción
Solicitud de más información
Incidencia en análisis
Servicio operativo
Incidencia resuelta
Restauración de backup
Mantenimiento programado
Respuesta breve WhatsApp
~~~

## Variables usadas

Las respuestas se adaptan al ticket usando:

~~~text
ticket_id
cliente
contacto
email
servicio
tipo
prioridad
estado
~~~

## Funcionamiento esperado

Desde el detalle de un ticket:

~~~text
/soporte/tickets/{ticket_id}
~~~

el equipo DASC puede:

- Seleccionar una plantilla.
- Generar una respuesta adaptada al ticket.
- Copiar el texto generado.
- Usarlo en email, WhatsApp, Jira, Zammad o canal externo.

## Criterio de validación

R-049E se considera preparada cuando:

- `main.py` compila.
- `dasc-api` arranca.
- El detalle de `DASC-2026-002` carga correctamente.
- Aparece el bloque `Plantillas de respuesta`.
- Se puede seleccionar `Incidencia en análisis`.
- Se genera una respuesta con `DASC-2026-002`, contacto, servicio y estado.
- El botón de copiar respuesta aparece.
- No se rompe el cambio de estado/prioridad.
- No se rompe la vista interna de tickets.

## Límites

Esta tarea todavía no incluye:

- Envío automático por email.
- Envío automático por WhatsApp.
- Integración API con Jira/Zammad.
- Guardar respuesta generada como comentario interno.
- Plantillas editables desde UI.

## Próximo paso

Validar en `lab-pruebas` y cerrar R-049E con evidencias.

## Conclusión

R-049E acerca el soporte de DASC a un flujo profesional, reutilizando plantillas de comunicación directamente desde el panel.
