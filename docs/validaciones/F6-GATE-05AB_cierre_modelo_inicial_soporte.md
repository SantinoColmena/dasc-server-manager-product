# F6-GATE-05AB - Cierre modelo inicial de soporte sin GitHub

## Objetivo

Cerrar la primera parte de F6-GATE-05, centrada en definir un modelo de soporte al cliente donde GitHub no sea el canal de atención para PyMEs.

## Estado

Cerrada.

## Gates cerrados

| Gate | Descripción | Estado |
|---|---|---|
| F6-GATE-05A | Modelo de soporte cliente sin GitHub | Cerrada |
| F6-GATE-05B | Ticket de soporte simulado | Cerrada |

## Documentos creados

~~~text
docs/soporte/modelo_soporte_cliente.md
docs/soporte/plantilla_ticket_soporte.md
docs/soporte/tickets_ejemplo/DASC-2026-001_error_acceso_panel.md
docs/validaciones/F6-GATE-05A_modelo_soporte_sin_github.md
docs/validaciones/F6-GATE-05B_ticket_soporte_simulado.md
~~~

## Decisión principal

GitHub queda reservado como herramienta interna del equipo DASC.

El cliente no debe usar GitHub Issues, Pull Requests ni repositorios para solicitar soporte.

## Canales definidos

El modelo inicial contempla:

- Email de soporte.
- Formulario de soporte.
- WhatsApp o teléfono controlado.
- Portal de cliente futuro.

## Flujo validado

~~~text
Cliente contacta por canal simple
Equipo DASC registra ticket interno
Se clasifica la solicitud
Se realiza diagnóstico
Se comunica el resultado al cliente
Se cierra con evidencia
~~~

## Ticket simulado

Se creó el ticket:

~~~text
DASC-2026-001 - Error de acceso al panel
~~~

El ticket valida un caso realista donde el cliente interpreta la redirección a `/login` como posible fallo.

Resultado del diagnóstico:

- API activa.
- Panel responde.
- Redirección a `/login` esperada.
- Logs remotos funcionando.
- Incidencia cerrada con explicación clara al cliente.

## Criterio de cierre

F6-GATE-05A/B se considera cerrado porque:

- Existe modelo de soporte documentado.
- Existe plantilla interna de ticket.
- Existe ticket de ejemplo completo.
- El cliente no usa GitHub.
- El equipo DASC registra y gestiona internamente.
- La comunicación al cliente se redacta en lenguaje claro.
- El cierre incluye evidencias.

## Próxima puerta

~~~text
F6-GATE-05C - Canales reales de soporte y datos mínimos de contacto
~~~

## Conclusión

DASC Server Manager ya tiene una base inicial de soporte orientada a cliente PyME.

El modelo separa correctamente la comunicación externa sencilla de la gestión técnica interna.
