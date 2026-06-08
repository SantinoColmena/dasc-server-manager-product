# Decisión - De herramientas internas en GitHub a herramientas reales para cliente

## Contexto

Durante la Fase 6 se han empezado a crear herramientas funcionales dentro del repositorio, como:

- Auditoría clean del repositorio.
- Generador de informe mensual v1.
- Plantillas internas de issues.
- Documentación de soporte.
- Documentación comercial inicial.

Estas herramientas son útiles para el equipo, pero no deben confundirse con herramientas listas para una PyME.

## Problema detectado

Una herramienta puede funcionar en GitHub o desde PowerShell y aun así no estar lista para un cliente final.

Ejemplo:

- El informe mensual v1 funciona.
- Se genera correctamente.
- Sirve para seguimiento interno.
- Pero todavía no consulta backups reales, restauraciones reales ni alertas reales.
- Tampoco se entrega automáticamente al cliente en formato claro.

Por tanto, no debe venderse todavía como informe mensual comercial final.

## Decisión

A partir de ahora, cada herramienta de Fase 6 se clasificará en tres niveles de madurez:

1. Herramienta interna funcional.
2. Herramienta de producto validada.
3. Herramienta lista para cliente.

No se debe pasar a ventas reales solo porque algo funcione en GitHub.

## Nivel 1 - Herramienta interna funcional

Una herramienta está en este nivel cuando:

- Existe en el repositorio.
- Se puede ejecutar por el equipo.
- Está documentada.
- Tiene una validación básica.
- Sirve para organizar el proyecto o comprobar el estado interno.

Ejemplos actuales:

- Auditoría clean del repositorio.
- Informe mensual v1 interno.
- GitHub Issues como tickets internos.

Este nivel es válido para el equipo, pero no para cliente final.

## Nivel 2 - Herramienta de producto validada

Una herramienta pasa a producto validado cuando:

- Funciona fuera de una prueba puramente documental.
- Está integrada con instaladores, scripts reales o el panel Vigex.
- Usa datos reales o simulados de forma representativa.
- Tiene documentación técnica clara.
- Se ha probado en entorno de laboratorio o piloto.
- No depende de que el cliente entre en GitHub.
- No expone secretos ni datos sensibles.
- Tiene límites claros.

Ejemplo para informe mensual:

- Leer estado real de backups.
- Incluir última restauración de prueba.
- Incluir alertas.
- Incluir incidencias internas.
- Generar un resumen comprensible.
- Poder ejecutarse de forma repetible.

## Nivel 3 - Herramienta lista para cliente

Una herramienta está lista para cliente cuando:

- La PyME no necesita GitHub.
- La PyME no necesita entender el repositorio.
- La PyME no necesita ejecutar comandos técnicos complejos.
- La salida está pensada para una persona no técnica.
- Existe una forma sencilla de entrega: panel, email, PDF, formulario o soporte humano.
- Está probada en un entorno parecido al real.
- Tiene instrucciones simples.
- Tiene límites comerciales claros.

Ejemplo para informe mensual final:

- El cliente recibe un PDF o resumen claro.
- El informe indica si los backups están bien.
- Indica si hubo errores.
- Indica cuándo fue la última restauración de prueba.
- Indica si hay acciones recomendadas.
- No muestra detalles internos innecesarios.

## Relación con GitHub

GitHub se usará como herramienta interna del equipo.

GitHub sirve para:

- Versionar código.
- Registrar avances.
- Crear issues internas.
- Mantener documentación técnica.
- Validar cambios.
- Preparar releases.

GitHub no será el canal del cliente.

Una PyME no debe:

- Abrir issues.
- Leer documentación técnica interna.
- Revisar commits.
- Descargar scripts manualmente desde GitHub.
- Entender ramas, tags o releases.

## Relación con soporte

El cliente usará canales sencillos:

- Email.
- Formulario.
- WhatsApp o teléfono si el plan lo permite.
- Panel de ayuda futuro.
- Portal de cliente futuro.

El equipo convertirá esas entradas en tickets internos.

## Relación con el Excel de Fase 6

La Fase 6 se sigue usando como guía, pero con esta interpretación:

| Tarea | Interpretación corregida |
|---|---|
| R-047 Release candidate | Puede cerrarse con tag y documentación técnica. |
| R-048 Primer cliente de pago | No se retoma hasta superar la puerta de producto. |
| R-049 Sistema de tickets | De momento es interno, no canal de cliente. |
| R-050 Informe mensual automático v1 | Puede cerrarse como v1 interna, no como informe comercial final. |
| R-051 Tres clientes/pilotos de pago | Solo después de producto validado y soporte claro. |
| R-052 Decisión 2027 | Solo con feedback real o validación comercial real. |

## Puerta de producto antes de vender

Antes de vender a una PyME debe cumplirse:

- Repo limpio.
- Instaladores revisados.
- Configuración de ejemplos sin secretos.
- Documentación clara.
- Uso desde Windows explicado.
- Herramientas internas separadas de herramientas de cliente.
- Soporte real definido sin obligar al cliente a usar GitHub.
- Informe mensual evolucionado hacia datos reales o claramente presentado como revisión manual.
- Alcance y límites bien explicados.

## Conclusión

Vigex puede seguir avanzando por la Fase 6, pero no debe interpretar cada herramienta interna como una herramienta final de cliente.

La venta empieza cuando el producto sea instalable, entendible, mantenible y usable por una PyME sin pasar por GitHub.
