# F6-GATE-05G - Cierre global soporte real sin GitHub para cliente

## Objetivo

Cerrar globalmente F6-GATE-05, dedicada a definir un modelo de soporte realista para clientes PyME sin obligarles a usar GitHub.

## Estado

Cerrada.

## Resumen

F6-GATE-05 se ha centrado en convertir el soporte de DASC Server Manager en una parte seria del producto.

El objetivo principal ha sido separar claramente:

- Canales simples para cliente.
- Gestión interna del equipo DASC.
- Documentación de soporte.
- Herramientas futuras de ticketing.
- Implementación real pendiente en panel/API.

## Gates cerrados

| Gate | Descripción | Estado |
|---|---|---|
| F6-GATE-05A | Modelo de soporte cliente sin GitHub | Cerrada |
| F6-GATE-05B | Ticket de soporte simulado | Cerrada |
| F6-GATE-05C | Canales reales de soporte | Cerrada |
| F6-GATE-05C-PLUS | Ticketing gratuito integrado | Cerrada |
| F6-GATE-05D | Plantillas de respuesta al cliente | Cerrada |
| F6-GATE-05E | Guía de comunicación y tono | Cerrada |
| F6-GATE-05F | Separación entre soporte documentado e implementación pendiente | Cerrada |

## Documentos principales creados

~~~text
docs/soporte/modelo_soporte_cliente.md
docs/soporte/plantilla_ticket_soporte.md
docs/soporte/canales_reales_soporte.md
docs/soporte/protocolo_canales_soporte.md
docs/soporte/herramientas_ticketing_gratuitas.md
docs/soporte/plantillas_respuesta_cliente.md
docs/soporte/guia_comunicacion_tono_soporte.md
docs/soporte/plan_implementacion_soporte_real.md
docs/soporte/tickets_ejemplo/DASC-2026-001_error_acceso_panel.md
~~~

## Decisión principal

GitHub no será canal de soporte para clientes.

GitHub queda reservado para:

- Desarrollo interno.
- Roadmap técnico.
- Issues internos.
- Pull requests.
- Historial de cambios.
- Documentación técnica interna.

El cliente usará canales simples y comprensibles.

## Canales definidos para cliente

~~~text
Email
Formulario
WhatsApp controlado
Teléfono controlado
Portal futuro
~~~

## Ticketing interno recomendado

Se documentó una capa de ticketing interna o futura:

| Herramienta | Decisión |
|---|---|
| Jira Service Management Free | Recomendada inicialmente |
| Zammad self-hosted | Alternativa open source |
| Freshdesk | Reservada para fase comercial real |
| GLPI | Descartada temporalmente |

## Modelo de soporte resultante

~~~text
Cliente contacta por canal simple
        ↓
Equipo DASC registra internamente
        ↓
Se clasifica prioridad
        ↓
Se diagnostica
        ↓
Se responde con plantilla o comunicación clara
        ↓
Se cierra con evidencia
        ↓
Si aplica, se registra o exporta a Jira/Zammad
~~~

## Plantillas y comunicación

Se crearon plantillas para:

- Confirmar recepción.
- Solicitar más información.
- Informar análisis.
- Comunicar servicio operativo.
- Cerrar incidencia resuelta.
- Gestionar restauraciones.
- Avisar mantenimiento.
- Confirmar ticket interno.
- Responder por WhatsApp.

También se creó una guía de tono para evitar respuestas demasiado técnicas o poco profesionales.

## Separación honesta de estado

Se deja claro que el soporte está avanzado documentalmente, pero todavía no está completamente implementado en el panel.

Estado actual:

~~~text
Soporte documentado: Sí
Formulario real en panel: No
Sistema interno de tickets: No
Vista interna de tickets: No
Integración Jira/Zammad: No
Email automático: No
Portal cliente: No
~~~

## Relación con R-049

La hoja de ruta incluye:

~~~text
R-049 - Montar sistema básico de tickets
~~~

Para convertirlo en implementación real se proponen subtareas:

~~~text
R-049A - Formulario básico de soporte en el panel
R-049B - Guardar tickets en SQLite/JSON/DB
R-049C - Vista interna de tickets para equipo DASC
R-049D - Estados y prioridades de tickets
R-049E - Usar plantillas de respuesta desde documentación
R-049F - Exportar o copiar resumen para Jira/Zammad
R-049G - Integración futura con Jira/Zammad vía email/API
R-049H - Validación flujo cliente -> ticket -> cierre
R-049I - Documentar límites de la primera versión
~~~

## Criterio de cierre

F6-GATE-05 se considera cerrada porque:

- Existe modelo de soporte sin GitHub.
- Existen canales reales para cliente.
- Existe plantilla interna de ticket.
- Existe ticket simulado.
- Existen plantillas de respuesta.
- Existe guía de tono y comunicación.
- Se documentaron opciones gratuitas de ticketing.
- Se dejó claro qué está documentado y qué falta implementar.
- Se evita presentar como terminado algo que todavía es diseño documental.
- Se deja preparada la ruta hacia R-049.

## Próximo bloque recomendado

La siguiente fase lógica es iniciar la implementación real:

~~~text
R-049A - Formulario básico de soporte en el panel
~~~

## Conclusión

DASC Server Manager supera F6-GATE-05.

El producto ya dispone de una base profesional de soporte al cliente, aunque la integración técnica en panel debe implementarse en el bloque R-049.
