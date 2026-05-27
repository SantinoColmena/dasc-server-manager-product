# R-051D - Adaptar instalador API/panel local a perfiles

## Objetivo

Adaptar el instalador del panel/API local para que pueda trabajar con perfiles reales de despliegue y no dependa únicamente de un config.env ya preparado.

## Estado

Cerrada.

## Archivo modificado

- deploy/api/install_dasc_api.sh

## Cambio aplicado

Se añade un bloque de perfil al instalador API:

- DASC_PROFILE=lite
- DASC_PROFILE=standard
- DASC_PROFILE=pro
- DASC_PROFILE=custom

## Comportamiento por perfil

### Lite

Configura automáticamente como locales:

- BACKUPS_HOST=127.0.0.1
- SERVICIOS_HOST=127.0.0.1
- LOGS_DB_HOST=127.0.0.1
- TERMINAL_DATABASE_HOST=127.0.0.1

### Standard

Pide o usa un servidor común para:

- DB
- Backups
- Servicios
- Logs

Es el perfil recomendado para PyME.

### Pro

Pide o usa servidores separados:

- Backups
- Servicios
- DB/Logs

### Custom

Permite configuración manual flexible.

## Variables soportadas desde entorno

El instalador puede recibir:

- DASC_PROFILE
- BACKUPS_HOST
- SERVICIOS_HOST
- LOGS_DB_HOST
- TERMINAL_DATABASE_HOST
- CENTRAL_SUPPORT_ENABLED
- CENTRAL_SUPPORT_URL
- CENTRAL_SUPPORT_CLIENT_ID
- CENTRAL_SUPPORT_CLIENT_NAME
- CENTRAL_SUPPORT_TOKEN
- DASC_LOCAL_INTERNAL_SUPPORT_ENABLED
- CLIENT_ID
- CLIENT_NAME

## Decisión de seguridad

Si no se define DASC_LOCAL_INTERNAL_SUPPORT_ENABLED, el instalador deja:

- DASC_LOCAL_INTERNAL_SUPPORT_ENABLED=false

como estado limpio para cliente.

## Criterio de validación

R-051D se considera preparada cuando:

- install_dasc_api.sh conserva sintaxis Bash válida.
- El bloque R-051D aparece en el instalador.
- El instalador permite DASC_PROFILE=lite.
- El instalador permite DASC_PROFILE=standard.
- El instalador permite DASC_PROFILE=pro.
- El instalador permite DASC_PROFILE=custom.
- No se rompe el comportamiento actual en lab-pruebas.
- El repo queda limpio y subido.
