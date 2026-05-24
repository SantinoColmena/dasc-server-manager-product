# F6-GATE-03G - Cierre restauración controlada de backups

## Objetivo

Validar que DASC Server Manager dispone de una herramienta de producto para restaurar backups completos de forma controlada, segura y verificable.

## Estado

Cerrada.

## Entorno usado

| Rol | Máquina | IP privada DASC |
|---|---|---|
| API / Restauración | lab-pruebas | 192.168.60.10 |
| DB / Destino restauración | lab-db-gate02 | 192.168.60.20 |

## Contexto

En F6-GATE-03D se validó la generación automatizada de backups completos.

En F6-GATE-03E se integró el estado del último backup en el informe operativo.

En F6-GATE-03F se validó retención y limpieza de backups.

En F6-GATE-03G se valida la restauración controlada de un backup completo sobre una base separada.

## Herramientas añadidas

~~~text
/opt/dasc/api/tools/restore_db_backup.py
/opt/dasc/api/tools/restore_db_backup.sh
~~~

En el repositorio:

~~~text
deploy/api/package/tools/restore_db_backup.py
deploy/api/package/tools/restore_db_backup.sh
~~~

## Variables de restauración

Se añadieron al ejemplo de configuración:

~~~text
RESTORE_DB_HOST
RESTORE_DB_USER
RESTORE_DB_PASS
RESTORE_TARGET_DB
~~~

En la validación real se usó:

~~~text
RESTORE_DB_HOST=192.168.60.20
RESTORE_DB_USER=dasc_restore
RESTORE_DB_PASS=***
RESTORE_TARGET_DB=dasc_logs_restore_test
~~~

## Base destino

La restauración se realizó sobre una base separada:

~~~text
dasc_logs_restore_test
~~~

Esto evita tocar la base original:

~~~text
dasc_logs
~~~

## Preparación en servidor DB

En `lab-db-gate02` se recreó la base de restauración:

~~~sql
DROP DATABASE IF EXISTS dasc_logs_restore_test;
CREATE DATABASE dasc_logs_restore_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
~~~

También se preparó el usuario:

~~~text
dasc_restore@192.168.60.10
~~~

Con permisos sobre:

~~~text
dasc_logs_restore_test.*
~~~

## Backup restaurado

La herramienta usó el último backup válido conservado tras la retención:

~~~text
/var/backups/dasc/mysql/full/dasc_logs_full_20260524-082800_F6-GATE-03F-D.sql
~~~

Hash SHA256 verificado:

~~~text
a5e6c4c0cf86094b2e1b75c384ca80c8794210f6d94251df63f8b8619747b537
~~~

## Dry-run

Se ejecutó:

~~~bash
cd /opt/dasc/api
./tools/restore_db_backup.sh
~~~

Resultado:

- Modo: `DRY-RUN`.
- Backup detectado correctamente.
- Base origen esperada: `dasc_logs`.
- Base destino: `dasc_logs_restore_test`.
- SHA256: OK.
- Conexión destino: OK.
- No se restauró nada.
- Evidencia generada.
- Resultado: OK.

Evidencia:

~~~text
/opt/dasc/api/reports/restores/restore_20260524-083431.json
~~~

## Restauración real controlada

Se ejecutó:

~~~bash
cd /opt/dasc/api
./tools/restore_db_backup.sh --apply
~~~

Resultado:

- Modo: `APLICAR`.
- SHA256: OK.
- Conexión destino: OK.
- Restauración aplicada correctamente.
- Tabla restaurada: `eventos`.
- Eventos después: `19`.
- Resultado: OK.

Evidencia:

~~~text
/opt/dasc/api/reports/restores/restore_20260524-083438.json
~~~

## Validación en base de datos

En `lab-db-gate02` se comprobó:

~~~text
Base original dasc_logs: 20 eventos
Base restaurada dasc_logs_restore_test: 19 eventos
~~~

La diferencia es correcta porque el backup restaurado corresponde a un momento anterior al último evento registrado en la base original.

Últimos eventos restaurados detectados:

~~~text
id 19 | dasc-web | acceso | anon  | HEAD /      | ERROR
id 18 | dasc-web | acceso | anon  | HEAD /      | ERROR
id 17 | dasc-web | acceso | anon  | HEAD /      | ERROR
id 16 | dasc-web | login  | sqs   | POST /login | ERROR
id 15 | dasc-web | login  | admin | POST /logout | OK
~~~

## Evidencia JSON

La evidencia final confirmó:

~~~text
mode: apply
source_db: dasc_logs
target_db: dasc_logs_restore_test
host: 192.168.60.20
user: dasc_restore
sha256.ok: true
before.tables: []
after.tables: eventos
after.eventos_count: 19
status: OK
~~~

## Seguridad temporal

Se comprobó que no quedaron temporales de credenciales:

~~~text
OK: no quedan temporales dasc_restore en /tmp
~~~

## Criterio de cierre

F6-GATE-03G se considera cerrada porque:

- Existe herramienta de restauración dentro del paquete API.
- Existe wrapper Bash ejecutable.
- La restauración usa variables configurables.
- La herramienta detecta el último backup válido.
- Verifica SHA256 antes de restaurar.
- Funciona en modo `dry-run`.
- Funciona en modo `--apply`.
- No restaura sobre la base original.
- Restaura en una base separada.
- Valida tablas después de restaurar.
- Valida conteo de eventos.
- Genera evidencia JSON.
- No deja temporales de credenciales.

## Límites

Esta puerta no valida todavía:

- Restauración desde panel web.
- Restauración sobre producción.
- Restauración parcial.
- Restauración desde copia externa cifrada.
- Confirmación humana avanzada.
- Alertas ante fallo de restauración.

## Conclusión

DASC Server Manager supera la validación de restauración controlada de backups.

El ciclo básico de protección de datos queda validado:

~~~text
generar backup
verificar backup
incluir backup en informe
limpiar backups antiguos
restaurar backup de forma controlada
~~~
