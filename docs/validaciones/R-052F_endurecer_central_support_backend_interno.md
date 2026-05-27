# R-052F - Endurecer central-support como backend interno

## Objetivo

Endurecer `central-support` para que deje de exponerse directamente en `0.0.0.0:8010` y pase a funcionar como backend interno detrás de Nginx.

## Estado

Cerrada.

## Problema detectado

Durante R-052C y R-052E se detectó:

- dasc-api ya fue corregido para escuchar en 127.0.0.1:8000.
- central-support seguía escuchando en 0.0.0.0:8010.
- Nginx ya publica el panel central por el puerto 80.

## Decisión aplicada

Central support debe quedar así:

- Nginx escucha públicamente en puerto 80.
- central-support escucha internamente en 127.0.0.1:8010.
- El usuario accede al panel central por Nginx.
- El backend 8010 no debe ser acceso público directo.

## Archivos añadidos

- deploy/central-support/harden_central_support_security.sh

## Archivos modificados

- deploy/central-support/install_central_support.sh
- deploy/central-support/install_nginx_central_support.sh

## Cambios previstos

### Servicio central-support

Antes:

- --host 0.0.0.0 --port 8010

Después:

- --host 127.0.0.1 --port 8010

### Nginx central

Se ajusta la cabecera Host para conservar el host completo:

- proxy_set_header Host $http_host;
- proxy_set_header X-Forwarded-Host $http_host;

## Criterio de validación

R-052F se considerará validada cuando:

- dasc-central-support active.
- systemd use --host 127.0.0.1.
- 8010 escuche en 127.0.0.1 y no en 0.0.0.0.
- /health responda localmente.
- Panel central por Nginx puerto 80 responda.
- Panel local por Nginx 8080 siga funcionando.
- dasc-api siga funcionando.
- Repo limpio.
