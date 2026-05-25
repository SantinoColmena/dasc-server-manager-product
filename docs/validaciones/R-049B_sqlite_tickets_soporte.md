# R-049B - Guardar tickets en SQLite y preparar estructura interna

## Objetivo

Evolucionar el almacenamiento inicial de tickets desde JSON local hacia una base SQLite local preparada para gestión interna.

## Estado

En curso.

## Contexto

R-049A implementó el primer formulario real de soporte en el panel.

La primera versión guardaba tickets en:

~~~text
data/support_tickets.json
~~~

R-049B introduce SQLite para permitir una gestión más estructurada.

## Cambios aplicados

Archivo modificado:

~~~text
deploy/api/package/main.py
~~~

Plantilla actualizada:

~~~text
deploy/api/package/templates/soporte.html
~~~

## Nuevo almacenamiento

Los tickets pasan a guardarse en:

~~~text
data/support_tickets.db
~~~

Tabla creada:

~~~text
support_tickets
~~~

## Campos principales

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

## Índices añadidos

~~~text
idx_support_tickets_estado
idx_support_tickets_prioridad
idx_support_tickets_fecha
~~~

## Migración desde JSON

Si existe:

~~~text
data/support_tickets.json
~~~

el sistema intenta migrar tickets existentes a SQLite usando `INSERT OR IGNORE`.

Esto permite conservar tickets creados en R-049A, como:

~~~text
DASC-2026-001
~~~

## Funcionamiento esperado

- Si no existe la DB, se crea automáticamente.
- Si existe JSON previo, se migra automáticamente.
- Los nuevos tickets se guardan en SQLite.
- La página `/soporte` muestra los últimos tickets desde SQLite.
- El ID de ticket se calcula usando los tickets existentes en SQLite.

## Límites

Esta tarea todavía no implementa:

- Edición de tickets.
- Cambio de estado.
- Vista avanzada.
- Búsqueda o filtros.
- Adjuntos.
- Integración Jira/Zammad.
- Email automático.

## Criterio de validación

R-049B se considera preparada cuando:

- `main.py` compila.
- `dasc-api` arranca.
- `/soporte` carga correctamente.
- Se crea `data/support_tickets.db`.
- El ticket previo `DASC-2026-001` aparece migrado o disponible.
- Al crear un nuevo ticket, se genera `DASC-2026-002`.
- El nuevo ticket queda guardado en SQLite.
- Se registra evento en `dasc_logs`.

## Próximo paso

Validar en `lab-pruebas` y cerrar R-049B con evidencias.

## Conclusión

R-049B prepara la base técnica para que el soporte deje de ser solo un formulario y pueda evolucionar hacia una vista interna real de tickets.
