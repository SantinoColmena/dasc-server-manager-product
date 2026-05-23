# F6-GATE-01 - Validación real de instalación API en Ubuntu

## Objetivo

Validar que el paquete API de DASC Server Manager no solo está correcto en GitHub, sino preparado para instalarse y comprobarse en una máquina Ubuntu real.

## Motivo

Antes de avanzar hacia clientes o pilotos de pago, el producto debe superar una puerta técnica de instalación real.

No basta con que el repositorio esté limpio o que los scripts existan.

Debe comprobarse que una instalación real crea correctamente:

- Directorio `/opt/dasc/api`.
- Archivo `config.env`.
- Directorio `data`.
- Directorio `reports`.
- Directorio `tools`.
- Entorno virtual Python.
- Servicio systemd `dasc-api`.
- Informe operativo.
- Validador post-instalación.

## Herramienta creada

Se añade el script:

~~~text
deploy/api/package/tools/check_api_installation.sh
~~~

En una instalación real queda en:

~~~text
/opt/dasc/api/tools/check_api_installation.sh
~~~

## Ejecución esperada en Ubuntu

~~~bash
cd /opt/dasc/api
sudo ./tools/check_api_installation.sh "DASC validacion" "2026-05"
~~~

## Salida esperada

El script genera un informe en:

~~~text
/opt/dasc/api/reports/validacion_instalacion_api_YYYYMMDD-HHMMSS.md
~~~

## Criterio de éxito

La validación se considera correcta si:

- Todas las comprobaciones salen OK.
- El servicio `dasc-api` existe.
- El servicio está activo.
- El panel responde en `http://127.0.0.1:8000`.
- Se puede generar el informe operativo.
- No se detectan errores de permisos o rutas.

## Estado

Pendiente de ejecutar en Ubuntu real.

## Conclusión

Esta puerta no sustituye a las tareas del Excel, pero evita avanzar hacia ventas con una instalación no validada.
