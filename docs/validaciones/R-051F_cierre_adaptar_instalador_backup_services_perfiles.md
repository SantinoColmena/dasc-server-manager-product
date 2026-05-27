# R-051F - Cierre adaptación instalador backup-services a perfiles reales

## Objetivo

Cerrar la adaptación del instalador de backup-services para perfiles reales de despliegue.

## Estado

Cerrada.

## Contexto

R-051F forma parte de la tarea R-051, orientada a preparar los instaladores de DASC Server Manager para trabajar con IPs, hosts, perfiles y secretos reales.

Esta subtarea se centra en:

- deploy/backup-services/install_backup_services.sh

## Problema corregido

El instalador de backup-services tenía valores por defecto útiles en laboratorio, pero no adecuados para producto:

- DB_BACKUP_PASS=dasc_backup_2026
- DB_RESTORE_PASS=dasc_restore_2026

## Cambio aplicado

Se eliminaron los passwords débiles como defaults activos.

Ahora las asignaciones quedan sin valor débil por defecto:

- DB_BACKUP_PASS="${DB_BACKUP_PASS:-}"
- DB_RESTORE_PASS="${DB_RESTORE_PASS:-}"

## Decisión técnica

A diferencia del instalador DB, backup-services no genera contraseñas aleatorias automáticamente.

Motivo:

- Las contraseñas de backup-services deben coincidir con las credenciales creadas previamente en el servidor DB.
- Si backup-services generase secretos distintos, fallaría la conexión a la base de datos.

## Orden de resolución de secretos

El instalador usa este orden:

1. Cargar DB_SECRETS_FILE si existe.
2. Usar variables de entorno si se proporcionan.
3. Pedir passwords por teclado sin mostrarlos.

## Fichero de secretos compatible

Por defecto intenta cargar:

- /root/dasc-db-install-secrets.env

Este fichero puede ser generado por:

- deploy/db/install_db.sh

y sirve para trasladar de forma controlada las credenciales necesarias hacia backup-services.

## Perfiles soportados

Se añadió soporte para:

- DASC_PROFILE=lite
- DASC_PROFILE=standard
- DASC_PROFILE=pro
- DASC_PROFILE=custom

## Comportamiento por perfil

### Lite

Si DB_HOST está vacío, usa:

- DB_HOST=127.0.0.1

### Standard, Pro y Custom

DB_HOST se valida o se solicita como ya hacía el instalador.

## Seguridad

Las contraseñas no se muestran por pantalla.

Los ficheros locales usados por el usuario `dasc` siguen siendo:

- /home/dasc/.my.cnf
- /home/dasc/.my_restore.cnf

con permisos esperados:

- 600
- propietario dasc:dasc

## Commit funcional

- 39fcd62 feat: adaptar instalador backups a perfiles

## Validación en lab-pruebas

Se validó:

- Repo actualizado.
- install_backup_services.sh mantiene sintaxis Bash válida.
- Bloque R-051F presente.
- DB_SECRETS_FILE presente.
- prompt_secret_var presente.
- DB_BACKUP_PASS ya no tiene default débil activo.
- DB_RESTORE_PASS ya no tiene default débil activo.
- Los valores antiguos solo aparecen como placeholders rechazados.
- No se reinstaló backup-services.
- dasc-api sigue activo.
- nginx sigue activo.
- Panel local directo 8000 sigue respondiendo.
- Panel local por Nginx 8080 sigue respondiendo.

## Resultado

R-051F queda validada.

El instalador de backup-services queda preparado para perfiles reales y deja de usar contraseñas débiles como defaults activos.

## Próximo paso

Continuar con:

- R-051G - Validación global de instaladores adaptables
