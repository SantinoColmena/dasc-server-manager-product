# R-029 - Validación de copia externa cifrada con GPG

## Objetivo

Validar que el script `sync_external_backup.sh` puede cifrar una copia de seguridad con GPG antes de sincronizarla hacia un destino externo.

Esta prueba valida la primera versión funcional de R-029.

## Servidor usado

| Rol | Servidor |
|---|---|
| Backups / Servicios | 192.168.60.30 |

La prueba se realizó en el servidor de Backups / Servicios, ya que es la máquina donde se generan y sincronizan las copias de seguridad.

No se realizaron cambios en el servidor API ni en el servidor DB.

## Preparación de la prueba

Se crearon dos directorios temporales:

~~~bash
/tmp/dasc-backups-test-gpg
/tmp/dasc-external-test-gpg
~~~

El primero actúa como origen de backups.

El segundo actúa como destino externo local simulado.

## Comando ejecutado

~~~bash
cd ~/dasc-server-manager-product

git pull

chmod +x deploy/backup-services/package/sync_external_backup.sh

rm -rf /tmp/dasc-backups-test-gpg /tmp/dasc-external-test-gpg
mkdir -p /tmp/dasc-backups-test-gpg
mkdir -p /tmp/dasc-external-test-gpg

echo "backup cifrado de prueba R-029" > /tmp/dasc-backups-test-gpg/backup-cifrado-demo.sql

EXTERNAL_BACKUP_ENABLED=yes \
EXTERNAL_BACKUP_TYPE=local \
EXTERNAL_BACKUP_PATH=/tmp/dasc-external-test-gpg \
EXTERNAL_BACKUP_ENCRYPTION=gpg \
EXTERNAL_GPG_PASSPHRASE="dasc-test-2026" \
bash deploy/backup-services/package/sync_external_backup.sh /tmp/dasc-backups-test-gpg
~~~

## Resultado obtenido

~~~text
[2026-05-23 10:20:47] Cifrado activado. Preparando copias cifradas en /tmp/tmp.NyNsJ1emMe
gpg: creado el directorio '/home/santino/.gnupg'
gpg: caja de claves '/home/santino/.gnupg/pubring.kbx' creada
[2026-05-23 10:20:48] Sincronizando backups hacia destino local: /tmp/dasc-external-test-gpg
sending incremental file list
./
backup-cifrado-demo.sql.gpg

sent 266 bytes  received 38 bytes  608,00 bytes/sec
total size is 115  speedup is 0,38
[2026-05-23 10:20:48] OK: sincronización externa completada correctamente
~~~

## Comprobación del archivo cifrado

Comando ejecutado:

~~~bash
ls -l /tmp/dasc-external-test-gpg
test -f /tmp/dasc-external-test-gpg/backup-cifrado-demo.sql.gpg && echo "OK: archivo cifrado generado"
~~~

Resultado obtenido:

~~~text
-rw-rw-r-- 1 santino santino 115 may 23 10:20 backup-cifrado-demo.sql.gpg
OK: archivo cifrado generado
~~~

## Prueba de descifrado

Comando ejecutado:

~~~bash
gpg --batch --yes --pinentry-mode loopback \
  --passphrase "dasc-test-2026" \
  -o /tmp/dasc-descifrado-r029.sql \
  -d /tmp/dasc-external-test-gpg/backup-cifrado-demo.sql.gpg

cat /tmp/dasc-descifrado-r029.sql
~~~

Resultado obtenido:

~~~text
gpg: datos cifrados AES256.CFB
gpg: cifrado con 1 frase contraseña
backup cifrado de prueba R-029
~~~

## Interpretación

El script ha generado correctamente una versión cifrada del backup original.

El archivo sincronizado al destino externo no es el `.sql` original, sino una copia cifrada con extensión `.gpg`.

La prueba de descifrado confirma que el contenido original se puede recuperar correctamente usando la contraseña definida en `EXTERNAL_GPG_PASSPHRASE`.

## Conclusión

R-029 queda validada en modo local con cifrado GPG.

Estado:

- Cifrado GPG: validado.
- Sincronización externa cifrada: validada.
- Descifrado de prueba: validado.
- Uso con NAS/SFTP real: pendiente de una validación futura si se dispone de destino real.
