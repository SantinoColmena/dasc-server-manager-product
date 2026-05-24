# F6-GATE-03D - Validación de backup completo automatizado como herramienta de producto

## Objetivo

Convertir el backup completo validado manualmente en una herramienta incluida dentro del paquete API de DASC Server Manager.

## Estado

En curso.

## Contexto

En F6-GATE-03A/B/C ya se validó manualmente:

- Conexión desde API a DB remota.
- Usuario de backup.
- Backup completo con `mysqldump`.
- Hash SHA256 del backup.
- Restauración en base separada.
- Eliminación de archivos temporales con credenciales.

F6-GATE-03D busca pasar de operación manual a herramienta de producto.

## Archivos añadidos

~~~text
deploy/api/package/tools/run_full_db_backup.py
deploy/api/package/tools/run_full_db_backup.sh
~~~

## Variables añadidas al ejemplo de configuración

~~~text
BACKUP_DB_HOST
BACKUP_DB_NAME
BACKUP_DB_USER
BACKUP_DB_PASS
BACKUP_OUTPUT_DIR
~~~

## Funcionamiento esperado

La herramienta debe:

- Leer configuración desde `/opt/dasc/api/config.env`.
- Usar preferentemente variables `BACKUP_DB_*`.
- Usar como fallback variables `LOGS_DB_*`.
- Generar backup completo con `mariadb-dump` o `mysqldump`.
- Guardar el backup en `/var/backups/dasc/mysql/full`.
- Crear archivo `.sha256`.
- Crear archivo `.meta.json`.
- Validar que el backup no está vacío.
- Validar que contiene `CREATE TABLE`.
- Registrar si contiene `INSERT INTO`.
- No dejar archivos temporales con credenciales.

## Ejecución esperada en servidor API

~~~bash
cd /opt/dasc/api
./tools/run_full_db_backup.sh --label F6-GATE-03D
~~~

## Resultado esperado

Debe generarse un backup en:

~~~text
/var/backups/dasc/mysql/full
~~~

Con archivos asociados:

~~~text
.sql
.sql.sha256
.sql.meta.json
~~~

## Ajuste en instalador

El instalador API debe:

- Verificar que existe `mysqldump` o `mariadb-dump`.
- Instalar `mariadb-client` si falta.
- Dar permisos de ejecución a `run_full_db_backup.sh`.
- Dar permisos de ejecución a `run_full_db_backup.py`.

## Estado de madurez

Esta puerta convierte el backup completo en una herramienta de producto inicial.

Todavía no valida:

- Programación automática.
- Retención.
- Cifrado.
- Copia externa.
- Restauración automática desde panel.
- Integración final en informe mensual de cliente.

## Próximo paso

Validar la herramienta en Ubuntu real usando la arquitectura ya creada:

~~~text
lab-pruebas     192.168.60.10   API / ejecutor backup
lab-db-gate02   192.168.60.20   DB / origen datos
~~~

## Conclusión

F6-GATE-03D queda preparada para validación real en Ubuntu.
