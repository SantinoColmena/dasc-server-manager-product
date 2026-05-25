# F6-GATE-05C-PLUS - Ticketing gratuito integrado con canales de soporte

## Objetivo

Ampliar F6-GATE-05C incorporando herramientas gratuitas o sin coste inicial para gestionar tickets internamente sin eliminar los canales simples para el cliente.

## Estado

En curso.

## Contexto

En F6-GATE-05C se definieron los canales reales de soporte:

~~~text
Email
Formulario
WhatsApp controlado
Teléfono controlado
Portal futuro
~~~

Después se decide añadir una capa interna de ticketing.

## Decisión

Los canales de entrada se mantienen.

El cliente no necesita conocer ni usar la herramienta interna.

El equipo DASC podrá gestionar internamente los tickets con:

~~~text
Jira Service Management Free
Zammad self-hosted
~~~

## Herramientas evaluadas

| Herramienta | Decisión | Motivo |
|---|---|---|
| Jira Service Management Free | Recomendada inicialmente | Profesional, conocida y válida para equipo pequeño |
| Zammad self-hosted | Alternativa | Open source y autogestionada |
| Freshdesk | Futura | Interesa reservar su periodo gratuito para etapa comercial real |
| GLPI | Descartada temporalmente | Puede ser útil, pero añade complejidad y no es necesaria ahora |

## Modelo resultante

~~~text
Cliente usa canales simples
        ↓
Equipo DASC registra internamente
        ↓
Ticket se gestiona en Jira o Zammad
        ↓
Equipo DASC responde al cliente
        ↓
Ticket se cierra con evidencia
~~~

## Criterio de validación

F6-GATE-05C-PLUS se considera preparada cuando:

- Se documenta Jira como opción inicial recomendada.
- Se documenta Zammad como alternativa open source.
- Se mantiene email, formulario, WhatsApp y teléfono como canales de cliente.
- Freshdesk queda reservado para fase comercial.
- GLPI queda descartado temporalmente.
- GitHub sigue fuera del soporte al cliente.

## Próximo paso

Crear plantillas de respuesta al cliente para confirmar recepción, pedir más información y cerrar incidencias.

## Conclusión

DASC Server Manager mejora su modelo de soporte con una capa profesional de ticketing, manteniendo canales simples para el cliente y sin asumir costes iniciales innecesarios.
