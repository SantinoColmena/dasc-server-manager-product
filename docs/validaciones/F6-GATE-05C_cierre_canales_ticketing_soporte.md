# F6-GATE-05C - Cierre canales reales de soporte y ticketing gratuito

## Objetivo

Cerrar la definición de canales reales de soporte para clientes PyME y añadir una capa interna de ticketing gratuita o sin coste inicial.

## Estado

Cerrada.

## Gates cerrados

| Gate | Descripción | Estado |
|---|---|---|
| F6-GATE-05C | Canales reales de soporte y datos mínimos de contacto | Cerrada |
| F6-GATE-05C-PLUS | Ticketing gratuito integrado con canales de soporte | Cerrada |

## Documentos creados o actualizados

~~~text
docs/soporte/canales_reales_soporte.md
docs/soporte/protocolo_canales_soporte.md
docs/soporte/herramientas_ticketing_gratuitas.md
docs/validaciones/F6-GATE-05C_canales_reales_soporte.md
docs/validaciones/F6-GATE-05C_PLUS_ticketing_gratuito.md
~~~

## Canales de entrada para cliente

Se mantienen canales simples y comprensibles:

~~~text
Email
Formulario
WhatsApp controlado
Teléfono controlado
Portal futuro
~~~

## Principio principal

El cliente no necesita usar GitHub ni herramientas técnicas.

GitHub queda como herramienta interna de desarrollo.

## Capa interna de ticketing

Se añade la posibilidad de usar herramientas de ticketing internamente.

El cliente puede seguir entrando por email, formulario, WhatsApp o teléfono.

El equipo DASC puede registrar y gestionar internamente en:

~~~text
Jira Service Management Free
Zammad self-hosted
~~~

## Decisiones sobre herramientas

| Herramienta | Decisión | Motivo |
|---|---|---|
| Jira Service Management Free | Recomendada inicialmente | Profesional, conocida y viable para equipo pequeño |
| Zammad self-hosted | Alternativa | Open source y autogestionada |
| Freshdesk | Futura | Reservar periodo gratuito para etapa comercial real |
| GLPI | Descartada temporalmente | Evitar complejidad y coste operativo no validado |

## Modelo resultante

~~~text
Cliente usa canal simple
        ↓
Equipo DASC registra internamente
        ↓
Ticket se gestiona en Jira o Zammad
        ↓
Equipo DASC diagnostica y actúa
        ↓
Cliente recibe respuesta clara
        ↓
Ticket se cierra con evidencia
~~~

## Limpieza realizada

Durante la ampliación se ejecutó dos veces el bloque de documentación y se generaron secciones duplicadas.

Se corrigió con el commit:

~~~text
fix: limpiar duplicados en docs de ticketing soporte
~~~

Después de la corrección solo queda una sección de integración en:

~~~text
docs/soporte/canales_reales_soporte.md
docs/soporte/protocolo_canales_soporte.md
~~~

## Criterio de cierre

F6-GATE-05C se considera cerrada porque:

- Existen canales reales de soporte documentados.
- Se definen datos mínimos de contacto.
- Se mantiene al cliente fuera de GitHub.
- Se diferencia canal externo de gestión interna.
- Se documenta Jira como opción recomendada inicial.
- Se documenta Zammad como alternativa open source.
- Freshdesk queda reservado para fase comercial.
- GLPI queda descartado temporalmente.
- Se limpiaron duplicados de documentación.

## Próxima puerta

~~~text
F6-GATE-05D - Plantillas de respuesta al cliente
~~~

## Conclusión

DASC Server Manager ya dispone de un modelo de soporte más profesional:

- Canales simples para el cliente.
- Gestión interna ordenada.
- Posibilidad de ticketing gratuito o sin coste inicial.
- Sin dependencia de GitHub como canal de atención.
