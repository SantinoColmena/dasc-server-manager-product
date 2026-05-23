# R-049 - Cierre del sistema básico de tickets

## Tarea

Montar sistema básico de tickets.

## Estado

Cerrada.

## Objetivo

Evitar que las incidencias, solicitudes de soporte y tareas relacionadas con clientes queden perdidas en conversaciones informales como WhatsApp, mensajes sueltos o notas sin seguimiento.

## Trabajo realizado

Durante R-049 se ha creado un sistema básico de tickets usando GitHub Issues.

Se han añadido:

- Configuración general de Issues.
- Plantilla de incidencia técnica.
- Plantilla de solicitud de soporte.
- Documento de funcionamiento del sistema de tickets.
- Validación específica de R-049.

## Archivos creados

~~~text
.github/ISSUE_TEMPLATE/config.yml
.github/ISSUE_TEMPLATE/incidencia.yml
.github/ISSUE_TEMPLATE/solicitud_soporte.yml
docs/soporte/sistema_tickets.md
docs/validaciones/R-049_validacion_sistema_tickets.md
~~~

## Decisión adoptada

Se usará GitHub Issues como sistema inicial de tickets.

Motivos:

- No añade coste mensual.
- Ya está integrado en el repositorio.
- Permite historial.
- Permite clasificar incidencias.
- Permite diferenciar fallos técnicos y solicitudes de soporte.
- Permite evitar soporte desordenado por WhatsApp.
- Es suficiente para la primera fase comercial.

## Alcance cubierto

El sistema permite registrar:

- Fallos técnicos.
- Problemas de instalación.
- Incidencias de backups.
- Incidencias de restauración.
- Problemas de logs.
- Problemas de alertas.
- Problemas de servicios.
- Solicitudes de soporte.
- Revisiones mensuales.
- Cambios menores.

## Límites

Este sistema no incluye todavía:

- Portal privado de cliente.
- SLA automático.
- Automatización de tiempos de respuesta.
- Integración con correo.
- Integración con IA.
- Sistema externo tipo Jira, Freshdesk o Zendesk.
- Panel interno avanzado de soporte.

## Reglas de seguridad

No se deben incluir en tickets:

- Contraseñas.
- Tokens.
- Claves privadas.
- Backups reales.
- Datos personales.
- Datos sensibles de clientes.
- Capturas con información confidencial.

## Criterio de salida

R-049 se considera cerrada porque:

- Existen plantillas de Issues.
- Existe documentación del sistema.
- Existe validación específica.
- El flujo de soporte queda definido.
- El repositorio queda limpio tras el commit.
- El sistema ya puede usarse en R-048, R-050 y futuros pilotos/clientes.

## Commit relacionado

~~~text
docs: montar sistema basico de tickets
~~~

## Conclusión

R-049 queda cerrada.

A partir de este punto, cualquier incidencia o solicitud de soporte relacionada con DASC Server Manager deberá registrarse como ticket.
