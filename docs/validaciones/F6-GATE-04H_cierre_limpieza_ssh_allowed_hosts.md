# F6-GATE-04H - Cierre limpieza SSH allowed hosts y ajuste final de logs

## Objetivo

Cerrar la limpieza fina de configuración SSH y validar que la API sigue funcionando correctamente después de eliminar duplicados en `DASC_SSH_ALLOWED_HOSTS`.

## Estado

Cerrada.

## Archivo modificado

~~~text
deploy/api/install_dasc_api.sh
~~~

## Cambio aplicado en código

Se añadió la función:

~~~text
build_unique_csv
~~~

El instalador API ahora genera `DASC_SSH_ALLOWED_HOSTS` evitando duplicados cuando varios roles apuntan a la misma máquina.

## Configuración runtime validada

En `lab-pruebas` se limpió la configuración real:

~~~text
DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.30,192.168.60.20
~~~

## Validación API

Después de reiniciar `dasc-api`, se comprobó:

~~~text
Servicio dasc-api: active
HTTP local: 303 See Other -> /login
Puerto 8000: activo
~~~

## Incidencia detectada durante la validación

Durante la comprobación apareció un problema independiente:

~~~text
Access denied for user 'dasc_logs'@'192.168.60.10'
~~~

El problema no estaba causado por `DASC_SSH_ALLOWED_HOSTS`.

La causa fue una desalineación entre la contraseña de `LOGS_DB_PASS` en `/opt/dasc/api/config.env` y la contraseña del usuario MariaDB `dasc_logs`.

## Corrección aplicada

Se alineó `LOGS_DB_PASS` en el `config.env` runtime con la contraseña configurada en MariaDB:

~~~text
LOGS_DB_HOST=192.168.60.20
LOGS_DB_NAME=dasc_logs
LOGS_DB_USER=dasc_logs
LOGS_DB_PASS=***
~~~

Después se reinició el servicio API.

## Validación de logs

Desde `lab-pruebas`, la prueba Python contra MariaDB devolvió:

~~~text
Resultado: OK
Eventos: 21
~~~

Después de forzar nuevas peticiones HTTP, en `lab-db-gate02` se comprobó:

~~~text
total_eventos = 22
~~~

Últimos eventos registrados:

~~~text
id 22 | dasc-web | acceso | anon | 127.0.0.1 | HEAD / | ERROR
id 21 | dasc-web | acceso | anon | 127.0.0.1 | HEAD / | ERROR
~~~

Esto confirma que la API vuelve a guardar eventos correctamente en la base remota `dasc_logs`.

## Observación

Los errores `Access denied` que aparecen en `journalctl` son históricos, anteriores a la corrección.

Después del reinicio y la alineación de contraseña, la API registra eventos correctamente.

## Criterio de cierre

F6-GATE-04H se considera cerrada porque:

- El instalador API evita duplicados en `DASC_SSH_ALLOWED_HOSTS`.
- La configuración runtime quedó limpia.
- `dasc-api` sigue activo.
- El panel responde correctamente.
- La conexión a `dasc_logs` volvió a funcionar.
- Se registraron nuevos eventos en la base remota.
- La incidencia de contraseña de logs fue corregida.

## Próxima puerta

~~~text
F6-GATE-05 - Soporte real sin GitHub para cliente
~~~

## Conclusión

DASC Server Manager supera la limpieza fina de configuración SSH.

El bloque F6-GATE-04 queda completamente cerrado, incluyendo la validación final de API, SSH allowed hosts y logs remotos.
