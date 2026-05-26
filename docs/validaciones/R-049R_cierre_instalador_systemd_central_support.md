# R-049R - Cierre instalador systemd para central-support

## Objetivo

Cerrar la validación del instalador systemd del panel central DASC.

## Estado

Cerrada.

## Funcionalidad implementada

R-049R permite instalar `central-support` como servicio systemd real, evitando depender de ejecuciones manuales con `nohup`.

El panel central queda instalado en:

~~~text
/opt/dasc/central-support
~~~

y gestionado por el servicio:

~~~text
dasc-central-support
~~~

## Archivos añadidos

~~~text
deploy/central-support/install_central_support.sh
deploy/central-support/uninstall_central_support.sh
~~~

## Archivos de documentación relacionados

~~~text
docs/validaciones/R-049R_instalador_systemd_central_support.md
docs/validaciones/R-049R_FIX1_permisos_instalador_central_support.md
~~~

## Servicio systemd creado

Unidad:

~~~text
/etc/systemd/system/dasc-central-support.service
~~~

Contenido principal validado:

~~~text
User=dasc
Group=dasc
WorkingDirectory=/opt/dasc/central-support
EnvironmentFile=/opt/dasc/central-support/config.env
ExecStart=/opt/dasc/central-support/venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8010
Restart=always
RestartSec=5
~~~

## Puerto validado

~~~text
8010
~~~

## Problema detectado durante la primera validación

La primera ejecución del servicio falló con:

~~~text
status=200/CHDIR
Changing to the requested working directory failed: Permission denied
~~~

La causa fue que el directorio padre:

~~~text
/opt/dasc
~~~

no permitía al usuario `dasc` atravesar hasta:

~~~text
/opt/dasc/central-support
~~~

## Fix aplicado

Se aplicó R-049R-FIX1.

El instalador ahora:

~~~text
Crea el directorio padre de instalación.
Aplica permisos 755 al directorio padre.
Ajusta propietario del directorio instalado a dasc:dasc.
Aplica permisos 750 al directorio de la aplicación.
Aplica permisos 750 al directorio data.
Aplica permisos 600 a config.env.
Evita copiar logs y bases SQLite del entorno fuente.
~~~

Commit relacionado:

~~~text
81a1832 fix: corregir permisos instalador central support
~~~

## Validación del instalador corregido

Se reejecutó el instalador corregido:

~~~text
sudo bash deploy/central-support/install_central_support.sh
~~~

Resultado validado:

~~~text
OK: DASC Central Support instalado.
URL local: http://127.0.0.1:8010
Servicio: dasc-central-support
Directorio: /opt/dasc/central-support
~~~

## Validación de estado del servicio

Se comprobó:

~~~text
systemctl is-active dasc-central-support
active
~~~

También:

~~~text
systemctl is-enabled dasc-central-support
enabled
~~~

## Validación health

Se comprobó:

~~~text
GET http://127.0.0.1:8010/health
~~~

Respuesta:

~~~text
status: ok
app: DASC Central Support
db: /opt/dasc/central-support/data/central_support.db
demo_client_id: cliente-demo-a
~~~

## Validación login

Sin sesión, el panel central redirige correctamente:

~~~text
GET /
HTTP 303
location: /login?msg=Sesion+requerida
~~~

Login administrador validado:

~~~text
POST /login admin/admin
HTTP 303
location: /
~~~

Dashboard autenticado validado:

~~~text
GET /
HTTP 200
~~~

## Validación API por token

Se creó un ticket por API usando token de cliente:

~~~text
POST /api/v1/support/tickets
~~~

Resultado:

~~~text
ok: true
central_ticket_id: CENTRAL-2026-0002
estado: Nuevo
mensaje: Ticket recibido en API central DASC
~~~

Esto confirma que el login web no rompe la API usada por paneles locales.

## Validación reinicio systemd

Se ejecutó:

~~~text
sudo systemctl restart dasc-central-support
~~~

Resultado posterior:

~~~text
systemctl is-active dasc-central-support
active
~~~

Y `/health` volvió a responder correctamente.

## Validación de logs

Los logs recientes muestran arranque correcto:

~~~text
Started DASC Central Support (FastAPI/Uvicorn)
Application startup complete.
Uvicorn running on http://0.0.0.0:8010
GET /health HTTP/1.1 200 OK
POST /api/v1/support/tickets HTTP/1.1 200 OK
~~~

No aparecen errores nuevos de `CHDIR` tras aplicar el FIX1.

## Validación técnica

Se comprobó:

~~~text
Instalador ejecutado: OK
Dependencias del sistema instaladas/verificadas: OK
Entorno virtual creado/verificado: OK
Requirements instalados: OK
config.env creado/conservado: OK
Permisos corregidos: OK
Servicio systemd creado: OK
Servicio habilitado: OK
Servicio arrancado: OK
Health responde: OK
Login responde: OK
API por token responde: OK
Reinicio systemd funciona: OK
Logs recientes limpios: OK
~~~

## Resultado

R-049R queda validada correctamente.

`central-support` ya puede instalarse y mantenerse como servicio systemd real.

## Límites actuales

Esta versión todavía no incluye:

- Reverse proxy Nginx.
- HTTPS.
- Dominio público.
- Rotación avanzada de logs.
- Endurecimiento de credenciales.
- Variables productivas obligatorias.
- Instalación multi-cliente definitiva.
- Gestión de backups de la base central.

## Próxima tarea recomendada

~~~text
R-049S - Reintento automático mediante systemd timer
~~~

También queda pendiente:

~~~text
R-049T - Mejoras visuales del panel central
R-049U - Endurecimiento de credenciales del panel central
R-049V - Reverse proxy Nginx para central-support
~~~

## Conclusión

DASC Server Manager supera R-049R.

El panel central ya no depende de ejecución manual: queda instalado, habilitado, reiniciable y operativo mediante systemd.
