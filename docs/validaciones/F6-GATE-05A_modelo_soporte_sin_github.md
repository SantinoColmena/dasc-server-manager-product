# F6-GATE-05A - Modelo de soporte cliente sin GitHub

## Objetivo

Definir un modelo de soporte para clientes reales donde GitHub no sea el canal de atención al cliente.

## Estado

En curso.

## Contexto

DASC Server Manager evoluciona de MVP académico a base de producto.

En un producto para PyMEs, el cliente no debe depender de GitHub para reportar incidencias o solicitar soporte.

## Documentos creados

~~~text
docs/soporte/modelo_soporte_cliente.md
docs/soporte/plantilla_ticket_soporte.md
~~~

## Decisión principal

GitHub queda como herramienta interna del equipo DASC.

El cliente usará canales sencillos:

- Email.
- Formulario.
- WhatsApp o teléfono controlado.
- Portal futuro.

## Flujo definido

~~~text
Cliente contacta por canal simple
Equipo DASC registra ticket interno
Se clasifica prioridad
Se actúa o planifica intervención
Se comunica resultado al cliente
Se cierra con evidencia
~~~

## Criterio de validación

F6-GATE-05A se considera preparada cuando:

- Existe modelo de soporte documentado.
- Queda claro que GitHub no es canal de cliente.
- Existen canales recomendados.
- Existe plantilla interna de ticket.
- Se diferencia comunicación cliente de gestión técnica interna.

## Próximo paso

Validar el modelo creando un ejemplo de ticket realista.

## Conclusión

F6-GATE-05A inicia el paso desde un proyecto técnico hacia un servicio gestionado con soporte real para cliente PyME.
