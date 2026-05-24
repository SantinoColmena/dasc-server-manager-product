# F6-GATE-03F - Cierre retención y limpieza de backups

## Objetivo

Validar que DASC Server Manager dispone de una herramienta de producto para aplicar una política básica de retención sobre backups completos.

## Estado

Cerrada.

## Entorno usado

| Rol | Máquina | IP privada DASC |
|---|---|---|
| API / Backups / Limpieza | lab-pruebas | 192.168.60.10 |
| DB / Origen datos | lab-db-gate02 | 192.168.60.20 |

## Contexto

En F6-GATE-03D se validó la generación automatizada de backups completos.

En F6-GATE-03E se integró el último backup completo en el informe operativo.

En F6-GATE-03F se valida la retención para evitar crecimiento indefinido de la carpeta de backups.

## Herramientas añadidas

~~~text
/opt/dasc/api/tools/cleanup_db_backups.py
/opt/dasc/api/tools/cleanup_db_backups.sh
~~~

En el repositorio:

~~~text
deploy/api/package/tools/cleanup_db_backups.py
deploy/api/package/tools/cleanup_db_backups.sh
~~~

## Variable de retención

Se añadió:

~~~text
BACKUP_RETENTION_KEEP=10
~~~

En la validación real se usó:

~~~text
BACKUP_RETENTION_KEEP=3
~~~

## Validación estructural

La validación del paquete API detectó:

~~~text
Total comprobaciones: 42
Correctas: 42
Fallidas: 0
Resultado: OK
~~~

La validación incluye:

- Existencia de herramienta Python de limpieza.
- Existencia de wrapper Bash.
- Variable `BACKUP_RETENTION_KEEP`.
- Permisos desde instalador.
- Uso de LF en scripts Linux.

## Backups generados para prueba

Se generaron cuatro backups de prueba:

~~~text
F6-GATE-03F-A
F6-GATE-03F-B
F6-GATE-03F-C
F6-GATE-03F-D
~~~

Cada backup generó:

~~~text
.sql
.sql.sha256
.sql.meta.json
~~~

## Dry-run

Se ejecutó:

~~~bash
./tools/cleanup_db_backups.sh --keep 3 --include-orphans
~~~

Resultado:

- Modo: `DRY-RUN`.
- Backups detectados: 6.
- Backups conservados: 3.
- Backups candidatos a eliminación: 3.
- No se eliminó nada.
- No se detectaron huérfanos.
- Resultado: OK.

## Aplicación real

Se ejecutó:

~~~bash
./tools/cleanup_db_backups.sh --keep 3 --apply --include-orphans
~~~

Resultado:

- Modo: `APLICAR`.
- Backups detectados: 6.
- Backups conservados: 3.
- Backups eliminados: 3.
- Ficheros eliminados en total: 8.
- No se detectaron huérfanos.
- Resultado: OK.

## Backups conservados

Quedaron conservados:

~~~text
dasc_logs_full_20260524-082755_F6-GATE-03F-B.sql
dasc_logs_full_20260524-082758_F6-GATE-03F-C.sql
dasc_logs_full_20260524-082800_F6-GATE-03F-D.sql
~~~

Cada uno conserva sus ficheros asociados:

~~~text
.sql
.sql.sha256
.sql.meta.json
~~~

## Backups eliminados

Se eliminaron backups antiguos y sus asociados cuando existían:

~~~text
F6-GATE-03F-A
F6-GATE-03D
backup manual inicial 20260524-074603
~~~

## Criterio de cierre

F6-GATE-03F se considera cerrada porque:

- Existe herramienta de limpieza dentro del paquete API.
- Existe wrapper Bash ejecutable.
- La política de retención es configurable.
- El modo seguro `dry-run` funciona.
- El modo real `--apply` funciona.
- Se conservan los últimos N backups.
- Se eliminan backups antiguos.
- Se eliminan ficheros asociados `.sha256` y `.meta.json`.
- Se revisan huérfanos.
- El resultado final es OK.

## Límites

Esta puerta no valida todavía:

- Programación automática con cron o systemd timer.
- Cifrado.
- Copia externa.
- Restauración automática.
- Alertas ante fallo.
- Política avanzada por días/semanas/meses.

## Próxima puerta recomendada

La siguiente puerta lógica es:

~~~text
F6-GATE-03G - Restauración automática o semiautomática controlada
~~~

También queda pendiente para más adelante:

~~~text
F6-GATE-04 - Instaladores adaptables por perfil e IPs reales
~~~

## Conclusión

DASC Server Manager supera la validación de retención y limpieza de backups.

El sistema ya no solo genera backups completos, sino que también puede aplicar una política básica para conservar los últimos N y eliminar los antiguos de forma controlada.
