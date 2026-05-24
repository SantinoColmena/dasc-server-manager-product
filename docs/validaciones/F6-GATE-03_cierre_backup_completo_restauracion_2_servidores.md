# F6-GATE-03 - Cierre backup completo y restauración en arquitectura de 2 servidores

## Objetivo

Validar que DASC Server Manager puede realizar un backup completo real de una base de datos remota y restaurarlo en una base de prueba sin afectar a la base original.

## Estado

Cerrada parcialmente.

Se cierran:

- F6-GATE-03A - Preparación de backup en 2 servidores.
- F6-GATE-03B - Backup completo real contra DB remota.
- F6-GATE-03C - Restauración de prueba en base separada.

Quedan pendientes para fases posteriores:

- Backups incrementales/diferenciales.
- Automatización desde scripts de producto.
- Integración completa con informe operativo.
- Validación de backups desde panel.

## Entorno usado

| Rol | Máquina | IP privada DASC |
|---|---|---|
| API / Ejecutor backup | lab-pruebas | 192.168.60.10 |
| DB / Logs / Origen datos | lab-db-gate02 | 192.168.60.20 |

## Base de datos validada

Base original:

~~~text
dasc_logs
~~~

Tabla principal:

~~~text
eventos
~~~

Base de restauración de prueba:

~~~text
dasc_logs_restore_test
~~~

## Preparación en servidor DB

En `lab-db-gate02` se comprobó que:

- MariaDB estaba activo.
- MariaDB escuchaba en `0.0.0.0:3306`.
- Existía la base `dasc_logs`.
- Existía la tabla `eventos`.
- La base original contenía eventos reales del panel.

Se creó el usuario de backup:

~~~text
dasc_backup@192.168.60.10
~~~

Con permisos suficientes para backup mediante `mysqldump`.

## Preparación en servidor API

En `lab-pruebas` se instalaron herramientas cliente MariaDB:

~~~text
mariadb-client
mysqldump
mariadb-dump
~~~

Se comprobó:

- Puerto 3306 accesible hacia `192.168.60.20`.
- Login remoto correcto con `dasc_backup`.
- Acceso a la base `dasc_logs`.

## Carpeta de backups

Se creó la estructura:

~~~text
/var/backups/dasc/mysql/full
~~~

Con permisos controlados.

## Backup completo generado

Se generó un backup completo real de `dasc_logs` usando `mysqldump`.

Archivo generado:

~~~text
/var/backups/dasc/mysql/full/dasc_logs_full_20260524-074603.sql
~~~

Comprobaciones realizadas:

| Comprobación | Resultado |
|---|---|
| Archivo no vacío | OK |
| Contiene `CREATE TABLE` | OK |
| Contiene `INSERT INTO` | OK |
| Líneas del archivo | 67 |
| Tamaño aproximado | 8 KB |

Hash SHA256:

~~~text
bf0a585661ac14bff20faccebd114ae9e9e98f781f59d3b8d699acaf660d5050
~~~

## Seguridad temporal

Para el backup se usó un archivo temporal de conexión:

~~~text
/tmp/dasc_backup_gate03.cnf
~~~

Después del backup, el archivo temporal fue eliminado correctamente.

Para la restauración se usó otro archivo temporal:

~~~text
/tmp/dasc_restore_gate03.cnf
~~~

Después de la restauración, el archivo temporal fue eliminado correctamente.

## Restauración de prueba

Primero se intentó copiar el backup por `scp`, pero el servidor DB no tenía SSH activo:

~~~text
ssh: connect to host 192.168.60.20 port 22: Connection refused
~~~

Esto no se considera fallo de backup/restauración, porque para esta prueba se validó una restauración directa por conexión MariaDB remota.

Se creó la base:

~~~text
dasc_logs_restore_test
~~~

Se creó el usuario de restauración:

~~~text
dasc_restore@192.168.60.10
~~~

Con permisos sobre la base de restauración.

La restauración se ejecutó desde `lab-pruebas` hacia MariaDB remoto usando:

~~~bash
mysql --defaults-extra-file=/tmp/dasc_restore_gate03.cnf dasc_logs_restore_test < "$LATEST_BACKUP"
~~~

## Validación de restauración

En `lab-db-gate02` se comprobó:

~~~sql
USE dasc_logs_restore_test;
SHOW TABLES;
~~~

Resultado:

~~~text
eventos
~~~

Conteo original:

~~~text
total_original_actual = 16
~~~

Conteo restaurado:

~~~text
total_restaurado = 16
~~~

También se verificaron los últimos eventos restaurados, incluyendo:

- Login fallido.
- Logout correcto.
- Acceso a `/logs`.
- Acceso a `/servicios`.
- Evento real del panel `dasc-web`.

## Criterio de cierre

F6-GATE-03A/B/C se considera cerrada porque:

- Existe usuario remoto de backup.
- El servidor API puede acceder a MariaDB remoto.
- Se generó un backup completo real con `mysqldump`.
- El backup contiene estructura y datos.
- El backup tiene hash SHA256 registrado.
- El backup se restauró en una base separada.
- La restauración no tocó la base original.
- El conteo restaurado coincide con el esperado.
- Se eliminaron archivos temporales con credenciales.

## Límites

Esta puerta no valida todavía:

- Backups incrementales.
- Backups diferenciales.
- Restauración automática desde panel.
- Programación automática.
- Retención de backups.
- Cifrado de backups.
- Copia externa.
- Integración completa del resultado en el informe operativo.

## Próxima puerta recomendada

La siguiente puerta lógica es:

~~~text
F6-GATE-03D - Automatizar backup completo como herramienta de producto
~~~

Después:

~~~text
F6-GATE-03E - Integrar estado de backup/restauración en informe operativo
~~~

## Conclusión

DASC Server Manager supera la validación manual de backup completo y restauración en arquitectura de 2 servidores.

Esto demuestra que la base de datos remota puede protegerse mediante backup completo y que el backup generado es recuperable en una base de prueba.
