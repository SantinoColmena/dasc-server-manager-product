# F6-GATE-03D - Cierre backup completo automatizado como herramienta de producto

## Objetivo

Validar que el backup completo de base de datos remota ya no depende de comandos manuales, sino de una herramienta incluida dentro del paquete API de DASC Server Manager.

## Estado

Cerrada.

## Entorno usado

| Rol | Máquina | IP privada DASC |
|---|---|---|
| API / Ejecutor backup | lab-pruebas | 192.168.60.10 |
| DB / Origen datos | lab-db-gate02 | 192.168.60.20 |

## Contexto

En F6-GATE-03A/B/C se validó manualmente:

- Usuario remoto de backup.
- Backup completo con `mysqldump`.
- Hash SHA256.
- Restauración en base separada.
- Eliminación de archivos temporales con credenciales.

En F6-GATE-03D se convierte esa operación manual en una herramienta de producto.

## Archivos añadidos al paquete API

~~~text
deploy/api/package/tools/run_full_db_backup.py
deploy/api/package/tools/run_full_db_backup.sh
~~~

En instalación real quedan en:

~~~text
/opt/dasc/api/tools/run_full_db_backup.py
/opt/dasc/api/tools/run_full_db_backup.sh
~~~

## Variables añadidas

Se añadieron variables de backup al ejemplo de configuración:

~~~text
BACKUP_DB_HOST
BACKUP_DB_NAME
BACKUP_DB_USER
BACKUP_DB_PASS
BACKUP_OUTPUT_DIR
~~~

En la validación real se configuró:

~~~text
BACKUP_DB_HOST=192.168.60.20
BACKUP_DB_NAME=dasc_logs
BACKUP_DB_USER=dasc_backup
BACKUP_DB_PASS=***
BACKUP_OUTPUT_DIR=/var/backups/dasc/mysql/full
~~~

## Instalador

El instalador API fue actualizado para:

- Verificar la existencia de `mysqldump` o `mariadb-dump`.
- Instalar `mariadb-client` si falta.
- Copiar la herramienta de backup dentro de `/opt/dasc/api/tools`.
- Dar permisos de ejecución a `run_full_db_backup.sh`.
- Dar permisos de ejecución a `run_full_db_backup.py`.

## Validación estructural del paquete

Se ejecutó la validación automática del paquete API.

Resultado:

~~~text
Total comprobaciones: 32
Correctas: 32
Fallidas: 0
Resultado: OK
~~~

## Ejecución real en Ubuntu

En `lab-pruebas` se ejecutó:

~~~bash
cd /opt/dasc/api
./tools/run_full_db_backup.sh --label F6-GATE-03D
~~~

Resultado:

~~~text
Backup completo generado correctamente.
Base de datos: dasc_logs
Host: 192.168.60.20
CREATE TABLE: True
INSERT INTO: True
~~~

## Backup generado

Archivo generado:

~~~text
/var/backups/dasc/mysql/full/dasc_logs_full_20260524-080415_F6-GATE-03D.sql
~~~

Archivos asociados:

~~~text
/var/backups/dasc/mysql/full/dasc_logs_full_20260524-080415_F6-GATE-03D.sql.sha256
/var/backups/dasc/mysql/full/dasc_logs_full_20260524-080415_F6-GATE-03D.sql.meta.json
~~~

## Hash SHA256

~~~text
64b0a829de533a13ec870104e1cb55cccdcbe8c1b76687f406d0a829008e2b15
~~~

## Metadata generada

La metadata confirmó:

~~~text
database: dasc_logs
host: 192.168.60.20
user: dasc_backup
size_bytes: 4386
has_create_table: true
has_insert_into: true
dump_binary: /usr/bin/mariadb-dump
label: F6-GATE-03D
~~~

## Permisos

El backup y sus archivos asociados quedaron con permisos controlados:

~~~text
-rw-r-----
0640
usuario: santino
grupo: santino
~~~

## Seguridad temporal

Se comprobó que no quedaron temporales de credenciales en `/tmp`:

~~~text
OK: no quedan temporales dasc_backup en /tmp
~~~

## Corrección adicional de calidad

Durante la validación se detectó que el instalador seguía mostrando un mensaje final confuso indicando que el SSH automático estaba configurado contra `192.168.60.30`.

Ese mensaje se corrige para indicar que el SSH remoto queda en modo no bloqueante y que la validación completa se hará en una puerta posterior.

## Criterio de cierre

F6-GATE-03D se considera cerrada porque:

- El backup completo ya existe como herramienta de producto.
- La herramienta está incluida en el paquete API.
- El instalador copia y da permisos a la herramienta.
- La validación estructural del paquete da 32/32 OK.
- La herramienta se ejecuta en Ubuntu real.
- Genera backup `.sql`.
- Genera hash `.sha256`.
- Genera metadata `.meta.json`.
- Valida estructura del backup.
- No deja temporales de credenciales.
- Usa MariaDB remoto real.

## Límites

Esta puerta no valida todavía:

- Programación automática.
- Retención.
- Cifrado.
- Copia externa.
- Restauración automática desde panel.
- Integración completa en informe operativo.
- Envío de alertas ante fallo de backup.

## Próxima puerta recomendada

La siguiente puerta lógica es:

~~~text
F6-GATE-03E - Integrar estado de backup/restauración en informe operativo
~~~

Después:

~~~text
F6-GATE-03F - Automatización, retención y limpieza de backups
~~~

## Conclusión

DASC Server Manager supera la validación de backup completo automatizado como herramienta de producto.

El proyecto pasa de backup manual validado a backup ejecutable desde el paquete API instalado en Ubuntu.
