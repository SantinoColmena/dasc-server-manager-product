# R-051F - Adaptar instalador backup-services a perfiles reales

## Objetivo

Adaptar el instalador de backup-services para perfiles reales y evitar contraseñas débiles por defecto.

## Estado

En curso.

## Archivo modificado

- deploy/backup-services/install_backup_services.sh

## Problema detectado

El instalador de backup-services tenía valores por defecto útiles en laboratorio, pero no adecuados para producto:

- DB_BACKUP_PASS=dasc_backup_2026
- DB_RESTORE_PASS=dasc_restore_2026

Estos valores deben dejar de ser defaults activos.

## Decisión aplicada

A diferencia del instalador DB, backup-services no debe generar contraseñas aleatorias por defecto.

Motivo:

- Las contraseñas usadas por backup-services deben coincidir con las creadas en el servidor DB.
- Si backup-services generase contraseñas nuevas, la conexión a la DB fallaría.

Por tanto, el instalador usa este orden:

1. Cargar DB_SECRETS_FILE si existe.
2. Usar variables de entorno si se proporcionan.
3. Pedir passwords por teclado sin mostrarlos.

## Fichero de secretos compatible

Por defecto intenta cargar:

- /root/dasc-db-install-secrets.env

Este fichero puede ser generado por:

- deploy/db/install_db.sh

y copiado de forma segura al servidor de backups si aplica.

## Variables soportadas

- DASC_PROFILE
- DB_SECRETS_FILE
- DB_HOST
- DB_NAME
- DB_BACKUP_USER
- DB_BACKUP_PASS
- DB_RESTORE_USER
- DB_RESTORE_PASS
- BACKUP_USER
- BACKUP_PASS
- RESTORE_USER
- RESTORE_PASS
- BACKUP_DIR

## Perfiles soportados

Se añade soporte para:

- DASC_PROFILE=lite
- DASC_PROFILE=standard
- DASC_PROFILE=pro
- DASC_PROFILE=custom

## Comportamiento por perfil

### Lite

Si DB_HOST está vacío, usa:

- DB_HOST=127.0.0.1

### Standard, Pro y Custom

DB_HOST se valida o se pide como ya hacía el instalador.

## Seguridad

Las contraseñas no se muestran por pantalla.

Los ficheros locales usados por el usuario `dasc` siguen siendo:

- /home/dasc/.my.cnf
- /home/dasc/.my_restore.cnf

con permisos esperados:

- 600
- propietario dasc:dasc

## Criterio de validación

R-051F se considera preparada cuando:

- install_backup_services.sh conserva sintaxis Bash válida.
- Ya no hay defaults activos dasc_backup_2026 ni dasc_restore_2026.
- Existe bloque R-051F en el instalador.
- El instalador puede cargar DB_SECRETS_FILE.
- El instalador puede pedir secretos manualmente.
- No se reinstala ni rompe el entorno actual.
- El repo queda limpio y subido.
