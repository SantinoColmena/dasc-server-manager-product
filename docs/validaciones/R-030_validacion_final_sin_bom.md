# R-030 - Validación final del asistente de perfiles sin BOM

## Objetivo

Confirmar que el script `scripts/generar_config_perfil.sh` funciona correctamente en Ubuntu después de corregir la codificación UTF-8 con BOM.

## Servidor usado

| Rol | Servidor |
|---|---|
| API / Panel | 192.168.60.10 |

No se realizaron cambios en el servidor DB ni en el servidor de Backups.

## Prueba 1 - Ejecución con Bash

Comando ejecutado en el servidor API:

~~~bash
DEST_CONFIG=/tmp/dasc-config-distributed-3.env bash scripts/generar_config_perfil.sh distributed
~~~

Resultado validado:

~~~text
INSTALL_MODE=distributed
DASC_PROFILE_NAME=DASC Pro
SERVICIOS_HOST=192.168.60.30
BACKUPS_HOST=192.168.60.30
LOGS_DB_HOST=192.168.60.20
DB_HOST=192.168.60.20
EXTERNAL_BACKUP_REQUIRED=recommended
~~~

Estado: correcto.

## Prueba 2 - Ejecución directa del script

Comando ejecutado en el servidor API:

~~~bash
DEST_CONFIG=/tmp/dasc-config-distributed-direct.env ./scripts/generar_config_perfil.sh distributed
~~~

Resultado validado:

~~~text
INSTALL_MODE=distributed
DASC_PROFILE_NAME=DASC Pro
SERVICIOS_HOST=192.168.60.30
BACKUPS_HOST=192.168.60.30
LOGS_DB_HOST=192.168.60.20
DB_HOST=192.168.60.20
EXTERNAL_BACKUP_REQUIRED=recommended
~~~

Estado: correcto.

## Prueba 3 - Comprobación de BOM

Comando ejecutado:

~~~bash
xxd -g 1 -l 4 scripts/generar_config_perfil.sh
~~~

Resultado obtenido:

~~~text
00000000: 23 21 2f 75                                      #!/u
~~~

Interpretación:

El archivo empieza directamente por `#!/u`, por lo que ya no contiene BOM al inicio.

## Conclusión

El asistente de perfiles queda validado correctamente en Ubuntu.

Se confirma que:

- El script genera correctamente el perfil `distributed`.
- El perfil generado apunta a la arquitectura real de tres servidores.
- El script funciona tanto con `bash script.sh` como con ejecución directa `./script.sh`.
- El archivo ya no contiene BOM.
- R-030 queda validada y corregida.
