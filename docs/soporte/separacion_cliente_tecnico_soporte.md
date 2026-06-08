# Separación entre panel cliente y soporte técnico - Vigex

## Objetivo

Definir claramente qué debe ver un cliente y qué debe quedar reservado al equipo técnico Vigex.

## Decisión principal

La gestión interna de soporte no debe exponerse al cliente.

El cliente no debe ver:

~~~text
Todos los tickets
Historial interno técnico
Cambios internos de prioridad
Plantillas internas de respuesta
Resumen para Jira/Zammad
Notas internas
Tickets de otros clientes
Herramientas administrativas
~~~

## Acceso técnico Vigex

El equipo técnico Vigex puede acceder a:

~~~text
/soporte
/soporte/tickets
/soporte/tickets/{ticket_id}
/soporte/tickets/{ticket_id}/estado
~~~

Estas rutas se consideran internas.

## Acceso cliente

El cliente debería acceder, en una fase posterior, solo a funciones propias:

~~~text
Estado general contratado
Historial de copias
Informes mensuales
Alertas visibles
Solicitud sencilla de soporte
Estado de sus propias solicitudes
~~~

## Panel cliente futuro

El panel cliente futuro no debe ser el mismo panel de gestión técnica.

Debe ser una vista limitada y segura, por ejemplo:

~~~text
/cliente
/cliente/backups
/cliente/informes
/cliente/soporte/nuevo
/cliente/soporte/mis-tickets
~~~

## Panel técnico Vigex

El panel técnico puede mantener:

~~~text
/soporte/tickets
/soporte/tickets/{ticket_id}
/soporte/tickets/{ticket_id}/estado
/soporte/tickets/{ticket_id}/plantillas
/soporte/tickets/{ticket_id}/resumen
~~~

## Relación con Jira/Zammad

El resumen para Jira/Zammad no es una integración automática.

Es una herramienta puente para el equipo técnico.

Permite copiar manualmente un resumen técnico mientras no exista integración real con API o email.

## Decisión sobre R-049F

R-049F queda clasificada como:

~~~text
Utilidad interna manual
No integración automática
Solo para equipo técnico
Modo puente hacia Jira/Zammad
~~~

## Próximas integraciones posibles

Más adelante se podrá implementar:

~~~text
Enviar ticket por email a Jira/Zammad
Crear issue por API en Jira
Crear ticket por API en Zammad
Sincronizar estado externo
Portal cliente limitado
~~~

## Conclusión

Vigex debe separar claramente cliente y equipo técnico.

La zona de soporte implementada hasta ahora queda reservada al equipo Vigex.

## Aclaración de roles para producto real

En la validación actual se usa el rol `admin` para restringir las rutas internas de soporte.

Esta decisión es válida para laboratorio, pero no representa el modelo final de producto.

## Diferencia importante

~~~text
admin actual del panel != técnico Vigex definitivo
~~~

En un producto real deben separarse claramente:

~~~text
cliente_admin
vigex_tecnico
~~~

## cliente_admin

El `cliente_admin` pertenece a la empresa cliente.

Puede administrar aspectos internos de su propio panel, por ejemplo:

~~~text
Usuarios del cliente
Visibilidad interna
Consulta de backups
Consulta de informes
Consulta de estado
Solicitud simple de soporte
~~~

Pero no debe acceder a:

~~~text
Tickets internos de todos los clientes
Historial técnico Vigex
Resumen Jira/Zammad
Notas internas
Prioridades internas globales
Herramientas de soporte Vigex
~~~

## vigex_tecnico

El `vigex_tecnico` pertenece al equipo Vigex.

Debe trabajar desde un panel central Vigex, no entrando manualmente al panel de cada cliente para revisar incidencias.

Puede acceder a:

~~~text
Tickets centralizados
Historial técnico
Cambios de estado y prioridad
Plantillas de respuesta
Resumen para Jira/Zammad
Diagnóstico interno
Cierre con evidencia
~~~

## Decisión sobre la implementación actual

La restricción actual usando `is_admin(request)` se considera una medida temporal de laboratorio.

Sirve para validar que las rutas internas no quedan abiertas a usuarios normales.

No debe interpretarse como arquitectura final.

## Decisión de producto

La arquitectura final debe evolucionar hacia:

~~~text
Panel local del cliente
        ↓
API central Vigex
        ↓
Panel central Vigex
        ↓
Equipo técnico Vigex
~~~

El técnico Vigex no debería depender de entrar en cada panel local de cliente para ver incidencias.

Las incidencias deben centralizarse en un sistema propio de Vigex.
