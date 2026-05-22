# Validación R-020 - Validación de integridad de backups

## Objetivo

Añadir comprobaciones de integridad a los backups generados por DASC Server Manager y evitar restauraciones de ficheros corruptos, vacíos o no registrados correctamente.

## Estado inicial

La restauración controlada quedó preparada en R-019 mediante `restore_api.sh`.

Sin embargo, todavía faltaba una comprobación de integridad del fichero antes de restaurar.

## Cambios realizados

- `backups_api.sh` comprueba que el fichero generado existe y no está vacío.
- Si el backup está comprimido con gzip, se valida con `gzip -t`.
- Se calcula un hash SHA256 de cada backup generado.
- Se registra el hash en:

    /home/dasc/backups/.dasc/checksums.sha256

- Se añade información de integridad al campo de notas del historial.
- `restore_api.sh` comprueba que existe el manifiesto `checksums.sha256`.
- `restore_api.sh` busca el hash esperado del backup seleccionado.
- `restore_api.sh` recalcula el SHA256 real antes de restaurar.
- Si el hash no coincide, la restauración se cancela.
- Si el fichero gzip no supera `gzip -t`, la restauración se cancela.
- Se registra el resultado de integridad en `restore.log`.

## Archivos modificados

- `deploy/backup-services/package/backups_api.sh`
- `deploy/backup-services/package/restore_api.sh`

## Criterio de seguridad

La restauración solo debe ejecutarse si:

1. El backup existe.
2. El backup no está vacío.
3. El backup está dentro de `/home/dasc/backups`.
4. El backup tiene checksum registrado.
5. El SHA256 actual coincide con el SHA256 registrado.
6. Si está comprimido, supera `gzip -t`.

## Pruebas pendientes en VM Ubuntu

| Prueba | Estado |
|---|---|
| Crear backup y comprobar SHA256 en `checksums.sha256` | Pendiente |
| Comprobar que el backup no está vacío | Pendiente |
| Comprobar `gzip -t` en backup comprimido | Pendiente |
| Restaurar backup válido | Pendiente |
| Alterar un backup y comprobar que la restauración falla | Pendiente |
| Borrar checksum y comprobar que la restauración falla | Pendiente |
| Revisar `restore.log` | Pendiente |
| Validación completa en VM Ubuntu | Pendiente |

## Estado de cierre

R-020 queda implementado a nivel de scripts y pendiente de validación en VM Ubuntu.
