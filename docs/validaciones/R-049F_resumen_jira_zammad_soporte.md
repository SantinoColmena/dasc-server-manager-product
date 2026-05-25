# R-049F - Exportar o copiar resumen para Jira/Zammad

## Objetivo

Permitir que el equipo DASC pueda generar un resumen técnico de un ticket para copiarlo en Jira, Zammad u otra herramienta externa de soporte.

## Estado

En curso.

## Contexto

R-049A implementó el formulario de soporte.

R-049B migró los tickets a SQLite.

R-049C añadió la vista interna de tickets.

R-049D añadió cambio de estado, prioridad e historial interno.

R-049E añadió plantillas de respuesta al cliente.

R-049F añade un resumen técnico interno preparado para ticketing externo.

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
format_support_history_for_external_summary
render_support_external_summary
~~~

## Funcionalidad incluida

Desde el detalle de un ticket:

~~~text
/soporte/tickets/{ticket_id}
~~~

el equipo DASC puede ver y copiar un resumen con:

- Identificación del ticket.
- Estado.
- Prioridad.
- Tipo.
- Servicio afectado.
- Cliente.
- Contacto.
- Email.
- Fechas.
- Canal.
- Descripción.
- Evidencia.
- Historial interno.
- Próximo paso recomendado.

## Uso previsto

El resumen puede copiarse manualmente en:

~~~text
Jira Service Management
Zammad
Email interno
Documento de seguimiento
Herramienta futura de ticketing
~~~

## Criterio de validación

R-049F se considera preparada cuando:

- `main.py` compila.
- `dasc-api` arranca.
- El detalle de `DASC-2026-002` carga correctamente.
- Aparece el bloque `Resumen para Jira/Zammad`.
- El resumen contiene `DASC-2026-002`.
- El resumen contiene cliente, contacto, estado, prioridad y servicio.
- El resumen contiene descripción y evidencia.
- El resumen contiene historial interno.
- Aparece el botón `Copiar resumen`.
- No se rompe la generación de plantillas de respuesta.
- No se rompe el cambio de estado/prioridad.

## Límites

Esta tarea todavía no incluye:

- Integración real con API de Jira.
- Integración real con API de Zammad.
- Creación automática de issue/ticket externo.
- Sincronización bidireccional.
- Adjuntos.

## Próximo paso

Validar en `lab-pruebas` y cerrar R-049F con evidencias.

## Conclusión

R-049F permite que DASC use Jira o Zammad de forma práctica sin integraciones complejas iniciales, copiando un resumen técnico completo desde el panel.
