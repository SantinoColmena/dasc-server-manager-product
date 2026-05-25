# R-049C - Cierre vista interna de tickets de soporte

## Objetivo

Cerrar la validación de la primera vista interna de tickets de soporte para el equipo DASC.

## Estado

Cerrada.

## Funcionalidad implementada

R-049C añade una vista interna para consultar tickets de soporte almacenados en SQLite.

Rutas añadidas:

~~~text
GET /soporte/tickets
GET /soporte/tickets/{ticket_id}
~~~

Templates añadidos:

~~~text
deploy/api/package/templates/soporte_tickets.html
deploy/api/package/templates/soporte_ticket_detalle.html
~~~

Template actualizado:

~~~text
deploy/api/package/templates/soporte.html
~~~

## Funciones añadidas

~~~text
search_support_tickets
get_support_ticket
support_ticket_counts
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
/soporte/tickets sin sesión redirige a /login: OK
/soporte/tickets/DASC-2026-002 sin sesión redirige a /login: OK
~~~

## Validación funcional

Desde navegador con sesión iniciada se comprobó:

~~~text
/soporte/tickets carga correctamente
Total tickets: 2
Abiertos: 2
Cerrados: 0
DASC-2026-001 visible
DASC-2026-002 visible
~~~

También se comprobó el filtro:

~~~text
/soporte/tickets?prioridad=Baja
~~~

Resultado:

~~~text
Muestra DASC-2026-002
Prioridad Baja
Tipo Consulta
Servicio Soporte
Estado Abierto
~~~

## Validación de detalle

Se abrió correctamente:

~~~text
/soporte/tickets/DASC-2026-002
~~~

El detalle muestra:

~~~text
ID: DASC-2026-002
Cliente: PyME Demo SQLite
Contacto: Responsable IT
Email: soporte-sqlite@dasc.local
Servicio: Soporte
Canal: Panel DASC
Fecha apertura: 2026-05-25 14:24:17
Creado por: admin
Descripción: Ticket de prueba R-049B guardado en SQLite.
Evidencia: Validación de migración desde JSON a SQLite.
~~~

## Validación SQLite

La base local mantiene correctamente los tickets:

~~~text
/opt/dasc/api/data/support_tickets.db
~~~

Contenido validado:

~~~text
DASC-2026-001 | PyME Demo | Incidencia | Media | API / Panel | Abierto | admin | json_migrado
DASC-2026-002 | PyME Demo SQLite | Consulta | Baja | Soporte | Abierto | admin | panel
~~~

Resumen:

~~~text
Total tickets: 2
Estado Abierto: 2
Prioridad Baja: 1
Prioridad Media: 1
~~~

## Validación de logs remotos

En `lab-db-gate02`, dentro de la base `dasc_logs`, se confirmó:

~~~text
id 54
tipo acceso
usuario admin
ip_origen 192.168.1.140
recurso GET /soporte/tickets/DASC-2026-002
resultado OK
detalle HTTP 200
~~~

También se registraron accesos autenticados a:

~~~text
GET /soporte/tickets
~~~

y accesos no autenticados bloqueados a:

~~~text
HEAD /soporte/tickets
HEAD /soporte/tickets/DASC-2026-002
~~~

## Resultado

R-049C queda validada correctamente.

El sistema de soporte ya permite:

- Listar tickets.
- Ver resumen de totales.
- Filtrar por estado.
- Filtrar por prioridad.
- Filtrar por tipo.
- Buscar por texto.
- Abrir detalle de un ticket.
- Registrar accesos en logs remotos.
- Mantener protección por sesión.

## Límites actuales

Esta versión todavía no incluye:

- Cambio de estado desde UI.
- Edición de tickets.
- Asignación de responsable.
- Comentarios internos.
- Historial de cambios.
- Exportación a Jira/Zammad.
- Envío automático de email.
- Portal externo de cliente.

## Próxima tarea recomendada

~~~text
R-049D - Estados y prioridades de tickets
~~~

La siguiente mejora lógica es permitir cambiar el estado de un ticket desde la vista interna, por ejemplo:

~~~text
Abierto
En análisis
En curso
Esperando cliente
Cerrado
~~~

## Conclusión

DASC Server Manager supera R-049C.

El soporte ya no solo permite crear tickets, sino también consultarlos desde una vista interna básica preparada para gestión real.
