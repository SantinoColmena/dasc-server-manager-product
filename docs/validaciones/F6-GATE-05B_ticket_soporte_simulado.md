# F6-GATE-05B - Ticket de soporte simulado

## Objetivo

Validar el modelo de soporte definido en F6-GATE-05A mediante un ticket de ejemplo completo.

## Estado

En curso.

## Ticket creado

~~~text
docs/soporte/tickets_ejemplo/DASC-2026-001_error_acceso_panel.md
~~~

## Escenario simulado

Un cliente PyME contacta por email indicando que no puede acceder correctamente al panel DASC.

El equipo DASC revisa el estado del servicio, la respuesta HTTP y los logs remotos.

## Resultado del diagnóstico

Se comprueba que:

- `dasc-api` está activo.
- El panel responde con `303 See Other`.
- La redirección a `/login` es esperada.
- Los logs remotos registran eventos correctamente.
- No existe caída real del servicio.

## Flujo validado

~~~text
Cliente contacta por email
Equipo DASC registra ticket interno
Se clasifica como incidencia alta
Se revisa técnicamente
Se comunica resultado en lenguaje claro
Se cierra con evidencia
~~~

## Criterio de validación

F6-GATE-05B se considera preparada porque:

- Existe un ticket realista.
- El cliente no usa GitHub.
- La incidencia se documenta internamente.
- Se registra diagnóstico técnico.
- Se registra comunicación al cliente.
- Se cierra con evidencia.

## Próximo paso

Cerrar F6-GATE-05A y F6-GATE-05B como base del modelo de soporte inicial.

## Conclusión

El modelo de soporte sin GitHub queda validado con un caso práctico de incidencia.
