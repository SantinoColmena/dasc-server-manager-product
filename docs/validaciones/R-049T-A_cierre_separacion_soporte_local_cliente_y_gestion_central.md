# R-049T-A - Cierre separación soporte local cliente y gestión central

## Objetivo

Cerrar la validación de la separación entre la vista de soporte visible en el panel local del cliente y la gestión interna del equipo DASC.

## Estado

Cerrada.

## Contexto

Durante la revisión visual se detectó que el panel local del cliente seguía mostrando elementos internos de gestión de soporte.

Elementos detectados:

- Botón Gestionar tickets.
- Vista interna de tickets locales.
- Detalle técnico de tickets.
- Actualización de estado y prioridad.
- Resumen para Jira/Zammad.
- Plantillas de respuesta.
- Historial interno.
- Sincronización central.

Estos elementos no deben formar parte de la experiencia normal del cliente en el panel local.

## Decisión aplicada

El panel local del puerto 8000 queda orientado a cliente.

Debe permitir:

- Crear solicitudes de soporte.
- Ver últimas solicitudes de forma básica.
- Consultar información sencilla de seguimiento.

No debe mostrar por defecto:

- Gestión interna de tickets.
- Herramientas de respuesta.
- Resúmenes para herramientas externas.
- Sincronización técnica central.
- Botón manual de reintento central.

La gestión real queda reservada al panel central DASC del puerto 8010.

## Archivos modificados

- deploy/api/package/main.py
- deploy/api/package/templates/soporte.html
- deploy/api/package/templates/index.html
- docs/validaciones/R-049T-A_separar_soporte_local_cliente_y_gestion_central.md

## Variable de control añadida

Se añadió la variable:

- DASC_LOCAL_INTERNAL_SUPPORT_ENABLED

Valor por defecto:

- false

Si se establece en true, permite recuperar las vistas internas locales para laboratorio o depuración.

## Rutas bloqueadas por defecto

Con DASC_LOCAL_INTERNAL_SUPPORT_ENABLED en false, quedan bloqueadas o redirigidas:

- GET /soporte/tickets
- POST /soporte/tickets/reintentar-central
- GET /soporte/tickets/{ticket_id}
- POST /soporte/tickets/{ticket_id}/estado
- POST /soporte/tickets/{ticket_id}/sync-central

## Validación técnica

Se comprobó:

- main.py R-049T-A compila correctamente.
- main.py instalado compila correctamente.
- dasc-api reinicia correctamente.
- dasc-api queda activo.
- El código R-049T-A está instalado.
- DASC_LOCAL_INTERNAL_SUPPORT_ENABLED aparece en main.py.
- soporte.html contiene la condición para ocultar Gestionar tickets.
- Timer R-049S sigue activo.
- Timer R-049S sigue habilitado.

## Validación visual

En la ruta:

- /soporte

se comprobó que ya no aparece:

- Gestionar tickets

Se comprobó que ahora aparece:

- Formulario para registrar solicitudes de soporte hacia el equipo DASC.
- Últimas solicitudes.
- Seguimiento básico de solicitudes registradas en este panel.

## Validación de redirección

Al acceder manualmente a:

- /soporte/tickets

el sistema redirige a:

- /soporte?ok=0&msg=Gestion+interna+reservada+al+panel+central+DASC

Se muestra el aviso:

- Gestion interna reservada al panel central DASC

Esto confirma que la gestión interna local queda cerrada por defecto.

## Resultado

R-049T-A queda validada correctamente.

El panel local del cliente ya no expone la gestión interna de soporte y queda alineado con el modelo de producto.

## Límites actuales

Esta tarea no elimina el código interno local.

Solo lo oculta y lo bloquea por configuración para conservarlo como herramienta de laboratorio o emergencia.

## Próxima tarea recomendada

R-049T - Mejoras visuales del panel central

Objetivo de la siguiente tarea:

- Mejorar dashboard central.
- Mejorar detalle de ticket central.
- Añadir filtros básicos.
- Añadir resumen por estados.
- Hacer el panel central más profesional para uso real del equipo DASC.

## Conclusión

DASC Server Manager supera R-049T-A.

La separación queda clara:

- Panel local 8000: cliente y solicitud de soporte.
- Panel central 8010: equipo DASC y gestión interna.
