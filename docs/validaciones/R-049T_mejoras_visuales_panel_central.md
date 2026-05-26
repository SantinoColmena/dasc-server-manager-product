# R-049T - Mejoras visuales del panel central

## Objetivo

Mejorar la interfaz del panel central DASC para que sea más usable como herramienta interna del equipo de soporte.

## Estado

En curso.

## Contexto

Tras separar el soporte local del cliente y la gestión central, el panel central del puerto 8010 pasa a ser la vista principal para el equipo DASC.

Por tanto, necesita una interfaz más clara y profesional.

## Archivos modificados

- deploy/central-support/package/main.py
- deploy/central-support/package/templates/central_dashboard.html
- deploy/central-support/package/templates/central_ticket_detail.html

## Mejoras en dashboard

Se añaden métricas visuales:

- Total tickets.
- Nuevos.
- En gestión.
- Críticos.
- Cerrados o resueltos.

Se añaden filtros:

- Estado.
- Prioridad.
- Búsqueda libre por ID, cliente, email, servicio o contacto.

Se mejora la tabla:

- Diseño más ancho y legible.
- Badges para estado y prioridad.
- Enlaces claros al detalle del ticket.
- Información de cliente y contacto mejor organizada.
- Mensaje vacío cuando no hay resultados.

## Mejoras en detalle

Se reorganiza la vista de detalle:

- Cabecera con ID, estado, prioridad y tipo.
- Datos del cliente agrupados.
- Datos técnicos del ticket local agrupados.
- Descripción y evidencia separadas.
- Panel lateral de gestión interna.
- Historial central más legible.
- Botones superiores de navegación y cierre de sesión.

## Lógica añadida

El dashboard central ahora acepta filtros por query string:

- estado
- prioridad
- q

La API no se modifica.

El flujo local-central no se modifica.

## Criterio de validación

R-049T se considera preparada cuando:

- main.py central compila.
- central-support arranca.
- /login sigue funcionando.
- / redirige a /login sin sesión.
- Dashboard central autenticado carga correctamente.
- Métricas aparecen correctamente.
- Filtro por estado funciona.
- Filtro por prioridad funciona.
- Búsqueda libre funciona.
- Detalle de ticket central carga correctamente.
- Cambio de estado/prioridad sigue funcionando.
- API por token sigue funcionando.

## Límites

Esta tarea no incluye todavía:

- Diseño móvil avanzado.
- Gráficas.
- Paginación real.
- Gestión multi-cliente completa.
- Usuarios en base de datos.
- Métricas históricas.

## Próximo paso

Validar en lab-pruebas.

## Conclusión

R-049T mejora el panel central para que sea una herramienta interna más clara y profesional para el equipo DASC.
