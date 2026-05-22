# Validación R-019 - Restauración controlada de backups

## Objetivo

Implementar la restauración controlada de backups desde el panel DASC Server Manager, usando un script remoto seguro instalado en el servidor de backups/servicios.

## Estado inicial

El backend del panel ya tenía parte de la restauración preparada:

- Variable `SCRIPT_RESTORE`.
- Función `plan_restauracion_backups()`.
- Función `restaurar_backup_remoto()`.
- Ruta `/backups/restore/preview`.
- Ruta `/backups/restore/confirm`.

El instalador de backup-services también esperaba un script:

    restore_api.sh

Pero en el repositorio todavía no existía el paquete `deploy/backup-services/package/` con los scripts administrativos necesarios.

## Cambios realizados

- Se crea `deploy/backup-services/package/`.
- Se añade `servicios_api.sh`.
- Se añade `backups_api.sh`.
- Se añade `restore_api.sh`.
- `restore_api.sh` exige confirmación explícita `SI`.
- `restore_api.sh` solo permite restaurar backups ubicados dentro de `/home/dasc/backups`.
- `restore_api.sh` busca el backup por ID en `history.tsv`.
- `restore_api.sh` valida que el backup tenga estado `OK`.
- `restore_api.sh` usa `/home/dasc/.my_restore.cnf` para credenciales de restauración.
- `restore_api.sh` registra el resultado en `.dasc/restore.log`.

## Archivos añadidos

- `deploy/backup-services/package/backups_api.sh`
- `deploy/backup-services/package/servicios_api.sh`
- `deploy/backup-services/package/restore_api.sh`
- `docs/validaciones/R-019_restauracion_controlada.md`

## Criterio de seguridad

La restauración no debe aceptar rutas arbitrarias desde el panel.

El panel solo envía un ID de backup, el directorio raíz permitido y la confirmación `SI`.

El script remoto se encarga de:

1. Buscar el ID en el historial.
2. Obtener la ruta real del fichero.
3. Validar que la ruta pertenece al directorio permitido.
4. Restaurar usando credenciales específicas de restore.

## Pruebas estáticas realizadas

Pendiente de ejecutar:

    git status

## Pruebas pendientes en VM Ubuntu

| Prueba | Estado |
|---|---|
| Instalar backup-services con paquete completo | Pendiente |
| Verificar instalación de `restore_api.sh` en `/usr/local/bin/restore_api.sh` | Pendiente |
| Crear backup completo de prueba | Pendiente |
| Comprobar registro en `history.tsv` | Pendiente |
| Restaurar backup por ID desde terminal | Pendiente |
| Restaurar backup desde panel | Pendiente |
| Verificar `restore.log` | Pendiente |
| Validación completa en VM Ubuntu | Pendiente |

## Estado de cierre

R-019 queda implementado a nivel de scripts y pendiente de validación en VM Ubuntu.
