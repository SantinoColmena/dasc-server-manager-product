# Validación R-022 - Auditoría de operaciones críticas

## Objetivo

Añadir una auditoría local normalizada para operaciones críticas relacionadas con backups, integridad, retención y restauración.

## Estado inicial

Antes de esta tarea existían varios registros parciales:

- `history.tsv` para historial de backups.
- `checksums.sha256` para integridad.
- `restore.log` para restauraciones.
- Logs del panel mediante `log_event()`.
- Alertas mediante `emit_alert()`.

Sin embargo, faltaba un registro local unificado y fácil de revisar para operaciones críticas ejecutadas desde los scripts.

## Cambios realizados

- Se añade `audit.log` en:

    /home/dasc/backups/.dasc/audit.log

- Se añade función `audit_log()` en `backups_api.sh`.
- Se añade función `audit_log()` en `restore_api.sh`.
- Se registra creación de backups.
- Se registra validación de integridad de backups.
- Se registra purgado por retención segura.
- Se registran avisos cuando una ruta no se borra por estar fuera del directorio permitido.
- Se registra inicio de restauración.
- Se registra restauración correcta.
- Se registra error de restauración.
- Se registra error de integridad antes de restaurar.

## Archivos modificados

- `deploy/backup-services/package/backups_api.sh`
- `deploy/backup-services/package/restore_api.sh`

## Formato de auditoría

Cada línea de auditoría usa pares clave-valor:

    timestamp=... action=... result=... id=... file=...

Ejemplos esperados:

    timestamp=2026-05-22T19:00:00+02:00 action=backup.create result=OK id=1 type=full db=employees file=/home/dasc/backups/full.sql.gz
    timestamp=2026-05-22T19:00:01+02:00 action=backup.integrity result=OK id=1 sha256=... file=/home/dasc/backups/full.sql.gz
    timestamp=2026-05-22T19:10:00+02:00 action=backup.restore.start result=OK id=1 db=employees file=/home/dasc/backups/full.sql.gz
    timestamp=2026-05-22T19:10:05+02:00 action=backup.restore result=OK id=1 db=employees file=/home/dasc/backups/full.sql.gz

## Criterio de seguridad

Las operaciones críticas deben dejar evidencia técnica local aunque no haya conexión con la base de datos de logs del panel.

La auditoría local no sustituye a los logs del panel ni a las alertas, pero sirve como evidencia adicional en la máquina de backups.

## Pruebas pendientes en VM Ubuntu

| Prueba | Estado |
|---|---|
| Crear backup y comprobar entrada `backup.create` | Pendiente |
| Comprobar entrada `backup.integrity` | Pendiente |
| Ejecutar retención y comprobar entrada `backup.prune` | Pendiente |
| Restaurar backup y comprobar `backup.restore.start` | Pendiente |
| Restaurar backup y comprobar `backup.restore` OK | Pendiente |
| Forzar error de integridad y comprobar auditoría ERROR | Pendiente |
| Revisar `/home/dasc/backups/.dasc/audit.log` | Pendiente |
| Validación completa en VM Ubuntu | Pendiente |

## Estado de cierre

R-022 queda implementado a nivel de scripts y pendiente de validación en VM Ubuntu.
