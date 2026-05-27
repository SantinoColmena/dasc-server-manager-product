# R-052B - Auditoría de permisos de instalación local API

## Objetivo

Auditar permisos de la instalación local del panel/API DASC en `/opt/dasc/api`.

## Estado

Cerrada.

## Resultado detectado

La instalación actual tiene:

- /opt/dasc/api propiedad de santino:santino.
- dasc-api ejecutándose como User=santino y Group=santino.
- /opt/dasc/api/config.env con permisos 640 y propietario santino:santino.
- El usuario santino puede leer /opt/dasc/api/config.env.
- /opt/dasc/api/data/users.json con permisos 644.
- /opt/dasc/api/data/alerts.db con permisos 644.
- /opt/dasc/api/data/support_tickets.db con permisos 644.
- /opt/dasc/api/.ssh/id_rsa_dasc con permisos 600.

## Punto positivo

La clave privada SSH del API está protegida con permisos 600.

## Punto positivo

El archivo `users.json` usa `password_hash` y no contraseña plana.

Validación observada:

- password_hash=True
- password_plano=False

## Riesgo principal

El panel local se ejecuta con un usuario humano del sistema:

- santino

Esto implica que ese mismo usuario puede leer el `config.env` del panel local.

## Comparación con central-support

central-support está mejor protegido:

- Servicio ejecutado como usuario `dasc`.
- config.env central con root:root.
- permisos 600.
- usuario normal no puede leerlo.

## Conclusión

R-052B queda validada.

Se recomienda migrar dasc-api a un usuario técnico dedicado, por ejemplo `dasc-api`, y proteger `config.env`, `data/` y ficheros runtime.
