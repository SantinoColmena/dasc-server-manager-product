# R-049B - Cierre almacenamiento SQLite para tickets de soporte

## Objetivo

Cerrar la validación de almacenamiento de tickets de soporte en SQLite dentro del panel DASC.

## Estado

Cerrada.

## Funcionalidad implementada

R-049B evoluciona el almacenamiento inicial de soporte desde JSON local a SQLite.

Archivo principal modificado:

~~~text
deploy/api/package/main.py
~~~

Plantilla actualizada:

~~~text
deploy/api/package/templates/soporte.html
~~~

Documento inicial:

~~~text
docs/validaciones/R-049B_sqlite_tickets_soporte.md
~~~

## Almacenamiento validado

Se crea y utiliza la base local:

~~~text
/opt/dasc/api/data/support_tickets.db
~~~

El JSON anterior se conserva:

~~~text
/opt/dasc/api/data/support_tickets.json
~~~

## Tabla validada

Tabla creada:

~~~text
support_tickets
~~~

Campos principales validados:

~~~text
id
fecha_apertura
fecha_actualizacion
cliente
contacto
email
telefono
canal
tipo
prioridad
servicio
descripcion
evidencia
estado
creado_por
origen
~~~

## Migración desde JSON

Se validó la migración automática del ticket creado en R-049A:

~~~text
DASC-2026-001
origen: json_migrado
cliente: PyME Demo
tipo: Incidencia
prioridad: Media
servicio: API / Panel
estado: Abierto
creado_por: admin
~~~

## Nuevo ticket creado en SQLite

Se creó un nuevo ticket desde el panel después de activar SQLite:

~~~text
DASC-2026-002
origen: panel
cliente: PyME Demo SQLite
tipo: Consulta
prioridad: Baja
servicio: Soporte
estado: Abierto
creado_por: admin
~~~

## Validación técnica

Se comprobó:

~~~text
main.py del repositorio compila: OK
main.py instalado compila: OK
dasc-api activo: OK
Panel responde: OK
/soporte sin sesión redirige a /login: OK
/soporte con sesión carga correctamente: OK
support_tickets.db creado: OK
tickets en SQLite: 2
~~~

## Validación de logs remotos

En `lab-db-gate02`, dentro de la base `dasc_logs`, se confirmó el registro del nuevo ticket:

~~~text
id 40
tipo soporte
usuario admin
ip_origen 192.168.1.140
recurso POST /soporte DASC-2026-002
resultado OK
detalle Ticket de soporte creado: Consulta / Baja / Soporte
~~~

También quedaron registrados los accesos asociados:

~~~text
GET /soporte OK
POST /soporte OK
HEAD /soporte ERROR por acceso no autenticado
~~~

## Resultado

R-049B queda validada correctamente.

El soporte del panel ya no depende solo de un JSON plano y pasa a tener una base SQLite local preparada para gestión interna.

## Límites actuales

Esta versión todavía no incluye:

- Edición de tickets.
- Cambio de estado desde UI.
- Vista interna avanzada.
- Filtros o búsqueda.
- Adjuntos.
- Exportación a Jira/Zammad.
- Envío automático de email.
- Portal externo de cliente.
- Separación avanzada de permisos por rol.

## Próxima tarea recomendada

~~~text
R-049C - Vista interna de tickets para equipo DASC
~~~

Esta tarea debería permitir ver tickets de forma más útil, preparar filtros básicos y abrir camino al cambio de estado.

## Conclusión

DASC Server Manager supera R-049B.

El sistema de soporte ya cuenta con almacenamiento estructurado en SQLite, migración desde JSON y auditoría en logs remotos.
