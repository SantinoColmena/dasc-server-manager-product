# Uso del informe operativo en instalación real

## Objetivo

Documentar cómo ejecutar el informe operativo cuando DASC Server Manager ya está instalado en un servidor API.

## Ruta esperada

En una instalación real, el generador queda en:

~~~text
/opt/dasc/api/tools/generate_operational_report.py
~~~

También existe un wrapper cómodo:

~~~text
/opt/dasc/api/tools/generate_operational_report.sh
~~~

## Ejecución recomendada

Desde el servidor API:

~~~bash
cd /opt/dasc/api
./tools/generate_operational_report.sh "Cliente demo" "2026-05"
~~~

## Salida esperada

El informe se genera en:

~~~text
/opt/dasc/api/reports/informe_operativo_2026-05.md
~~~

## Ejecución manual alternativa

También se puede ejecutar directamente con Python del entorno virtual:

~~~bash
cd /opt/dasc/api
./venv/bin/python tools/generate_operational_report.py --root /opt/dasc/api --client "Cliente demo" --period "2026-05"
~~~

## Qué revisa actualmente

La versión actual revisa:

- Configuración mínima.
- Variables relevantes enmascaradas.
- Archivos runtime.
- Base de datos de logs si está disponible.
- Limitaciones del estado actual.
- Conclusión operativa.

## Qué no hace todavía

No sustituye un informe mensual final de cliente.

Todavía no incluye:

- Historial real de backups.
- Restauraciones de prueba.
- Alertas enviadas.
- Estado de servicios.
- Exportación PDF.
- Envío por email.
- Vista desde panel web.

## Conclusión

El informe operativo ya está preparado para ejecutarse desde una instalación real de DASC, no solo desde GitHub.
