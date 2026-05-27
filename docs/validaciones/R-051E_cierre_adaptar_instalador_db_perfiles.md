# R-051E - Cierre adaptación instalador DB a perfiles reales

## Objetivo

Cerrar la adaptación del instalador DB para perfiles reales de despliegue.

## Estado

Cerrada.

## Contexto

R-051E forma parte de la tarea R-051, cuyo objetivo es preparar los instaladores de DASC Server Manager para funcionar con IPs, hosts y perfiles reales.

Esta subtarea se centra en:

- deploy/db/install_db.sh

## Problema corregido

El instalador DB tenía valores por defecto útiles para laboratorio, pero no adecuados para producto:

- BACKUP_PASS=dasc_backup_2026
- RESTORE_PASS=dasc_restore_2026
- LOGS_DB_PASS=dasc_logs_2026
- DB_SERVER_ID=20

## Cambio aplicado

Se eliminaron los passwords débiles como defaults activos.

Ahora las asignaciones quedan sin valor por defecto débil:

- BACKUP_PASS="${BACKUP_PASS:-}"
- RESTORE_PASS="${RESTORE_PASS:-}"
- LOGS_DB_PASS="${LOGS_DB_PASS:-}"

Si no se proporcionan desde entorno, el instalador genera secretos automáticamente mediante:

- secrets.token_urlsafe(32)

## Nota sobre validación

Los textos antiguos:

- dasc_backup_2026
- dasc_restore_2026
- dasc_logs_2026

siguen apareciendo dentro de la función is_empty_or_placeholder().

Esto es correcto.

Ahora se usan como valores rechazados o placeholders antiguos, no como contraseñas por defecto activas.

## Perfiles soportados

Se añadió soporte para:

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

El valor puede sobreescribirse desde entorno.

## Fichero de secretos local

El instalador guarda los secretos generados o proporcionados en:

- /root/dasc-db-install-secrets.env

Permisos esperados:

- root:root
- 600

Este fichero sirve para preparar backup-services y no debe subirse al repositorio.

## Commit funcional

- 27fd367 feat: adaptar instalador db a perfiles

## Validación en lab-pruebas

Se validó:

- Repo actualizado.
- install_db.sh mantiene sintaxis Bash válida.
- Bloque R-051E presente.
- resolve_secret_var presente.
- DB_SECRETS_FILE presente.
- No se reinstaló la DB activa.
- dasc-api sigue activo.
- nginx sigue activo.
- Panel local directo 8000 sigue respondiendo.
- Panel local por Nginx 8080 sigue respondiendo.

## Resultado

R-051E queda validada.

El instalador DB queda mejor preparado para perfiles reales y deja de usar contraseñas débiles como defaults activos.

## Próximo paso

Continuar con:

- R-051F - Adaptar instalador backup-services
