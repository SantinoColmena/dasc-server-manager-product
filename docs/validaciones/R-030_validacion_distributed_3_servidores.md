# R-030 - Validación Ubuntu del asistente de perfiles en arquitectura distribuida

## Objetivo

Validar que el script `scripts/generar_config_perfil.sh` genera correctamente la configuración base para el perfil `distributed`, correspondiente a la arquitectura real de tres servidores del proyecto DASC Server Manager.

## Arquitectura usada

| Rol | Servidor | Uso |
|---|---|---|
| API / Panel | 192.168.60.10 | Servidor donde se ejecuta el panel FastAPI y donde se prueba el asistente |
| DB / Logs | 192.168.60.20 | Servidor de base de datos principal y base de datos de logs |
| Backups / Servicios | 192.168.60.30 | Servidor de backups y gestión de servicios por SSH |

## Servidor donde se realizó la prueba

La prueba se realizó en el servidor API / Panel.

No se ejecutaron cambios en el servidor DB ni en el servidor de Backups, ya que esta validación solo comprueba la generación de configuración.

## Comando ejecutado en el servidor API / Panel

~~~bash
cd ~/dasc-server-manager-product
git pull
chmod +x scripts/generar_config_perfil.sh
DEST_CONFIG=/tmp/dasc-config-distributed.env bash scripts/generar_config_perfil.sh distributed
~~~

## Comprobación ejecutada

~~~bash
grep -E "^(INSTALL_MODE|DASC_PROFILE_NAME|SERVICIOS_HOST|BACKUPS_HOST|LOGS_DB_HOST|DB_HOST|EXTERNAL_BACKUP_REQUIRED)=" /tmp/dasc-config-distributed.env
~~~

## Resultado esperado

~~~text
INSTALL_MODE=distributed
DASC_PROFILE_NAME=DASC Pro
SERVICIOS_HOST=192.168.60.30
BACKUPS_HOST=192.168.60.30
LOGS_DB_HOST=192.168.60.20
DB_HOST=192.168.60.20
EXTERNAL_BACKUP_REQUIRED=recommended
~~~

## Interpretación

El resultado confirma que el perfil `distributed` representa correctamente la arquitectura real de tres servidores:

- El servidor API / Panel ejecuta el panel y lanza acciones.
- El servidor DB / Logs centraliza la base de datos y los eventos.
- El servidor Backups / Servicios ejecuta scripts de backup y gestión de servicios.

## Conclusión

El asistente de perfiles funciona correctamente para el modo distribuido de tres servidores.

R-030 queda validada en arquitectura real distribuida como primera versión funcional.
