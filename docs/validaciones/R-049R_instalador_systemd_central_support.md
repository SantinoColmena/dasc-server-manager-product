# R-049R - Instalador systemd para central-support

## Objetivo

Crear un instalador real para ejecutar el panel central DASC como servicio systemd.

## Estado

Cerrada.

## Contexto

Hasta ahora `central-support` se validaba manualmente con:

~~~text
nohup ./venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8010
~~~

Esto sirve para laboratorio, pero no es suficiente para un despliegue mantenible.

## Archivos añadidos

~~~text
deploy/central-support/install_central_support.sh
deploy/central-support/uninstall_central_support.sh
~~~

## Servicio creado

~~~text
dasc-central-support
~~~

Unidad systemd:

~~~text
/etc/systemd/system/dasc-central-support.service
~~~

## Directorio de instalación

~~~text
/opt/dasc/central-support
~~~

## Puerto

~~~text
8010
~~~

## Variables principales

~~~text
DASC_CENTRAL_AUTH_ENABLED
DASC_CENTRAL_SECRET_KEY
DASC_CENTRAL_ADMIN_USER
DASC_CENTRAL_ADMIN_PASSWORD
DASC_CENTRAL_TECH_USER
DASC_CENTRAL_TECH_PASSWORD
DASC_CENTRAL_DEMO_CLIENT_ID
DASC_CENTRAL_DEMO_CLIENT_NAME
DASC_CENTRAL_DEMO_TOKEN
~~~

## Criterio de validación

R-049R queda preparada cuando:

- El instalador copia el paquete a `/opt/dasc/central-support`.
- Crea entorno virtual.
- Instala requirements.
- Crea `config.env` si no existe.
- Crea servicio systemd.
- Activa y arranca `dasc-central-support`.
- `/health` responde en el puerto 8010.
- `/` redirige a `/login` sin sesión.
- Login central sigue funcionando.
- API por token sigue funcionando.
- El desinstalador elimina servicio y directorio.

## Límites

Esta tarea todavía no incluye:

- Reverse proxy Nginx.
- HTTPS.
- Dominio público.
- Rotación de logs.
- Endurecimiento de credenciales.
- Instalación multi-cliente productiva.

## Próximo paso

Validar en `lab-pruebas`.

## Conclusión

R-049R convierte `central-support` en un servicio instalable y reiniciable automáticamente, acercándolo a un despliegue real.
