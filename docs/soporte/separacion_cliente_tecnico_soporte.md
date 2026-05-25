# Separación entre panel cliente y soporte técnico - DASC Server Manager

## Objetivo

Definir claramente qué debe ver un cliente y qué debe quedar reservado al equipo técnico DASC.

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

## Acceso técnico DASC

El equipo técnico DASC puede acceder a:

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

## Panel técnico DASC

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

DASC Server Manager debe separar claramente cliente y equipo técnico.

La zona de soporte implementada hasta ahora queda reservada al equipo DASC.
