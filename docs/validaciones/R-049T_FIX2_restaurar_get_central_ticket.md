# R-049T-FIX2 - Restaurar helper de detalle de ticket central

## Objetivo

Restaurar la función auxiliar `get_central_ticket()` eliminada accidentalmente durante la sustitución del bloque dashboard en R-049T-FIX1.

## Estado

En curso.

## Problema detectado

Durante la corrección del contexto del dashboard central, el reemplazo del bloque entre el dashboard y el siguiente decorador eliminó también la función:

- get_central_ticket(ticket_id)

Esta función es necesaria para que la vista de detalle del panel central pueda cargar tickets individuales.

## Riesgo evitado

Sin esta función, el dashboard central podría cargar correctamente, pero al entrar en una ruta como:

- /tickets/CENTRAL-2026-0003

la aplicación podría fallar con error 500 por función no definida.

## Solución aplicada

Se restaura `get_central_ticket(ticket_id)` antes de la ruta:

- GET /tickets/{ticket_id}

La función vuelve a consultar la tabla `central_tickets` y devuelve el ticket como diccionario.

## Validación esperada

- main.py central compila.
- central-support arranca.
- Dashboard central carga.
- Detalle de ticket central carga.
- Cambio de estado/prioridad sigue funcionando.
