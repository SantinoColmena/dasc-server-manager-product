# R-052E - Cierre endurecimiento panel local API con usuario dedicado

## Objetivo

Cerrar la validación del endurecimiento del panel local API mediante usuario técnico dedicado y permisos restrictivos.

## Estado

Cerrada.

## Contexto

Durante R-052B se detectó que el servicio `dasc-api` se ejecutaba como usuario humano del sistema:

- santino

También se detectó que:

- /opt/dasc/api/config.env pertenecía a santino:santino.
- El usuario santino podía leer config.env.
- data/users.json, alerts.db y support_tickets.db tenían permisos 644.
- El puerto 8000 escuchaba en 0.0.0.0.

## Cambio aplicado

Se creó y ejecutó el script:

- deploy/api/harden_dasc_api_security.sh

El script aplica hardening sobre la instalación local del panel/API.

## Commit funcional

- 17f6ff5 feat: endurecer seguridad api local

## Cambios realizados

### Usuario de servicio

Antes:

- User=santino
- Group=santino

Después:

- User=dasc-api
- Group=dasc-api

### Unidad systemd

Antes:

- ExecStart=/opt/dasc/api/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

Después:

- ExecStart=/opt/dasc/api/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000

### Permisos config.env

Después del hardening:

- /opt/dasc/api/config.env
- root:dasc-api
- 640

Validación:

- El usuario normal santino no puede leer config.env.

### Permisos data/

Después del hardening:

- /opt/dasc/api/data
- dasc-api:dasc-api
- directorios 750
- ficheros 640

Ficheros protegidos:

- alerts.db
- auth_logs.json
- support_tickets.db
- support_tickets.json
- users.json

### Permisos SSH

Después del hardening:

- /opt/dasc/api/.ssh
- dasc-api:dasc-api
- directorio 700
- clave privada id_rsa_dasc 600
- clave pública 644
- known_hosts_dasc 644

## Validaciones realizadas

Se validó:

- dasc-api active.
- dasc-api ejecutándose como dasc-api.
- ExecStart usando 127.0.0.1.
- config.env protegido como root:dasc-api 640.
- usuario normal santino no puede leer config.env.
- users.json mantiene password_hash.
- users.json no contiene password plano.
- puerto 8000 escucha solo en 127.0.0.1.
- panel local directo local responde en 127.0.0.1:8000.
- panel local por Nginx responde en 8080.
- panel central por Nginx responde en 80.
- central-support health responde en 8010.
- repo limpio.

## Estado final de acceso

Acceso recomendado al panel local en laboratorio:

- http://192.168.1.250:8080/

El puerto 8000 queda como backend interno local:

- http://127.0.0.1:8000/

## Resultado

R-052E queda cerrada correctamente.

El panel local API deja de ejecutarse como usuario humano y pasa a ejecutarse con un usuario técnico dedicado, con secretos y ficheros runtime más protegidos.

## Pendiente relacionado

El puerto 8010 de central-support sigue escuchando en 0.0.0.0.

Ese punto se tratará en una tarea posterior de endurecimiento de central-support o en la validación final de exposición de puertos.
