# F6-GATE-05C - Canales reales de soporte y datos mínimos de contacto

## Objetivo

Definir los canales reales mínimos para que un cliente PyME pueda solicitar soporte sin usar GitHub.

## Estado

En curso.

## Contexto

En F6-GATE-05A se definió el modelo de soporte sin GitHub.

En F6-GATE-05B se validó el modelo mediante un ticket simulado.

F6-GATE-05C concreta los canales reales y los datos mínimos que debe recoger el equipo DASC.

## Documentos creados

~~~text
docs/soporte/canales_reales_soporte.md
docs/soporte/protocolo_canales_soporte.md
~~~

## Canales definidos

| Canal | Uso |
|---|---|
| Email | Canal base de soporte |
| Formulario | Recogida estructurada de solicitudes |
| WhatsApp controlado | Comunicación rápida opcional |
| Teléfono controlado | Urgencias o planes superiores |
| Portal futuro | Evolución a medio plazo |

## Datos mínimos definidos

~~~text
Cliente
Persona de contacto
Canal de respuesta
Servicio afectado
Descripción
Prioridad percibida
Fecha/hora del problema
Evidencia si existe
~~~

## Decisión principal

El cliente puede contactar por canales sencillos.

El equipo DASC registra internamente el caso y lo convierte en trabajo técnico controlado.

## Criterio de validación

F6-GATE-05C se considera preparada cuando:

- Existen canales de soporte documentados.
- Están definidos los datos mínimos de contacto.
- Se diferencia uso de email, formulario, WhatsApp, teléfono y portal futuro.
- Se indica que toda solicitud debe terminar registrada internamente.
- GitHub sigue quedando fuera del canal de cliente.

## Próximo paso

Crear una plantilla de respuesta al cliente para confirmar recepción y clasificación de incidencias.

## Conclusión

DASC Server Manager avanza hacia un modelo de servicio gestionado con canales de soporte comprensibles para clientes PyME.
