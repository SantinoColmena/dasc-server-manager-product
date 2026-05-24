# F6-GATE-03F - Validación de retención y limpieza de backups

## Objetivo

Añadir una herramienta de producto para aplicar política de retención sobre backups completos generados por DASC Server Manager.

## Estado

En curso.

## Contexto

En F6-GATE-03D se validó la generación automática de backups completos.

En F6-GATE-03E se integró el estado del último backup en el informe operativo.

F6-GATE-03F busca evitar crecimiento indefinido de la carpeta de backups.

## Archivos añadidos

~~~text
deploy/api/package/tools/cleanup_db_backups.py
deploy/api/package/tools/cleanup_db_backups.sh
~~~

## Variable añadida

~~~text
BACKUP_RETENTION_KEEP=10
~~~

## Funcionamiento esperado

La herramienta debe:

- Leer `BACKUP_OUTPUT_DIR` desde `config.env`.
- Leer `BACKUP_RETENTION_KEEP`.
- Detectar backups `.sql`.
- Asociar cada backup con `.sha256` y `.meta.json`.
- Conservar los últimos N backups.
- Mostrar candidatos a eliminación.
- Ejecutar en modo `dry-run` por defecto.
- Requerir `--apply` para borrar realmente.
- No tocar backups si no hay más de N.

## Ejecución esperada

Modo seguro:

~~~bash
cd /opt/dasc/api
./tools/cleanup_db_backups.sh --keep 3
~~~

Modo real:

~~~bash
cd /opt/dasc/api
./tools/cleanup_db_backups.sh --keep 3 --apply
~~~

## Límites

Esta puerta todavía no valida:

- Cron o systemd timer.
- Cifrado.
- Copia externa.
- Restauración automática.
- Alertas ante fallo.

## Conclusión

F6-GATE-03F prepara la política básica de retención para backups completos.
