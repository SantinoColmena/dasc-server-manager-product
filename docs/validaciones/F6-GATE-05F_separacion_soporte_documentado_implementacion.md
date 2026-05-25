# F6-GATE-05F - Separación entre soporte documentado e implementación pendiente

## Objetivo

Dejar claro qué parte del soporte de DASC Server Manager está documentada y qué parte todavía debe implementarse técnicamente.

## Estado

En curso.

## Contexto

En F6-GATE-05A se definió el modelo de soporte sin GitHub.

En F6-GATE-05B se creó un ticket simulado.

En F6-GATE-05C se definieron canales reales y ticketing gratuito.

En F6-GATE-05D se crearon plantillas de respuesta.

En F6-GATE-05E se creó una guía de comunicación y tono.

F6-GATE-05F separa documentación de implementación real.

## Documento creado

~~~text
docs/soporte/plan_implementacion_soporte_real.md
~~~

## Decisión principal

El soporte está avanzado a nivel documental, pero no debe presentarse como completamente implementado en el panel.

## Estado actual

~~~text
Soporte documentado: Sí
Formulario real en panel: No
Sistema interno de tickets: No
Vista interna de tickets: No
Integración Jira/Zammad: No
Email automático: No
Portal cliente: No
~~~

## Subtareas propuestas para R-049

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

## Criterio de validación

F6-GATE-05F se considera preparada cuando:

- Existe una separación clara entre documentación e implementación.
- Se reconoce que el soporte todavía no está integrado en panel.
- Se proponen subtareas concretas para R-049.
- Se evita vender como hecho algo que aún es diseño documental.
- Se deja una ruta clara para implementar soporte real.

## Próximo paso

Cerrar F6-GATE-05E y F6-GATE-05F, y después preparar el cierre global de F6-GATE-05 o iniciar la implementación real de R-049A.

## Conclusión

DASC Server Manager mantiene una visión honesta del estado del soporte.

La base documental ya existe, pero la implementación real debe abordarse como bloque posterior.
