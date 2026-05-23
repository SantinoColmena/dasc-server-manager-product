# R-047 - Cierre de release candidate v1.0-rc1

## Tarea

Publicar versión 1.0 candidata.

## Estado

Cerrada.

## Versión candidata

`v1.0-rc1`

## Trabajo realizado

Durante R-047 se ha preparado una versión candidata de DASC Server Manager orientada a primeras ventas, pilotos de pago o primer cliente real.

Se han realizado las siguientes acciones:

- Creación de documentación específica de release candidate.
- Creación de validación técnica de R-047.
- Actualización del README principal del repositorio.
- Marcado del proyecto como Fase 6 - Primeras ventas.
- Definición de `v1.0-rc1` como versión candidata actual.
- Confirmación de que el repositorio queda limpio antes de crear el tag.

## Commits relacionados

- `docs: preparar release candidate v1.0 rc1`
- `docs: actualizar readme para fase 6`

## Alcance confirmado

La versión candidata incluye:

- Instaladores del panel/API.
- Instalador de base de datos.
- Instalador del nodo de backups y servicios.
- Documentación de perfiles Lite, PyME y Pro.
- Backups.
- Restauración.
- Historial.
- Validaciones SHA256.
- Logs.
- Alertas.
- Documentación de SLA.
- Costes reales.
- Checklist de instalación.
- Documentación de soporte inicial.

## Limitaciones

Esta versión no se considera una versión final de producción.

No promete:

- Soporte ilimitado.
- Recuperación garantizada en cualquier escenario.
- Instalación sin validación previa.
- Cumplimiento legal automático.
- Uso en producción crítica sin revisión previa del entorno.

## Criterio de salida

R-047 se considera cerrada porque:

- Existe documentación de release candidate.
- Existe validación específica.
- El README está actualizado a Fase 6.
- El repositorio queda limpio.
- La versión candidata `v1.0-rc1` está preparada para etiquetarse.
- La versión puede usarse como base para R-048, R-049 y R-050.

## Siguiente paso

Crear el tag:

~~~powershell
git tag -a v1.0-rc1 -m "Release candidate v1.0-rc1"
git push origin v1.0-rc1
~~~

## Conclusión

R-047 queda cerrada.

DASC Server Manager dispone de una primera release candidate preparada para iniciar el bloque de primeras ventas.
