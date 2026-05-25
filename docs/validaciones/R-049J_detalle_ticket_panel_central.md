# R-049J - Detalle de ticket en panel central

## Objetivo

Añadir una vista de detalle para tickets recibidos en el panel central DASC.

## Estado

En curso.

## Contexto

R-049I creó la primera API central local de soporte.

Se validó la recepción del ticket:

~~~text
CENTRAL-2026-0001
~~~

R-049J permite abrir ese ticket desde el panel central y consultar toda su información.

## Archivos modificados

~~~text
deploy/central-support/package/main.py
deploy/central-support/package/templates/central_dashboard.html
~~~

## Archivo añadido

~~~text
deploy/central-support/package/templates/central_ticket_detail.html
~~~

## Ruta añadida

~~~text
GET /tickets/{ticket_id}
~~~

## Función añadida

~~~text
get_central_ticket
~~~

## Funcionalidad incluida

Desde el dashboard central, el ID del ticket pasa a ser un enlace.

Al abrir el detalle se muestra:

- ID central.
- Estado.
- Prioridad.
- Tipo.
- Cliente.
- ID de cliente.
- Ticket local.
- Servicio afectado.
- Contacto.
- Email.
- Fecha de recepción central.
- Fecha de actualización.
- Fecha origen del cliente.
- Versión del panel local.
- Origen.
- Descripción.
- Evidencia.

## Criterio de validación

R-049J se considera preparada cuando:

- `main.py` compila.
- La API central arranca.
- `GET /` carga el dashboard.
- El ID `CENTRAL-2026-0001` aparece como enlace.
- `GET /tickets/CENTRAL-2026-0001` carga correctamente.
- El detalle muestra los datos del ticket recibido.
- No se rompe `/health`.
- No se rompe la recepción de tickets por API.

## Límites

Esta tarea todavía no incluye:

- Login del panel central.
- Cambio de estado central.
- Historial central.
- Comentarios internos.
- Filtros avanzados.
- Integración con panel local.
- Integración Jira/Zammad.

## Próximo paso

Validar en `lab-pruebas`.

## Conclusión

R-049J convierte el dashboard central en una vista más útil para el equipo DASC, permitiendo consultar el detalle completo de cada incidencia centralizada.
