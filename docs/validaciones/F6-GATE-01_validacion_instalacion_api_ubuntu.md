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

## Hallazgo durante la primera prueba

Durante la primera instalación limpia en Ubuntu `lab-pruebas`, el instalador avanzó correctamente hasta crear el servicio y preparar el entorno API, pero falló al intentar registrar la huella SSH del host de backups `192.168.60.30`.

Esto demuestra que el instalador API estaba bloqueando una instalación de 1 servidor por depender de un nodo externo de backups.

## Decisión técnica

Para la validación API en 1 servidor, la parte SSH hacia backups no debe bloquear la instalación.

El instalador debe:

- Intentar registrar la huella SSH si `BACKUPS_HOST` está configurado.
- Avisar si no puede obtenerla.
- Continuar la instalación API.
- Dejar la validación de conexión con backups para una puerta posterior de 2 servidores.

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

## Separación de puertas

Esta puerta valida solo la instalación API.

No valida todavía:

- Nodo de backups remoto.
- SSH real contra backups.
- Restauraciones.
- Logs contra base de datos remota.
- Arquitectura PyME de 2 servidores.

Esas comprobaciones deben hacerse en puertas posteriores.

## Estado

En curso.

Pendiente repetir instalación limpia tras corregir el comportamiento no bloqueante de SSH hacia backups.

## Conclusión

Esta puerta no sustituye a las tareas del Excel, pero evita avanzar hacia ventas con una instalación no validada.
