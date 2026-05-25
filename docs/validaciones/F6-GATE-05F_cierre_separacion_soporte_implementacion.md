# F6-GATE-05F - Cierre separación soporte documentado e implementación pendiente

## Objetivo

Cerrar la separación entre soporte documentado y soporte implementado dentro de DASC Server Manager.

## Estado

Cerrada.

## Documento creado

~~~text
docs/soporte/plan_implementacion_soporte_real.md
~~~

## Validación creada

~~~text
docs/validaciones/F6-GATE-05F_separacion_soporte_documentado_implementacion.md
~~~

## Decisión principal

El soporte de DASC está avanzado a nivel documental y de proceso, pero no debe presentarse como una integración técnica completa dentro del panel.

## Estado real actual

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

La hoja de ruta contempla:

~~~text
R-049 - Montar sistema básico de tickets
~~~

Para convertir R-049 en una implementación real, se proponen subtareas concretas:

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

F6-GATE-05F se considera cerrada porque:

- Existe separación clara entre documentación e implementación.
- Se reconoce que el soporte todavía no está integrado en el panel.
- Se proponen subtareas concretas para R-049.
- Se evita vender como terminado algo que todavía es diseño documental.
- Se deja una ruta clara para implementar soporte real.

## Conclusión

DASC Server Manager mantiene una visión honesta del estado del soporte.

La base documental ya existe, pero la implementación real debe abordarse como bloque posterior mediante R-049.
