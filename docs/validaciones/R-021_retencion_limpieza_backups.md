# Validación R-021 - Retención segura y limpieza de backups

## Objetivo

Reforzar la limpieza automática de backups para que la retención no elimine ficheros de forma peligrosa ni rompa cadenas de restauración.

## Estado inicial

Antes de esta tarea, `backups_api.sh` aplicaba la retención con una eliminación directa:

    find "$DEST" -type f -mtime +"$RETENTION" -name "*.sql*" -delete

Este enfoque era simple, pero tenía riesgos:

- Podía borrar ficheros sin actualizar `history.tsv`.
- Podía dejar entradas históricas apuntando a ficheros inexistentes.
- Podía romper cadenas de restauración si se eliminaba una copia completa usada como base.
- No actualizaba el manifiesto `checksums.sha256`.

## Cambios realizados

- Se añade la función `safe_retention_cleanup()`.
- La retención solo se ejecuta dentro de `/home/dasc/backups`.
- Se valida que el valor de retención sea numérico.
- Los backups eliminados pasan a estado `PRUNED` en `history.tsv`.
- Se añade marca `pruned_at` en las notas del historial.
- Se evita eliminar backups que estén referenciados como base por otros backups activos.
- Se elimina el checksum asociado del fichero purgado.
- Se evita borrar rutas fuera del directorio permitido.
- Se sustituye el borrado directo con `find -delete`.

## Archivos modificados

- `deploy/backup-services/package/backups_api.sh`

## Criterio de seguridad

La retención automática no debe:

1. Borrar fuera de `/home/dasc/backups`.
2. Borrar una copia base necesaria para restaurar otra copia activa.
3. Dejar checksums obsoletos.
4. Dejar historial sin reflejar que el backup fue purgado.

## Pruebas pendientes en VM Ubuntu

| Prueba | Estado |
|---|---|
| Crear backups con retención activa | Pendiente |
| Comprobar que backups antiguos pasan a `PRUNED` | Pendiente |
| Comprobar que se elimina el fichero físico | Pendiente |
| Comprobar que se elimina el checksum asociado | Pendiente |
| Comprobar que una copia base referenciada no se borra | Pendiente |
| Comprobar que no se borra nada fuera de `/home/dasc/backups` | Pendiente |
| Validación completa en VM Ubuntu | Pendiente |

## Estado de cierre

R-021 queda implementado a nivel de script y pendiente de validación en VM Ubuntu.
