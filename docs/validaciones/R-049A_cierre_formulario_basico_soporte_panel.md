# R-049A - Cierre formulario básico de soporte en el panel

## Objetivo

Cerrar la validación de la primera implementación real de soporte dentro del panel DASC.

## Estado

Cerrada.

## Funcionalidad implementada

Se implementó una página básica de soporte en el panel:

~~~text
GET /soporte
POST /soporte
~~~

Archivos principales:

~~~text
deploy/api/package/main.py
deploy/api/package/templates/soporte.html
deploy/api/package/templates/index.html
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
/soporte sin sesión redirige a /login: OK
/soporte con sesión carga correctamente: OK
~~~

## Validación funcional

Desde el navegador se accedió al panel y se abrió la nueva sección de soporte.

Se creó un ticket de prueba:

~~~text
ID: DASC-2026-001
Cliente: PyME Demo
Contacto: Responsable IT
Email: soporte-demo@dasc.local
Tipo: Incidencia
Prioridad: Media
Servicio: API / Panel
Descripción: Ticket de prueba R-049A desde el panel.
Estado: Abierto
Creado por: admin
~~~

## Validación de almacenamiento

El ticket quedó guardado en:

~~~text
/opt/dasc/api/data/support_tickets.json
~~~

El JSON contiene los campos esperados:

~~~text
id
fecha_apertura
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
~~~

## Validación de logs remotos

En `lab-db-gate02`, dentro de la base `dasc_logs`, se confirmó el registro del evento:

~~~text
id 33
tipo soporte
usuario admin
ip_origen 192.168.1.140
recurso POST /soporte DASC-2026-001
resultado OK
detalle Ticket de soporte creado: Incidencia / Media / API / Panel
~~~

También quedaron registrados:

~~~text
GET /soporte OK
POST /soporte OK
HEAD /soporte ERROR por acceso no autenticado
~~~

Esto confirma que la ruta está protegida por sesión y que la creación del ticket genera auditoría.

## Resultado

R-049A queda validada como primera implementación real del soporte en panel.

La funcionalidad permite:

- Abrir sección de soporte desde el panel.
- Crear tickets básicos.
- Guardarlos localmente.
- Mostrar últimos tickets.
- Registrar evento en logs remotos.
- Mantener protección por sesión.

## Límites actuales

Esta versión todavía no incluye:

- Edición de tickets.
- Cambio de estado.
- Vista avanzada de gestión.
- Adjuntos reales.
- Envío automático de email.
- Integración Jira/Zammad.
- Portal externo de cliente.
- Filtros o búsqueda de tickets.
- Separación avanzada de permisos.

## Próxima tarea recomendada

~~~text
R-049B - Guardar tickets en SQLite/DB y preparar estructura interna
~~~

También puede plantearse:

~~~text
R-049C - Vista interna de tickets para equipo DASC
~~~

## Conclusión

DASC Server Manager supera R-049A.

El soporte deja de estar solo documentado y ya cuenta con una primera funcionalidad real integrada en el panel.
