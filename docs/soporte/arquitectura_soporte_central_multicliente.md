# Arquitectura de soporte central multi-cliente - DASC Server Manager

## Objetivo

Definir la arquitectura objetivo para que DASC Server Manager pueda gestionar incidencias de varios clientes desde un panel central propio.

## Decisión principal

DASC no dependerá inicialmente de Jira, Zammad ni Freshdesk como núcleo del soporte.

DASC tendrá un panel central propio.

Las herramientas externas podrán añadirse más adelante como integraciones opcionales.

## Principio de coste

La evolución del producto seguirá esta regla:

~~~text
Implementar primero todo lo que pueda hacerse sin coste de licencia.
Pausar o documentar cualquier parte que requiera pago.
Retomar partes de pago cuando el proyecto tenga clientes reales o presupuesto.
~~~

## Arquitectura objetivo

~~~text
Panel DASC Cliente A
Panel DASC Cliente B
Panel DASC Cliente C
        ↓
API central DASC
        ↓
Panel central DASC
        ↓
Equipo técnico DASC
        ↓
Opcional: Jira / Zammad / Email / WhatsApp / Portal futuro
~~~

## Panel local del cliente

El panel instalado en cada cliente debe centrarse en funciones propias del cliente:

~~~text
Estado general del servicio
Historial de copias
Últimos backups
Informes mensuales
Alertas visibles para el cliente
Solicitud simple de soporte
Estado de sus propias solicitudes
~~~

El cliente no debe ver:

~~~text
Tickets de otros clientes
Historial técnico interno
Notas internas del equipo DASC
Resumen Jira/Zammad
Prioridades internas reales
Herramientas administrativas globales
Tokens de integración
Configuración central
~~~

## Panel central DASC

El panel central DASC será usado por el equipo técnico.

Debe permitir:

~~~text
Ver clientes registrados
Ver tickets de todos los clientes
Filtrar por cliente
Filtrar por estado
Filtrar por prioridad
Consultar historial técnico
Usar plantillas de respuesta
Generar resumen Jira/Zammad
Registrar acciones internas
Cerrar tickets con evidencia
Consultar alertas centralizadas
Consultar informes operativos por cliente
~~~

## Roles del cliente

~~~text
cliente_admin
cliente_operador
cliente_lector
~~~

| Rol | Uso |
|---|---|
| cliente_admin | Administra usuarios y visibilidad dentro del cliente |
| cliente_operador | Consulta estado y ejecuta acciones permitidas |
| cliente_lector | Solo consulta estado, backups e informes |

## Roles internos DASC

~~~text
dasc_tecnico
dasc_admin
dasc_superadmin
~~~

| Rol | Uso |
|---|---|
| dasc_tecnico | Gestiona incidencias y soporte |
| dasc_admin | Gestiona clientes, técnicos, tickets e informes |
| dasc_superadmin | Configura plataforma, integraciones y seguridad global |

## Flujo recomendado de incidencia

~~~text
Cliente crea solicitud simple en su panel local
        ↓
Panel local envía incidencia a API central DASC
        ↓
API central valida token del cliente
        ↓
API central registra ticket
        ↓
Panel central DASC muestra el ticket
        ↓
Técnico DASC clasifica, responde y actúa
        ↓
Cliente recibe actualización por canal acordado
~~~

## Seguridad mínima requerida

La API central debe usar:

~~~text
HTTPS
Token por cliente
Identificador de cliente
Control de origen
Logs de recepción
Validación de campos
Estados de entrega
Rotación futura de tokens
~~~

## Datos mínimos enviados por cliente

~~~text
cliente_id
nombre_cliente
ticket_local_id
tipo
prioridad
servicio
descripcion
evidencia
contacto
email
fecha_origen
version_panel
origen
token_cliente
~~~

## Coste cero ahora

Se puede implementar ahora sin pagar:

~~~text
Prototipo local del panel central
API central en FastAPI
Base SQLite central
Registro de clientes demo
Tokens locales de laboratorio
Recepción de incidencias desde curl o panel local
Vista técnica central
Documentación de despliegue
Validación en laboratorio
~~~

## Partes que se dejan en pausa si requieren pago

~~~text
Dominio público real
VPS público permanente
Correo profesional de soporte
Plan Jira de pago
Plan Zammad hosted de pago
WhatsApp Business API
SMS
Monitorización externa comercial
SLA contractual real
~~~

## Jira y Zammad

Jira y Zammad no serán obligatorios para que DASC funcione.

Se consideran integraciones opcionales futuras:

~~~text
Exportación manual
Envío por email
Integración API
Sincronización avanzada
~~~

## Decisión sobre lo implementado hasta ahora

El módulo actual de soporte en `/soporte` se considera:

~~~text
Prototipo funcional de soporte
Base técnica reutilizable
No arquitectura final multi-cliente
No panel cliente definitivo
No integración real con Jira/Zammad
~~~

Debe evolucionar hacia:

~~~text
Panel central DASC
API central
Recepción multi-cliente
Roles separados
Panel cliente limitado
~~~

## Fases propuestas

## Fase 1 - Diseño y prototipo sin coste

~~~text
Documentar arquitectura central
Crear estructura de panel central
Crear base central SQLite
Crear modelo de clientes
Crear modelo de tickets centralizados
Crear API de recepción local
Validar con curl
~~~

## Fase 2 - Integración con panel local

~~~text
El panel local genera solicitud
El panel local envía a API central
Se valida token
Se crea ticket central
Se mantiene ticket local de referencia
~~~

## Fase 3 - Panel técnico central

~~~text
Listado de clientes
Listado de tickets
Detalle de ticket
Estado y prioridad
Historial interno
Plantillas
Resumen externo
~~~

## Fase 4 - Integraciones opcionales

~~~text
Email automático
Jira API
Zammad API
WhatsApp Business
Portal cliente externo
~~~

## Conclusión

La arquitectura recomendada para DASC Server Manager es un panel central propio multi-cliente.

Esto permite vender DASC como servicio gestionado, sin depender desde el inicio de herramientas externas de pago.
