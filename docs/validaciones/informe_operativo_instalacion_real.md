# Validación - Informe operativo preparado para instalación real

## Objetivo

Validar que el informe operativo ya no solo está dentro del paquete API, sino que queda preparado para ejecutarse en una instalación real.

## Archivos validados

~~~text
deploy/api/package/tools/generate_operational_report.py
deploy/api/package/tools/generate_operational_report.sh
deploy/api/install_dasc_api.sh
docs/producto/uso_informe_operativo_instalacion_real.md
~~~

## Cambios realizados

Se añade un wrapper Bash:

~~~text
tools/generate_operational_report.sh
~~~

Este wrapper permite ejecutar el informe desde `/opt/dasc/api` usando el entorno virtual del API.

## Comando esperado en servidor instalado

~~~bash
cd /opt/dasc/api
./tools/generate_operational_report.sh "Cliente demo" "2026-05"
~~~

## Salida esperada

~~~text
/opt/dasc/api/reports/informe_operativo_2026-05.md
~~~

## Ajustes en instalador

El instalador API prepara:

- Directorio `data`.
- Directorio `reports`.
- Directorio `tools`.
- Permisos de ejecución para scripts de informe.

## Estado de madurez

Con este cambio el informe operativo avanza dentro del Nivel 2:

~~~text
Herramienta de producto validada inicial
~~~

Aún no pasa a Nivel 3 porque todavía no está integrada en panel, PDF, email o canal simple de cliente.

## Conclusión

La herramienta ya está preparada para instalación real, aunque todavía no es informe final para cliente.
