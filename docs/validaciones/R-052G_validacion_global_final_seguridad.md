# R-052G - Validación global final de seguridad

## Objetivo

Validar globalmente el estado de seguridad del panel local, central-support, secretos, permisos, puertos internos, Nginx y repositorio tras las correcciones de R-052.

## Estado

Cerrada.

## Contexto

Durante R-052 se revisaron y corrigieron aspectos de seguridad relacionados con:

- secretos en repositorio,
- permisos de config.env,
- usuarios de servicio,
- ficheros runtime,
- exposición de puertos internos,
- Nginx,
- SSH,
- users.json,
- procesos del sistema.

## Servicios validados

Se validó que están activos:

- dasc-api
- dasc-central-support
- nginx
- dasc-central-retry.timer

También se validó que están enabled.

## Usuarios de servicio

### dasc-api

La unidad systemd quedó con:

- User=dasc-api
- Group=dasc-api
- ExecStart con --host 127.0.0.1 --port 8000

### central-support

La unidad systemd quedó con:

- User=dasc
- Group=dasc
- ExecStart con --host 127.0.0.1 --port 8010

## Puertos internos

Se validó:

- 8000 escucha en 127.0.0.1:8000.
- 8010 escucha en 127.0.0.1:8010.
- 8000 no escucha en 0.0.0.0.
- 8010 no escucha en 0.0.0.0.

Esto deja los backends internos detrás de Nginx.

## Puertos públicos de laboratorio

En laboratorio quedan públicos:

- 22 SSH.
- 80 Nginx panel central.
- 8080 Nginx panel local.

## Permisos de config.env

### API local

Se validó:

- /opt/dasc/api/config.env
- root:dasc-api
- 640

El usuario normal `santino` no puede leerlo.

### Central support

Se validó:

- /opt/dasc/central-support/config.env
- root:root
- 600

El usuario normal `santino` no puede leerlo.

## Permisos de data API

Se validó que `/opt/dasc/api/data` queda protegido como:

- dasc-api:dasc-api
- directorio 750
- ficheros 640

Incluye:

- alerts.db
- auth_logs.json
- support_tickets.db
- support_tickets.json
- users.json

## Permisos SSH API

Se validó:

- /opt/dasc/api/.ssh con permisos 700.
- id_rsa_dasc con permisos 600.
- id_rsa_dasc.pub con permisos 644.
- known_hosts_dasc con permisos 644.
- propietario dasc-api:dasc-api.

## users.json

Se validó que `users.json` no contiene password plano.

Resultado observado:

- usuario tecnico
- password_hash=True
- password_plano=False

## Nginx

Se validó:

- nginx -t correcto.
- dasc-api-local en 8080 hacia 127.0.0.1:8000.
- dasc-central-support en 80 hacia 127.0.0.1:8010.

## Accesos HTTP

Se validó:

- API backend local 8000 responde con redirección a login.
- Panel local por Nginx 8080 responde con redirección a login.
- Central backend local 8010 /health responde correctamente.
- Panel central por Nginx 80 responde con redirección a login.

## Procesos

Se validó que los procesos no muestran secretos en argumentos.

Procesos relevantes:

- dasc-api ejecutando uvicorn con --host 127.0.0.1 --port 8000.
- central-support ejecutando uvicorn con --host 127.0.0.1 --port 8010.

## Repo y deploy

Se validó:

- No hay IPs fijas de laboratorio en deploy.
- No hay defaults débiles activos.
- No hay archivos runtime sensibles versionados con los patrones revisados.
- Repositorio limpio.

## Resultado

R-052G queda validada correctamente.

El estado final de seguridad es notablemente mejor que al inicio de R-052:

- el panel local ya no corre como usuario humano,
- los secretos están protegidos,
- los backends internos no están expuestos directamente,
- Nginx queda como punto de entrada,
- users.json mantiene hashes,
- el repositorio queda limpio de secretos runtime.

## Próximo paso

Continuar con:

- R-052H - Cierre global de R-052
