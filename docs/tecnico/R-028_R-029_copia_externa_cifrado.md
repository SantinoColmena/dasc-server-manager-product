# R-028 / R-029 - Copia externa NAS/SFTP y cifrado opcional

## Objetivo

Preparar Vigex para poder enviar copias de seguridad a un destino externo.

Esta mejora forma parte de la Fase 3 porque permite que los perfiles de despliegue sean adaptables:

- En modo single / Lite, la copia externa es obligatoria.
- En modo dual / PyME, la copia externa es recomendable.
- En modo distributed / Pro, la copia externa puede usarse como protección adicional.

## Servidor donde se ejecuta

El script se ejecuta en el servidor de Backups / Servicios.

En el laboratorio real:

| Rol | Servidor |
|---|---|
| Backups / Servicios | 192.168.60.30 |

No se ejecuta en el servidor API ni en el servidor DB.

## Archivo implementado

~~~text
deploy/backup-services/package/sync_external_backup.sh
~~~

Cuando se instale el servidor de Backups / Servicios, el instalador lo copiará a:

~~~text
/usr/local/bin/sync_external_backup.sh
~~~

## Tipos de destino soportados

| Tipo | Uso |
|---|---|
| local | Directorio local o disco externo montado |
| nas | Carpeta NAS montada en el sistema |
| sftp | Servidor externo accesible por SSH/SFTP |

## Cifrado opcional

El script permite cifrado opcional con GPG simétrico.

Variables relacionadas:

~~~text
EXTERNAL_BACKUP_ENCRYPTION=none
EXTERNAL_GPG_PASSPHRASE=
~~~

Valores soportados:

| Valor | Resultado |
|---|---|
| none | Sin cifrado |
| gpg | Cifra los ficheros antes de sincronizar |
| gpg-symmetric | Alias de gpg |

## Variables principales

~~~text
EXTERNAL_BACKUP_ENABLED=no
EXTERNAL_BACKUP_TYPE=none
EXTERNAL_BACKUP_PATH=/mnt/vigex-external
EXTERNAL_SYNC_DELETE=no
EXTERNAL_BACKUP_ENCRYPTION=none
EXTERNAL_GPG_PASSPHRASE=
EXTERNAL_SFTP_HOST=
EXTERNAL_SFTP_PORT=22
EXTERNAL_SFTP_USER=
EXTERNAL_SFTP_REMOTE_PATH=
~~~

## Prueba segura recomendada

Antes de usar NAS o SFTP real, se debe probar con un destino local temporal:

~~~bash
mkdir -p /tmp/vigex-backups-test
mkdir -p /tmp/vigex-external-test

echo "backup de prueba" > /tmp/vigex-backups-test/backup-demo.sql

EXTERNAL_BACKUP_ENABLED=yes \
EXTERNAL_BACKUP_TYPE=local \
EXTERNAL_BACKUP_PATH=/tmp/vigex-external-test \
EXTERNAL_BACKUP_ENCRYPTION=none \
bash /usr/local/bin/sync_external_backup.sh /tmp/vigex-backups-test
~~~

## Resultado esperado

~~~text
OK: sincronización externa completada correctamente
~~~

Y debe existir el archivo:

~~~text
/tmp/vigex-external-test/backup-demo.sql
~~~

## Decisión de seguridad

En esta primera versión no se fuerza el cifrado por defecto.

Motivo:

- Permite validar primero la sincronización.
- Evita introducir secretos reales en el repositorio.
- Deja el cifrado preparado para entornos reales mediante variables de entorno.

## Estado

- R-028: implementada primera versión para destino local/NAS/SFTP.
- R-029: implementada primera versión de cifrado opcional con GPG.
- Pendiente: validación real en servidor Backups / Servicios.
