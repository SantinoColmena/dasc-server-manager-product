# R-052D - Auditoría SSH, claves y ficheros runtime

## Objetivo

Auditar SSH, claves y ficheros runtime relacionados con el panel local.

## Estado

Cerrada.

## SSH usuario actual

El usuario actual es:

- santino

Tiene:

- /home/santino/.ssh con permisos 700.
- known_hosts con permisos 600.
- known_hosts.old con permisos 644.

## SSH API

El panel local tiene:

- /opt/dasc/api/.ssh

Permisos:

- directorio 700.
- id_rsa_dasc 600.
- id_rsa_dasc.pub 644.
- known_hosts_dasc 644.

## Resultado

La clave privada del API está correctamente protegida.

## Observación

La carpeta SSH pertenece a `santino:santino` porque el servicio dasc-api corre como `santino`.

Si se migra dasc-api a usuario dedicado, esta carpeta deberá pasar al nuevo usuario técnico.

## Ficheros runtime detectados

En `/opt/dasc/api/data` existen:

- users.json
- alerts.db
- auth_logs.json
- support_tickets.db
- support_tickets.json

Actualmente están en permisos 644.

## Riesgo

Los ficheros de datos runtime deberían ser privados para el usuario del servicio.

## Conclusión

R-052D queda validada.

La clave privada está bien protegida, pero los ficheros runtime deben endurecerse junto con la migración del servicio a usuario dedicado.
