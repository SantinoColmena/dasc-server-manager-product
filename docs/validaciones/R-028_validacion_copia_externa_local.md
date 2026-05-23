# R-028 - Validación de copia externa local

## Objetivo

Validar que el script `sync_external_backup.sh` puede sincronizar copias de seguridad hacia un destino externo local.

Esta prueba representa el primer paso de R-028 antes de usar un NAS real o un servidor SFTP.

## Servidor usado

| Rol | Servidor |
|---|---|
| Backups / Servicios | 192.168.60.30 |

La prueba se realizó en el servidor de Backups / Servicios, porque es la máquina donde se generan y almacenan las copias de seguridad.

No se realizaron cambios en el servidor API ni en el servidor DB.

## Comando ejecutado

~~~bash
cd ~

if [ ! -d "dasc-server-manager-product" ]; then
  git clone https://github.com/SantinoColmena/dasc-server-manager-product.git
fi

cd ~/dasc-server-manager-product

git pull

chmod +x deploy/backup-services/package/sync_external_backup.sh

mkdir -p /tmp/dasc-backups-test
mkdir -p /tmp/dasc-external-test

echo "backup de prueba R-028" > /tmp/dasc-backups-test/backup-demo.sql

EXTERNAL_BACKUP_ENABLED=yes \
EXTERNAL_BACKUP_TYPE=local \
EXTERNAL_BACKUP_PATH=/tmp/dasc-external-test \
EXTERNAL_BACKUP_ENCRYPTION=none \
bash deploy/backup-services/package/sync_external_backup.sh /tmp/dasc-backups-test
~~~

## Resultado obtenido

~~~text
[2026-05-23 10:17:59] Sincronizando backups hacia destino local: /tmp/dasc-external-test
sending incremental file list
backup-demo.sql

sent 159 bytes  received 35 bytes  388,00 bytes/sec
total size is 23  speedup is 0,12
[2026-05-23 10:17:59] OK: sincronización externa completada correctamente
~~~

## Comprobación del destino externo

Comando ejecutado:

~~~bash
ls -l /tmp/dasc-external-test
cat /tmp/dasc-external-test/backup-demo.sql
~~~

Resultado obtenido:

~~~text
-rw-rw-r-- 1 santino santino 23 may 23 10:17 backup-demo.sql
backup de prueba R-028
~~~

## Interpretación

El script ha sincronizado correctamente el archivo de backup desde el directorio origen hacia el destino externo local.

Esto valida que la lógica base de copia externa funciona correctamente antes de probar destinos más avanzados como NAS o SFTP.

## Conclusión

R-028 queda validada en modo local.

Estado:

- Copia externa local: validada.
- NAS: preparado a nivel de script, pendiente de prueba con carpeta montada.
- SFTP: preparado a nivel de script, pendiente de prueba con servidor remoto.
