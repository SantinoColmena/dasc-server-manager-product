# R-014 - Publicación versión interna 0.1

## Objetivo

El objetivo de esta tarea es definir la publicación de una primera versión interna de DASC Server Manager como producto.

Esta versión no representa todavía una versión comercial ni una versión final para clientes reales. Su función es cerrar la Fase 1 con una base estable, documentada y preparada para seguir evolucionando.

La versión interna 0.1 debe servir como punto de control del proyecto.

## Qué significa versión interna 0.1

La versión interna 0.1 es una primera release de trabajo.

Su objetivo es agrupar el estado actual del producto después de completar la preparación y el núcleo estable.

Esta versión debe demostrar que el proyecto ya tiene:

- Visión de producto.
- Roadmap inicial.
- Configuración por perfiles diseñada.
- Instalador idempotente diseñado.
- Motor de backups centralizado definido.
- Historial persistente de backups diseñado.
- Programación automática de backups diseñada.
- Mejora de logs internos definida.
- Navegación y mensajes revisados.
- Laboratorio reproducible de pruebas definido.

## Alcance de la versión 0.1

La versión 0.1 no tiene que implementar todas las funciones futuras.

Su alcance principal es dejar una base clara y defendible.

Incluye:

- Documentación técnica de Fase 1.
- Documentación de validación.
- Estructura de perfiles.
- Criterios de instalación.
- Criterios de pruebas.
- Cierre de tareas R-006 a R-013.
- Preparación para futuras implementaciones.

No incluye todavía:

- Producto comercial final.
- Soporte real a clientes.
- Sistema completo de releases públicas.
- Instalador perfecto para todos los casos.
- Restauración avanzada completa.
- Agente Windows.
- Portal de soporte.

## Relación con la Fase 1

La Fase 1 se llama Núcleo estable.

Esta fase no busca añadir muchas funciones visuales nuevas, sino ordenar el proyecto para que pueda crecer sin romperse.

R-014 sirve como cierre formal de esa fase.

## Tareas incluidas en la versión 0.1

| ID | Tarea | Estado esperado |
|---|---|---|
| R-006 | Configuración por perfiles | Documentada y estructurada |
| R-007 | Instalador base idempotente | Diseñado y validado |
| R-008 | Motor centralizado de backups | Diseñado y validado |
| R-009 | Historial persistente de backups | Diseñado y validado |
| R-010 | Programación automática de backups | Diseñada y validada |
| R-011 | Mejora de logs internos | Diseñada y validada |
| R-012 | Limpieza de navegación y mensajes | Diseñada y validada |
| R-013 | Laboratorio reproducible de pruebas | Diseñado y validado |
| R-014 | Publicación versión interna 0.1 | Cierre de fase |

## Criterios para publicar la versión interna

Antes de publicar la versión interna 0.1 se debe comprobar:

- El repositorio está limpio.
- Los documentos de R-006 a R-013 existen.
- Los documentos de validación existen.
- Los cambios están subidos a GitHub.
- No quedan archivos temporales sin revisar.
- La rama principal está actualizada.
- La documentación mantiene coherencia con la visión de producto.
- La versión queda identificada mediante tag o release interna.

## Comprobaciones Git

Antes de publicar, ejecutar:

~~~bash
git status
git log --oneline -10
git branch
~~~

Resultado esperado:

~~~text
working tree clean
rama main actualizada
últimos commits relacionados con Fase 1
~~~

## Tag recomendado

Se recomienda crear un tag interno:

~~~text
v0.1-interna
~~~

Este tag permite marcar el punto exacto del repositorio donde se cierra la Fase 1.

Comando recomendado:

~~~bash
git tag -a v0.1-interna -m "Version interna 0.1 - cierre Fase 1 nucleo estable"
git push origin v0.1-interna
~~~

## Nombre de la release

Nombre recomendado:

~~~text
DASC Server Manager v0.1 interna - Núcleo estable
~~~

## Descripción recomendada de la release

Texto recomendado:

~~~text
Primera versión interna del repositorio de producto DASC Server Manager.

Esta versión cierra la Fase 1 - Núcleo estable e incluye documentación técnica, criterios de validación y estructura inicial para convertir el MVP académico en un producto-servicio orientado a PYMES.

No es una versión comercial ni una versión final para clientes. Es un punto de control interno para continuar el desarrollo de instaladores, backups, logs, programación automática y laboratorio reproducible.
~~~

## Checklist previo a la publicación

Antes de marcar R-014 como completada, revisar:

- [ ] R-006 documentada.
- [ ] R-006 validada.
- [ ] R-007 documentada.
- [ ] R-007 validada.
- [ ] R-008 documentada.
- [ ] R-008 validada.
- [ ] R-009 documentada.
- [ ] R-009 validada.
- [ ] R-010 documentada.
- [ ] R-010 validada.
- [ ] R-011 documentada.
- [ ] R-011 validada.
- [ ] R-012 documentada.
- [ ] R-012 validada.
- [ ] R-013 documentada.
- [ ] R-013 validada.
- [ ] Repositorio limpio.
- [ ] Cambios subidos a GitHub.
- [ ] Tag interno creado.
- [ ] Release interna documentada.

## Riesgos antes de publicar

Riesgos a revisar:

- Documentación duplicada.
- Incoherencias entre tareas.
- Tareas marcadas como implementadas cuando solo están diseñadas.
- Archivos temporales añadidos por error.
- Mezcla entre documentación académica y documentación de producto.
- Prometer funciones que todavía no existen.

## Decisión importante

La versión 0.1 debe presentarse como una versión interna de producto, no como una versión final.

Esto evita confusión y mantiene expectativas realistas.

La frase correcta sería:

~~~text
Versión interna 0.1: base documental y técnica para continuar el desarrollo del producto.
~~~

No sería correcto decir:

~~~text
Versión 0.1 lista para clientes reales.
~~~

## Resultado esperado

Al cerrar R-014, el proyecto debe tener un punto de control claro.

A partir de aquí se podrá avanzar hacia:

- Implementación práctica de mejoras.
- Refactor real de instaladores.
- Mejoras de backup.
- Historial persistente real.
- Scheduler real.
- Pruebas en laboratorio.
- Futuras versiones 0.2, 0.3 y pilotos.

## Estado

Estado actual: Pendiente de publicación.

Prioridad: Alta.

Dependencias:

- R-006
- R-007
- R-008
- R-009
- R-010
- R-011
- R-012
- R-013

Bloque siguiente:

- Cierre de Fase 1.
- Preparación de Fase 2.
