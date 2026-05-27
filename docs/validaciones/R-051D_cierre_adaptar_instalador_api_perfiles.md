# R-051D - Cierre adaptación instalador API/panel local a perfiles

## Objetivo

Cerrar la validación de la adaptación del instalador API/panel local a perfiles reales de despliegue.

## Estado

Cerrada.

## Contexto

Dentro de R-051 se está preparando DASC Server Manager para que los instaladores no dependan de IPs fijas o configuraciones manuales de laboratorio.

R-051D se centra en el instalador principal del panel/API local:

- deploy/api/install_dasc_api.sh

## Cambio aplicado

Se añadió un bloque de perfil al instalador API/panel local.

Perfiles soportados:

- lite
- standard
- pro
- custom

## Comportamiento añadido

### Perfil Lite

Configura automáticamente como locales:

- BACKUPS_HOST=127.0.0.1
- SERVICIOS_HOST=127.0.0.1
- LOGS_DB_HOST=127.0.0.1
- TERMINAL_DATABASE_HOST=127.0.0.1

### Perfil Standard

Permite usar un servidor común para:

- DB
- Backups
- Servicios
- Logs

Este perfil queda como opción recomendada para PyME.

### Perfil Pro

Permite separar:

- Servidor de backups.
- Servidor de servicios.
- Servidor de DB/logs.

### Perfil Custom

Permite configuración manual flexible.

## Variables soportadas

El instalador puede recibir por entorno:

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

como valor limpio para cliente real.

## Commit funcional

- 29745ab feat: adaptar instalador api a perfiles

## Validación en lab-pruebas

Se validó:

- Repo actualizado a 29745ab.
- Sintaxis Bash del instalador correcta.
- Bloque R-051D presente en install_dasc_api.sh.
- Variables DASC_PROFILE_VALUE presentes.
- Servicio dasc-api sigue activo.
- Servicio nginx sigue activo.
- Panel local directo por 8000 sigue respondiendo.
- Panel local por Nginx 8080 sigue respondiendo.

## Resultado

R-051D queda validada sin reinstalar el panel activo.

La instalación actual no se rompe y el instalador queda preparado para trabajar con perfiles reales.

## Próximo paso

Continuar con:

- R-051E - Adaptar instalador DB
