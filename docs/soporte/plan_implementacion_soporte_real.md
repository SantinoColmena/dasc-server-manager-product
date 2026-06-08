# Plan de implementación de soporte real - Vigex

## Objetivo

Separar claramente el soporte que ya está definido documentalmente del soporte que todavía debe implementarse en el producto.

## Estado actual

Vigex ya dispone de una base documental sólida para soporte al cliente.

Sin embargo, todavía no existe una implementación completa dentro del panel para gestionar tickets reales de cliente.

## Soporte documentado

Actualmente está documentado:

| Área | Estado |
|---|---|
| Modelo de soporte sin GitHub | Documentado |
| Canales de soporte | Documentado |
| Email, formulario, WhatsApp y teléfono | Documentado |
| Ticketing gratuito con Jira/Zammad | Documentado |
| Plantillas de respuesta al cliente | Documentado |
| Guía de tono y comunicación | Documentado |
| Ticket simulado | Documentado |

## Soporte implementado actualmente

Actualmente existe:

| Funcionalidad | Estado |
|---|---|
| Panel Vigex operativo | Implementado |
| Logs remotos de eventos | Implementado |
| Informes operativos básicos | Implementado |
| Registro de accesos/login/logout | Implementado |
| Plantillas de soporte dentro del repo | Documentado, no integrado en UI |
| Sistema de tickets en panel | No implementado |
| Formulario real de soporte en panel | No implementado |
| Vista interna de tickets | No implementado |
| Integración Jira/Zammad | No implementada |
| Envío automático de email | No implementado |
| Portal de cliente | No implementado |

## Decisión

El soporte diseñado en F6-GATE-05A a F6-GATE-05E debe considerarse una base de producto y proceso.

No debe presentarse como una integración técnica ya terminada.

## Relación con R-049

La hoja de ruta contempla:

~~~text
R-049 - Montar sistema básico de tickets
~~~

Para convertirlo en implementación real, se divide en subtareas más concretas.

## Subtareas propuestas para R-049

| Subtarea | Descripción | Tipo |
|---|---|---|
| R-049A | Formulario básico de soporte en el panel | Implementación |
| R-049B | Guardar tickets en SQLite/JSON/DB | Implementación |
| R-049C | Vista interna de tickets para equipo Vigex | Implementación |
| R-049D | Estados y prioridades de tickets | Implementación |
| R-049E | Usar plantillas de respuesta desde documentación | Implementación |
| R-049F | Exportar o copiar resumen para Jira/Zammad | Implementación |
| R-049G | Integración futura con Jira/Zammad vía email/API | Integración futura |
| R-049H | Validación flujo cliente -> ticket -> cierre | Validación |
| R-049I | Documentar límites de la primera versión | Documentación |

## Implementación mínima recomendada

La primera versión real debería incluir:

~~~text
Formulario de soporte en el panel
Guardado local de tickets
Vista interna sencilla
Estados: abierto, en análisis, en curso, cerrado
Prioridades: crítica, alta, media, baja
Exportación o copia de resumen para Jira/Zammad
~~~

## Implementación no recomendada todavía

Por ahora no se recomienda empezar directamente con:

~~~text
Integración completa con API de Jira
Integración completa con API de Zammad
Portal de cliente completo
Automatización avanzada por email
SLA automático complejo
Chat IA de soporte
~~~

Estas funciones son útiles, pero deben llegar después de tener un flujo básico funcionando.

## Flujo mínimo futuro

~~~text
Cliente contacta por email/formulario/WhatsApp
        ↓
Equipo Vigex crea ticket en panel o sistema interno
        ↓
Se clasifica prioridad
        ↓
Se registra diagnóstico
        ↓
Se responde con plantilla
        ↓
Se cierra con evidencia
        ↓
Si hace falta, se copia o exporta a Jira/Zammad
~~~

## Criterio para considerar R-049 implementado

R-049 podrá considerarse implementado cuando:

- Exista formulario de soporte funcional.
- Los tickets se guarden.
- El equipo Vigex pueda verlos.
- Existan estados y prioridades.
- Se pueda cerrar un ticket con evidencia.
- No se dependa de GitHub para soporte al cliente.

## Conclusión

F6-GATE-05 define el modelo de soporte.

R-049 debe convertir ese modelo en funcionalidad real del producto.

Hasta que R-049 no se implemente, el soporte está preparado a nivel documental y operativo interno, pero no integrado completamente en el panel.
