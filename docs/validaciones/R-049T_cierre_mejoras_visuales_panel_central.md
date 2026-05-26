# R-049T - Cierre mejoras visuales del panel central

## Objetivo

Cerrar la validación de las mejoras visuales del panel central DASC.

## Estado

Cerrada.

## Contexto

Después de separar el soporte local del cliente y la gestión interna DASC, el panel central del puerto 8010 pasa a ser la herramienta principal del equipo técnico DASC.

Por ese motivo se mejoró su interfaz para que fuese más clara, usable y profesional.

## Archivos modificados

- deploy/central-support/package/main.py
- deploy/central-support/package/templates/central_dashboard.html
- deploy/central-support/package/templates/central_ticket_detail.html
- docs/validaciones/R-049T_mejoras_visuales_panel_central.md
- docs/validaciones/R-049T_FIX1_contexto_dashboard_panel_central.md
- docs/validaciones/R-049T_FIX2_restaurar_get_central_ticket.md

## Commits relacionados

- 99a9759 feat: mejorar interfaz panel central
- 9328a2b fix: completar contexto dashboard central
- d97fcc1 fix: aplicar contexto dashboard central
- 4ea1dd3 fix: restaurar detalle ticket central

## Mejoras aplicadas al dashboard central

Se rediseñó la vista principal del panel central.

Ahora incluye:

- Cabecera más profesional.
- Información de sesión.
- Botón de cerrar sesión.
- Métricas superiores.
- Filtros visuales.
- Tabla más clara.
- Badges para estado y prioridad.
- Enlace directo al detalle de cada ticket.

## Métricas añadidas

El dashboard central muestra:

- Total tickets.
- Nuevos.
- En gestión.
- Críticos.
- Cerrados / resueltos.

## Filtros añadidos

Se añadió soporte visual y funcional para:

- Filtro por estado.
- Filtro por prioridad.
- Búsqueda libre.

La búsqueda libre permite localizar tickets por campos como:

- ID central.
- ID cliente.
- Nombre del cliente.
- Ticket local.
- Tipo.
- Prioridad.
- Estado.
- Servicio.
- Contacto.
- Email.

## Mejoras aplicadas al detalle del ticket central

La vista de detalle del ticket central se reorganizó en bloques más claros:

- Cabecera con ID central.
- Badges de estado, prioridad y tipo.
- Datos del cliente.
- Ticket local asociado.
- Servicio afectado.
- Contacto.
- Fechas.
- Versión del panel local.
- Descripción.
- Evidencia.
- Gestión interna.
- Historial interno central.

## Correcciones realizadas

Durante la aplicación inicial se detectaron dos incidencias.

### R-049T-FIX1

Problema:

- Las plantillas nuevas esperaban variables que main.py todavía no entregaba.

Solución:

- Se actualizó la función dashboard para enviar métricas, filtros, estados, prioridades y lista filtrada de tickets.

### R-049T-FIX2

Problema:

- Durante la sustitución del dashboard se eliminó accidentalmente la función get_central_ticket.

Riesgo:

- El dashboard podía cargar, pero el detalle de ticket central podía fallar con error 500.

Solución:

- Se restauró get_central_ticket antes de la ruta GET /tickets/{ticket_id}.

## Validación técnica de despliegue

Se validó en lab-pruebas:

- Repo actualizado a 4ea1dd3.
- main.py central nuevo compila.
- Se hicieron backups de los archivos anteriores.
- Se copiaron los archivos nuevos a /opt/dasc/central-support.
- main.py instalado compila.
- dasc-central-support reinicia correctamente.
- dasc-central-support queda activo.
- /health responde correctamente.
- Logs recientes sin errores críticos.

## Validación HTTP

Se comprobó:

- Login admin central: HTTP 303 hacia /
- Dashboard autenticado: HTTP 200
- Dashboard con filtro estado Nuevo: HTTP 200
- Dashboard con búsqueda Cliente: HTTP 200
- Detalle CENTRAL-2026-0003: HTTP 200

## Validación visual

En navegador se comprobó:

- Pantalla de login correcta.
- Dashboard central nuevo visible.
- Tarjetas de métricas visibles.
- Tabla de tickets centralizados mejorada.
- Filtros visibles.
- Detalle de ticket central rediseñado.
- Bloque de gestión interna separado.
- Historial interno central visible.

## Validación de cambio de estado y prioridad

Desde el detalle del ticket central se cambió:

- Estado: En curso
- Prioridad: Media

Resultado visual:

- El panel mostró Ticket actualizado.
- Los badges superiores reflejaron En curso y Media.
- El formulario quedó con los nuevos valores seleccionados.

## Validación SQLite central

Se validó en la base central:

Ticket:

- CENTRAL-2026-0003

Resultado:

- estado: En curso
- prioridad: Media
- fecha_actualizacion: 2026-05-26 14:05:14

Historial registrado:

- Cambio de prioridad: Crítica a Media.
- Cambio de estado: Nuevo a En curso.

Usuario registrado:

- admin

Detalle registrado:

- Actualización realizada desde panel central DASC.

## Resultado

R-049T queda validada correctamente.

El panel central DASC ya tiene una interfaz más profesional y funcional para el equipo interno.

## Límites actuales

Esta tarea no incluye todavía:

- Paginación real.
- Gráficas.
- Exportación CSV.
- Vista multi-cliente avanzada.
- Panel de SLA.
- Panel de cola/sincronización.
- Usuarios centrales en base de datos.
- Diseño móvil avanzado.

## Próximas tareas recomendadas

- R-049U - Endurecimiento de credenciales del panel central.
- R-049V - Reverse proxy Nginx para central-support.
- R-049W - Panel visual de cola/sincronización.
- R-049X - Documentación global del soporte central.

## Conclusión

DASC Server Manager supera R-049T.

El panel central deja de ser una vista básica de laboratorio y pasa a ser una herramienta interna más clara, organizada y alineada con la visión de producto-servicio.
