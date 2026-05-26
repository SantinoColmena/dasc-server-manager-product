# R-049T-A - Separar vista cliente local y gestión interna DASC

## Objetivo

Separar el soporte visible en el panel local del cliente de la gestión interna real del equipo DASC.

## Estado

Cerrada.

## Contexto

Durante la revisión visual se detectó que el panel local del cliente en el puerto 8000 seguía mostrando accesos y bloques internos de gestión:

- Gestionar tickets.
- Actualizar estado y prioridad.
- Resumen para Jira/Zammad.
- Plantillas de respuesta.
- Historial interno.
- Sincronización central.

Estos elementos tienen más sentido en el panel central DASC del puerto 8010, no en el panel local del cliente.

## Decisión

El panel local debe quedar orientado a cliente:

- Crear solicitud de soporte.
- Ver últimas solicitudes de forma básica.
- No gestionar internamente tickets.
- No ver resumen Jira/Zammad.
- No ver sincronización técnica central.
- No depender del botón manual de reintento, porque R-049S ya añade timer automático.

El panel central DASC debe encargarse de:

- Ver tickets centralizados.
- Cambiar estado y prioridad.
- Gestionar incidencias.
- Usar plantillas y respuestas.
- Revisar datos técnicos.
- Centralizar el trabajo del equipo DASC.

## Archivos modificados

- deploy/api/package/main.py
- deploy/api/package/templates/soporte.html
- deploy/api/package/templates/index.html

## Variable añadida

Se añade una variable para laboratorio o depuración:

- DASC_LOCAL_INTERNAL_SUPPORT_ENABLED

Valor por defecto:

- false

Si se establece a true, permite acceder de nuevo a las vistas internas locales de soporte.

## Rutas locales protegidas por esta separación

- GET /soporte/tickets
- POST /soporte/tickets/reintentar-central
- GET /soporte/tickets/{ticket_id}
- POST /soporte/tickets/{ticket_id}/estado
- POST /soporte/tickets/{ticket_id}/sync-central

## Vista /soporte

La vista local /soporte queda como formulario de solicitud.

Se oculta el botón:

- Gestionar tickets

salvo que DASC_LOCAL_INTERNAL_SUPPORT_ENABLED=true.

También se cambia el texto para evitar lenguaje interno.

## Motivo

Aunque estas rutas ya estaban protegidas por is_admin, en el modelo de producto el admin del panel local puede representar al responsable técnico del cliente, no necesariamente al equipo técnico DASC.

Por tanto, la gestión interna no debe vivir en el panel local del cliente.

## Criterio de validación

R-049T-A queda preparada cuando:

- main.py compila.
- dasc-api arranca.
- /soporte ya no muestra Gestionar tickets por defecto.
- /soporte/tickets redirige a /soporte si DASC_LOCAL_INTERNAL_SUPPORT_ENABLED no está activo.
- /soporte/tickets/DASC-2026-006 redirige a /soporte si DASC_LOCAL_INTERNAL_SUPPORT_ENABLED no está activo.
- La creación de solicitudes desde /soporte sigue funcionando.
- El timer automático R-049S sigue funcionando.
- El panel central 8010 sigue mostrando la gestión de tickets.

## Límites

Esta tarea no elimina todavía el código interno local. Solo lo oculta y lo bloquea por configuración.

Esto permite conservar herramientas de laboratorio si hicieran falta.

## Próximo paso

Validar en lab-pruebas.

## Conclusión

R-049T-A corrige la separación de responsabilidades: el panel local queda orientado al cliente y el panel central queda como herramienta principal del equipo DASC.
