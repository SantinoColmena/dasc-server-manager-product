# R-014 - Validación de publicación versión interna 0.1

## Objetivo

Este documento define cómo validar la publicación de la versión interna 0.1 de DASC Server Manager.

La validación busca comprobar que la Fase 1 - Núcleo estable queda cerrada correctamente y que el repositorio tiene un punto de control claro para continuar el desarrollo del producto.

## Qué se quiere validar

La versión interna 0.1 debe confirmar que el proyecto dispone de una base documental y técnica suficiente para seguir evolucionando desde el MVP académico hacia un producto-servicio orientado a PYMES.

Esta versión no debe entenderse como una versión comercial lista para clientes, sino como una versión interna de control.

## Alcance validado

La versión interna 0.1 valida:

- Documentación de configuración por perfiles.
- Diseño de instalador idempotente.
- Diseño de motor centralizado de backups.
- Diseño de historial persistente de backups.
- Diseño de programación automática de backups.
- Mejora prevista de logs internos.
- Limpieza prevista de navegación y mensajes.
- Laboratorio reproducible de pruebas.
- Cierre formal de Fase 1.

## Tareas que deben estar cerradas

| ID | Tarea | Validación esperada |
|---|---|---|
| R-006 | Configuración por perfiles | Diseño y validación documentados |
| R-007 | Instalador base idempotente | Diseño, mejoras y validación documentados |
| R-008 | Motor centralizado de backups | Diseño y validación documentados |
| R-009 | Historial persistente de backups | Diseño y validación documentados |
| R-010 | Programación automática de backups | Diseño y validación documentados |
| R-011 | Mejora de logs internos | Diseño y validación documentados |
| R-012 | Limpieza de navegación y mensajes | Diseño y validación documentados |
| R-013 | Laboratorio reproducible de pruebas | Diseño y validación documentados |
| R-014 | Publicación versión interna 0.1 | Publicación y validación documentadas |

## Comprobación del repositorio

Antes de cerrar la fase, se debe ejecutar:

~~~bash
git status
git log --oneline -10
~~~

Resultado esperado:

~~~text
working tree clean
últimos commits relacionados con Fase 1
~~~

## Comprobación de documentos

Debe existir documentación en:

~~~text
docs/tecnico/
~~~

Documentos esperados:

~~~text
r-006_configuracion_por_perfiles.md
r-006_validacion_perfiles.md
r-007_instalador_base_idempotente.md
r-007_validacion_instalador.md
r-007_mejoras_install_dasc_api.md
r-008_motor_backups_centralizado.md
r-008_validacion_motor_backups.md
r-009_historial_persistente_backups.md
r-009_validacion_historial_backups.md
r-010_programacion_automatica_backups.md
r-010_validacion_programacion_backups.md
r-011_mejora_logs_internos.md
r-011_validacion_logs_internos.md
r-012_limpieza_navegacion_mensajes.md
r-012_validacion_navegacion_mensajes.md
r-013_laboratorio_reproducible_pruebas.md
r-013_validacion_laboratorio_reproducible.md
r-014_publicacion_version_interna_0_1.md
r-014_validacion_publicacion_version_interna_0_1.md
~~~

## Validación del tag interno

Se recomienda crear un tag:

~~~text
v0.1-interna
~~~

Comando recomendado:

~~~bash
git tag -a v0.1-interna -m "Version interna 0.1 - cierre Fase 1 nucleo estable"
git push origin v0.1-interna
~~~

Resultado esperado:

- El tag queda creado en local.
- El tag queda subido a GitHub.
- Se puede identificar el punto exacto de cierre de Fase 1.

## Validación de release interna

En GitHub se puede crear una release usando el tag:

~~~text
v0.1-interna
~~~

Nombre recomendado:

~~~text
DASC Server Manager v0.1 interna - Núcleo estable
~~~

Descripción recomendada:

~~~text
Primera versión interna del repositorio de producto DASC Server Manager.

Esta versión cierra la Fase 1 - Núcleo estable e incluye documentación técnica, criterios de validación y estructura inicial para convertir el MVP académico en un producto-servicio orientado a PYMES.

No es una versión comercial ni una versión final para clientes. Es un punto de control interno para continuar el desarrollo de instaladores, backups, logs, programación automática y laboratorio reproducible.
~~~

## Riesgos revisados

Antes de cerrar la fase se debe revisar que no se haya cometido alguno de estos errores:

- Marcar como implementado algo que solo está diseñado.
- Mezclar documentación académica con documentación de producto sin contexto.
- Prometer que la versión 0.1 está lista para clientes reales.
- Subir archivos temporales.
- Dejar documentos sin commit.
- Crear el tag antes de subir todos los cambios.
- No diferenciar entre MVP entregado y evolución de producto.

## Decisión de cierre

La Fase 1 puede cerrarse si se cumple:

- R-006 a R-014 están documentadas.
- Las validaciones principales están documentadas.
- El repositorio está limpio.
- Los cambios están subidos a GitHub.
- Existe un punto de control mediante tag o release interna.

## Frase correcta de cierre

La frase recomendada para documentar el cierre es:

~~~text
La Fase 1 - Núcleo estable queda cerrada con la versión interna 0.1, que actúa como punto de control documental y técnico para continuar la evolución de DASC Server Manager como producto-servicio.
~~~

## Estado final

Estado actual: Validación documentada.

Prioridad: Alta.

Resultado:

- Fase 1 preparada para cierre.
- Versión interna 0.1 lista para ser marcada.
- Siguiente fase preparada para planificación.
