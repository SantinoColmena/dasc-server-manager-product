# F6-GATE-03G - Validación de restauración controlada de backups

## Objetivo

Añadir una herramienta de producto para restaurar backups completos de forma controlada y segura.

## Estado

En curso.

## Contexto

En F6-GATE-03D se automatizó la generación de backups completos.

En F6-GATE-03E se integró el estado del backup en el informe operativo.

En F6-GATE-03F se añadió retención y limpieza de backups.

F6-GATE-03G busca cerrar el ciclo de recuperación.

## Archivos añadidos

~~~text
deploy/api/package/tools/restore_db_backup.py
deploy/api/package/tools/restore_db_backup.sh
~~~

## Variables añadidas

~~~text
RESTORE_DB_HOST
RESTORE_DB_USER
RESTORE_DB_PASS
RESTORE_TARGET_DB
~~~

## Principios de seguridad

La herramienta debe:

- No restaurar sobre la base original.
- Usar una base destino separada.
- Verificar SHA256 antes de restaurar.
- Ejecutar en modo `dry-run` por defecto.
- Requerir `--apply` para restaurar realmente.
- Generar evidencia JSON de la restauración.
- No dejar temporales de credenciales.

## Ejecución esperada

Modo seguro:

~~~bash
cd /opt/dasc/api
./tools/restore_db_backup.sh
~~~

Modo real:

~~~bash
cd /opt/dasc/api
./tools/restore_db_backup.sh --apply
~~~

## Base destino prevista

~~~text
dasc_logs_restore_test
~~~

## Límites

Esta puerta todavía no valida:

- Restauración desde panel.
- Restauración sobre producción.
- Restauración parcial.
- Restauración con confirmación humana avanzada.
- Copia externa cifrada.

## Conclusión

F6-GATE-03G prepara la restauración controlada de backups como herramienta de producto.
