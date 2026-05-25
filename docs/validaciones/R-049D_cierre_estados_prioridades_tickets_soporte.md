# R-049D - Cierre estados y prioridades de tickets

## Objetivo

Cerrar la validación de gestión básica de estados y prioridades para tickets de soporte dentro del panel DASC.

## Estado

Cerrada.

## Funcionalidad implementada

R-049D permite modificar desde la vista interna:

~~~text
Estado del ticket
Prioridad del ticket
~~~

Ruta añadida:

~~~text
POST /soporte/tickets/{ticket_id}/estado
~~~

Archivo principal modificado:

~~~text
deploy/api/package/main.py
~~~

Template modificado:

~~~text
deploy/api/package/templates/soporte_ticket_detalle.html
~~~

## Tabla de historial añadida

Se creó la tabla SQLite:

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

## Despliegue validado

La funcionalidad fue desplegada manualmente en:

~~~text
lab-pruebas
/opt/dasc/api
~~~

Se copiaron los cambios desde el repositorio temporal hacia la instalación activa sin reinstalar todo el paquete ni sobrescribir `config.env`.

## Validación técnica

Se comprobó:

~~~text
main.py del repositorio compila: OK
main.py instalado compila: OK
dasc-api activo: OK
Panel responde: OK
Detalle de ticket protegido por sesión: OK
~~~

## Validación funcional

Desde el detalle del ticket:

~~~text
/soporte/tickets/DASC-2026-002
~~~

se actualizó:

~~~text
Estado anterior: Abierto
Estado nuevo: En análisis

Prioridad anterior: Baja
Prioridad nueva: Alta
~~~

La pantalla mostró confirmación:

~~~text
Ticket actualizado correctamente.
~~~

## Validación en SQLite

La base local:

~~~text
/opt/dasc/api/data/support_tickets.db
~~~

registró el ticket actualizado:

~~~text
id: DASC-2026-002
cliente: PyME Demo SQLite
tipo: Consulta
prioridad: Alta
servicio: Soporte
estado: En análisis
creado_por: admin
origen: panel
fecha_actualizacion: 2026-05-25 14:38:51
~~~

## Validación de historial interno

La tabla `support_ticket_history` registró dos eventos:

~~~text
Cambio de estado
Abierto -> En análisis
Detalle: Estado actualizado desde la vista interna
~~~

~~~text
Cambio de prioridad
Baja -> Alta
Detalle: Prioridad actualizada desde la vista interna
~~~

Ambos cambios quedaron asociados a:

~~~text
ticket_id: DASC-2026-002
usuario: admin
fecha: 2026-05-25 14:38:51
~~~

## Validación de vista interna

La vista:

~~~text
/soporte/tickets
~~~

reflejó correctamente:

~~~text
DASC-2026-002
Prioridad: Alta
Estado: En análisis
Servicio: Soporte
~~~

El resumen superior también se actualizó:

~~~text
Total tickets: 2
Abiertos: 1
Cerrados: 0
~~~

## Validación de logs remotos

En `lab-db-gate02`, dentro de la base `dasc_logs`, se confirmó:

~~~text
id 58
tipo soporte
usuario admin
ip_origen 192.168.1.140
recurso POST /soporte/tickets/DASC-2026-002/estado
resultado OK
detalle estado: Abierto -> En análisis; prioridad: Baja -> Alta
~~~

También quedaron registrados:

~~~text
POST /soporte/tickets/DASC-2026-002/estado | acceso | HTTP 303
GET /soporte/tickets/DASC-2026-002 | acceso | HTTP 200
HEAD /soporte/tickets/DASC-2026-002 | acceso bloqueado por no autenticado
~~~

## Resultado

R-049D queda validada correctamente.

El soporte interno ya permite:

- Cambiar estado de tickets.
- Cambiar prioridad de tickets.
- Actualizar fecha de modificación.
- Guardar historial interno.
- Reflejar cambios en la vista de tickets.
- Registrar auditoría en logs remotos.
- Mantener protección por sesión.

## Límites actuales

Esta versión todavía no incluye:

- Comentarios internos libres.
- Asignación de responsable.
- Respuesta al cliente desde el panel.
- Plantillas aplicables desde UI.
- Exportación a Jira/Zammad.
- Envío automático de email.
- Adjuntos.
- Portal externo de cliente.

## Próxima tarea recomendada

~~~text
R-049E - Usar plantillas de respuesta desde documentación
~~~

La siguiente mejora lógica es permitir que el equipo DASC pueda consultar o copiar respuestas tipo desde el panel al gestionar un ticket.

## Conclusión

DASC Server Manager supera R-049D.

La gestión de soporte ya permite crear, listar, consultar y actualizar tickets con trazabilidad interna y auditoría remota.
