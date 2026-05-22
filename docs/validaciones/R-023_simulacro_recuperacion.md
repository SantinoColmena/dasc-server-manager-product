# Validación R-023 - Simulacro de recuperación y validación guiada

## Objetivo

Añadir un simulacro de recuperación que permita comprobar si un backup está preparado para restaurarse sin ejecutar todavía una restauración real sobre la base de datos.

## Estado inicial

Hasta R-022 el sistema ya tenía:

- Backups con historial en `history.tsv`.
- Validación de integridad con `checksums.sha256`.
- Restauración controlada con `restore_api.sh`.
- Auditoría local en `audit.log`.
- Registro de restauración en `restore.log`.

Sin embargo, faltaba una prueba intermedia tipo dry-run para validar que un backup es restaurable sin modificar la base de datos.

## Cambios realizados

- Se añade `restore_drill_api.sh`.
- El script valida un backup por ID.
- Comprueba que existe `history.tsv`.
- Comprueba que existe `checksums.sha256`.
- Comprueba que el backup está en estado `OK`.
- Comprueba que la ruta pertenece a `/home/dasc/backups`.
- Comprueba que el fichero existe y no está vacío.
- Recalcula SHA256 y lo compara con el registrado.
- Si el fichero es `.gz`, ejecuta `gzip -t`.
- Comprueba que el SQL se puede leer.
- Registra resultado en `audit.log`.
- Registra resultado en `restore_drill.log`.
- Se actualiza `install_backup_services.sh` para instalar el nuevo script.

## Archivos modificados o añadidos

- `deploy/backup-services/package/restore_drill_api.sh`
- `deploy/backup-services/install_backup_services.sh`
- `docs/validaciones/R-023_simulacro_recuperacion.md`

## Uso previsto

En la máquina de backups:

    /usr/local/bin/restore_drill_api.sh 1 /home/dasc/backups

Resultado esperado si todo está correcto:

    OK: Simulacro de recuperación validado

## Criterio de seguridad

El simulacro no debe modificar la base de datos.

Solo valida que el backup existe, es legible, está registrado y mantiene su integridad.

## Pruebas pendientes en VM Ubuntu

| Prueba | Estado |
|---|---|
| Instalar `restore_drill_api.sh` con el instalador | Pendiente |
| Crear backup de prueba | Pendiente |
| Ejecutar simulacro con ID válido | Pendiente |
| Ejecutar simulacro con ID inexistente | Pendiente |
| Alterar backup y comprobar fallo SHA256 | Pendiente |
| Comprobar entrada en `audit.log` | Pendiente |
| Comprobar entrada en `restore_drill.log` | Pendiente |
| Validación completa en VM Ubuntu | Pendiente |

## Estado de cierre

R-023 queda implementado a nivel de scripts y pendiente de validación en VM Ubuntu.
