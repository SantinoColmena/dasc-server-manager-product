# R-049R-FIX1 - Corregir permisos del instalador central-support

## Objetivo

Corregir el instalador systemd de `central-support` para que el servicio pueda acceder a su directorio de trabajo.

## Estado

Cerrada.

## Problema detectado

Durante la validación de R-049R, el servicio quedó en bucle de reinicio con:

~~~text
status=200/CHDIR
Changing to the requested working directory failed: Permission denied
~~~

La unidad systemd ejecutaba el servicio como:

~~~text
User=dasc
WorkingDirectory=/opt/dasc/central-support
~~~

pero el directorio padre `/opt/dasc` no permitía acceso al usuario `dasc`.

## Solución aplicada

El instalador ahora:

- Crea el directorio padre de instalación.
- Aplica permisos `755` al directorio padre.
- Ajusta propietario del directorio instalado a `dasc:dasc`.
- Aplica permisos `750` al directorio de la aplicación.
- Aplica permisos `750` al directorio `data`.
- Aplica permisos `600` a `config.env`.
- Evita copiar logs y bases de datos SQLite del entorno fuente al destino instalado.

## Archivo modificado

~~~text
deploy/central-support/install_central_support.sh
~~~

## Criterio de validación

Este fix queda preparado cuando:

- `dasc-central-support` arranca como servicio systemd.
- `systemctl is-active dasc-central-support` devuelve `active`.
- `/health` responde en el puerto 8010.
- No aparece `status=200/CHDIR`.
- El instalador puede ejecutarse de nuevo sin romper la instalación.
