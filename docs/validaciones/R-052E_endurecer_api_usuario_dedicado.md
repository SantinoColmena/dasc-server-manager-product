# R-052E - Endurecer panel local API con usuario dedicado

## Objetivo

Endurecer la instalación local del panel/API DASC para que deje de ejecutarse como usuario humano y pase a ejecutarse con un usuario técnico dedicado.

## Estado

En curso.

## Problema detectado

Durante R-052B se detectó:

- dasc-api ejecutándose como User=santino.
- /opt/dasc/api/config.env propiedad de santino:santino.
- El usuario santino podía leer config.env.
- data/users.json, alerts.db y support_tickets.db con permisos 644.
- Puerto 8000 expuesto en 0.0.0.0.

## Decisión aplicada

Crear un script de hardening:

- deploy/api/harden_dasc_api_security.sh

Este script:

- Crea grupo técnico dasc-api si no existe.
- Crea usuario técnico dasc-api si no existe.
- Para el servicio dasc-api.
- Hace backup de la unidad systemd.
- Cambia User y Group del servicio a dasc-api.
- Cambia Uvicorn de 0.0.0.0 a 127.0.0.1.
- Protege config.env como root:dasc-api 640.
- Protege data/ como dasc-api:dasc-api.
- Protege .ssh/.
- Reinicia el servicio.
- Valida acceso local.
- Valida que el usuario normal no pueda leer config.env.

## Resultado esperado

Después de aplicar R-052E:

- dasc-api corre como dasc-api.
- config.env no puede ser leído por usuario normal.
- data/ queda privado para el servicio.
- puerto 8000 deja de exponerse externamente.
- Nginx sigue dando acceso al panel local.

## Acceso esperado

En laboratorio:

- http://192.168.1.250:8080/

En cliente real:

- http://IP_CLIENTE/
- o DNS local si el cliente lo configura.

## Criterio de validación

R-052E se considerará validada cuando:

- dasc-api active.
- dasc-api User=dasc-api.
- dasc-api Group=dasc-api.
- ExecStart usa --host 127.0.0.1.
- config.env queda root:dasc-api 640.
- usuario normal no puede leer config.env.
- users.json no contiene password plano.
- panel local por Nginx responde.
- panel central sigue funcionando.
- repo queda limpio.
