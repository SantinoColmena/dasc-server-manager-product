# Validación - Informe operativo dentro del paquete API

## Objetivo

Validar que el informe mensual empieza a evolucionar desde herramienta interna de GitHub hacia herramienta real incluida en el producto.

## Archivos validados

~~~text
deploy/api/package/tools/generate_operational_report.py
deploy/api/package/reports/.gitkeep
docs/producto/informe_operativo_paquete_api.md
~~~

## Prueba en Windows

Comando usado:

~~~powershell
py -3 .\deploy\api\package\tools\generate_operational_report.py --root .\deploy\api\package --client "DASC interno" --period "2026-05"
~~~

## Resultado obtenido

El script generó correctamente el informe operativo en:

~~~text
deploy/api/package/reports/informe_operativo_2026-05.md
~~~

El informe incluyó:

- Cliente o entorno.
- Periodo.
- Ruta revisada.
- Archivo de configuración leído.
- Modo de configuración.
- Configuración mínima.
- Variables relevantes enmascaradas.
- Archivos runtime.
- Estado de la base de datos de logs.
- Limitaciones.
- Conclusión.

## Resultado de configuración

La configuración mínima se detectó correctamente usando:

~~~text
deploy/api/package/config.env.example
~~~

Todas las variables mínimas aparecieron como presentes.

## Resultado de seguridad

Las variables sensibles se mostraron enmascaradas.

Ejemplos:

~~~text
ADMIN_PASSWORD = ***
LOGS_DB_PASS = ***
SECRET_KEY = ***
~~~

## Resultado de logs

En la prueba local desde Windows apareció:

~~~text
No module named 'pymysql'
~~~

Esto se considera aceptable en esta validación porque la prueba se ejecutó con Python local de Windows y no con el entorno virtual real del API instalado.

En una instalación real, el script debe ejecutarse desde el entorno del API:

~~~bash
cd /opt/dasc/api
./venv/bin/python tools/generate_operational_report.py --root /opt/dasc/api --client "Cliente demo" --period "2026-05"
~~~

## Decisión sobre informes generados

Los informes generados en:

~~~text
deploy/api/package/reports/*.md
~~~

no deben versionarse.

Son archivos runtime generados por la herramienta.

Solo se mantiene:

~~~text
deploy/api/package/reports/.gitkeep
~~~

## Conclusión

La validación demuestra que el informe operativo ya no es solo una herramienta interna del repositorio.

Ahora existe una utilidad incluida dentro del paquete API, preparada para ejecutarse en una instalación real de DASC Server Manager.

Estado de madurez:

~~~text
Nivel 2 - Herramienta de producto validada inicial
~~~

Todavía no es herramienta final de cliente porque falta:

- Integración con panel.
- Lectura real de backups.
- Lectura real de restauraciones.
- Exportación PDF.
- Envío o entrega simple al cliente.
