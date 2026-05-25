# R-049A - Formulario básico de soporte en el panel

## Objetivo

Implementar una primera versión funcional de formulario de soporte dentro del panel DASC.

## Estado

Cerrada.

## Contexto

F6-GATE-05 dejó definido el modelo de soporte sin GitHub.

R-049A inicia la implementación real dentro del producto.

## Cambios aplicados

Se añaden rutas en:

~~~text
deploy/api/package/main.py
~~~

Rutas nuevas:

~~~text
GET /soporte
POST /soporte
~~~

Se añade plantilla:

~~~text
deploy/api/package/templates/soporte.html
~~~

Se añade acceso desde:

~~~text
deploy/api/package/templates/index.html
~~~

## Funcionamiento

El usuario autenticado puede crear una solicitud de soporte indicando:

- Empresa.
- Persona de contacto.
- Email.
- Teléfono opcional.
- Tipo de solicitud.
- Prioridad percibida.
- Servicio afectado.
- Descripción.
- Evidencia opcional.

## Almacenamiento inicial

Los tickets se guardan localmente en:

~~~text
data/support_tickets.json
~~~

## Identificador de ticket

El sistema genera identificadores internos:

~~~text
DASC-YYYY-NNN
~~~

Ejemplo:

~~~text
DASC-2026-001
~~~

## Límites de esta primera versión

Esta versión no incluye todavía:

- Edición de tickets.
- Cambio de estado.
- Vista avanzada interna.
- Adjuntos reales.
- Envío de email.
- Integración Jira/Zammad.
- Portal cliente.

## Criterio de validación

R-049A se considera preparada cuando:

- `/soporte` carga correctamente.
- El formulario permite crear un ticket.
- El ticket queda guardado en `data/support_tickets.json`.
- El panel muestra los últimos tickets.
- La API registra el evento de soporte en logs.
- El acceso está protegido por sesión.

## Próximo paso

Validar en `lab-pruebas` copiando los cambios al paquete instalado y creando un ticket real de prueba.

## Conclusión

R-049A convierte el modelo de soporte documentado en una primera funcionalidad real dentro del panel.
