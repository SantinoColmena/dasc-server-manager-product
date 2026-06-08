# Herramientas gratuitas de ticketing para soporte Vigex

## Objetivo

Definir qué herramientas de ticketing puede usar Vigex sin depender inicialmente de planes de pago.

## Principio

Los canales de entrada del cliente siguen siendo simples:

~~~text
Email
Formulario
WhatsApp controlado
Teléfono controlado
Portal futuro
~~~

Las herramientas de ticketing se usan internamente para organizar, clasificar y cerrar solicitudes.

## Diferencia entre canal y herramienta

| Elemento | Uso | Lo ve el cliente |
|---|---|---|
| Email | Entrada de solicitudes | Sí |
| Formulario | Entrada estructurada de solicitudes | Sí |
| WhatsApp | Comunicación rápida | Sí |
| Teléfono | Urgencias o coordinación | Sí |
| Jira / Zammad | Gestión interna de tickets | No necesariamente |

## Opción 1 - Jira Service Management Free

## Uso recomendado

Opción inicial recomendada para Vigex.

Motivos:

- Es conocido y profesional.
- Permite empezar sin coste con un equipo pequeño.
- Permite portal de cliente.
- Permite entrada por email.
- Permite formularios, colas y estados.
- Permite trabajar con tickets sin exponer GitHub al cliente.

## Encaje con Vigex

~~~text
Cliente envía email o formulario
        ↓
Jira crea o centraliza la solicitud
        ↓
Equipo Vigex clasifica el ticket
        ↓
Equipo Vigex trabaja internamente
        ↓
Cliente recibe respuesta clara
        ↓
Ticket se cierra con evidencia
~~~

## Uso con 1-2 agentes

Para el estado actual de Vigex, Jira Free encaja porque el equipo de soporte inicial sería pequeño.

Ejemplo:

~~~text
Agente 1: Santino
Agente 2: colaborador Vigex
~~~

## Ventajas

- Muy conocido.
- Profesional de cara a futuro.
- Escalable.
- Buen punto de partida para soporte organizado.
- Se puede usar sin que el cliente conozca GitHub.

## Limitaciones

- Si el equipo crece, puede requerir plan de pago.
- Algunas funciones avanzadas pueden estar limitadas.
- Depende de Atlassian Cloud si se usa en modo SaaS.

## Decisión

Jira Service Management Free queda como opción recomendada inicial para gestionar tickets de soporte Vigex.

## Opción 2 - Zammad self-hosted

## Uso recomendado

Alternativa libre y autogestionada.

Motivos:

- Es open source.
- Puede instalarse en servidor propio.
- No depende inicialmente de licencia de pago.
- Permite gestionar tickets de soporte.
- Permite mantener más control sobre datos e infraestructura.

## Encaje con Vigex

~~~text
Cliente contacta por email o formulario
        ↓
Zammad centraliza la incidencia
        ↓
Equipo Vigex gestiona el ticket
        ↓
Se responde y documenta
        ↓
Se cierra con evidencia
~~~

## Ventajas

- Open source.
- Control propio.
- Buena opción si se quiere evitar SaaS.
- Puede integrarse con correo.

## Limitaciones

Aunque no tenga coste de licencia inicial, sí requiere:

- Servidor.
- Instalación.
- Backups.
- Actualizaciones.
- Seguridad.
- Mantenimiento.

## Decisión

Zammad queda como alternativa gratuita/autogestionada para una fase posterior o para laboratorio.

## Opción 3 - Freshdesk

## Uso recomendado

No se adopta ahora como base.

Se reserva para una fase comercial real.

## Motivo

Freshdesk puede ser útil para aprovechar un periodo gratuito cuando Vigex esté cerca de vender o pilotar con clientes reales.

## Decisión

Freshdesk queda como opción futura, no como herramienta inicial.

## Opción descartada temporalmente - GLPI

## Motivo

GLPI puede ser interesante para ITSM, inventario y soporte, pero ahora no se adopta por prudencia.

Razones:

- No se quiere añadir complejidad antes de tiempo.
- No se ha validado coste operativo real.
- Vigex todavía está priorizando soporte simple y ticketing básico.

## Decisión

GLPI queda descartado temporalmente.

Podrá reevaluarse si Vigex necesita inventario IT, CMDB o gestión más avanzada de activos.

## Estrategia recomendada

## Fase actual

~~~text
Email + formulario + plantilla interna
Jira Service Management Free como opción profesional inicial
~~~

## Fase laboratorio opcional

~~~text
Evaluar Zammad self-hosted
~~~

## Fase comercial real

~~~text
Evaluar Freshdesk aprovechando periodo gratuito
Revisar si Jira Free sigue siendo suficiente
Valorar Zammad si se quiere autogestión
~~~

## Conclusión

Vigex puede mantener canales sencillos para clientes y usar herramientas gratuitas o sin coste inicial para organizar soporte internamente.

La opción inicial más recomendable es Jira Service Management Free.

La alternativa libre/autogestionada es Zammad.

Freshdesk se reserva para el momento de venta real.
