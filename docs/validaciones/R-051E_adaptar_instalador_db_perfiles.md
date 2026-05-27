# R-051E - Adaptar instalador DB a perfiles reales

## Objetivo

Adaptar el instalador de base de datos para evitar valores débiles por defecto y prepararlo para perfiles reales.

## Estado

En curso.

## Archivo modificado

- deploy/db/install_db.sh

## Problema detectado

El instalador DB tenía valores por defecto útiles en laboratorio, pero no adecuados para producto:

- BACKUP_PASS=dasc_backup_2026
- RESTORE_PASS=dasc_restore_2026
- LOGS_DB_PASS=dasc_logs_2026
- DB_SERVER_ID=20

Estos valores deben evitarse en instalaciones reales.

## Cambio aplicado

Se eliminan los passwords débiles por defecto.

Ahora, si no se pasan desde entorno, el instalador genera automáticamente:

- BACKUP_PASS
- RESTORE_PASS
- LOGS_DB_PASS

con `secrets.token_urlsafe(32)`.

## Perfiles soportados

Se añade soporte para:

- DASC_PROFILE=lite
- DASC_PROFILE=standard
- DASC_PROFILE=pro
- DASC_PROFILE=custom

## DB_SERVER_ID por perfil

Si DB_SERVER_ID no viene definido:

- lite usa 10
- standard usa 20
- pro usa 30
- custom usa 20

El valor puede sobreescribirse pasando DB_SERVER_ID desde el entorno.

## Fichero de secretos local

El instalador guarda los secretos generados o proporcionados en:

- /root/dasc-db-install-secrets.env

con permisos:

- root:root
- 600

Este fichero sirve para preparar la instalación de backup-services, pero no debe subirse al repositorio.

## Variables afectadas

- DASC_PROFILE
- DB_SERVER_ID
- BACKUP_PASS
- RESTORE_PASS
- LOGS_DB_PASS
- DB_SECRETS_FILE

## Criterio de validación

R-051E se considera preparada cuando:

- install_db.sh conserva sintaxis Bash válida.
- Ya no hay defaults dasc_backup_2026, dasc_restore_2026 ni dasc_logs_2026.
- Existe bloque R-051E en el instalador.
- El instalador documenta fichero de secretos local.
- No se reinstala ni rompe la DB actual en laboratorio.
- El repo queda limpio y subido.
