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

Comando alternativo:

~~~powershell
python .\deploy\api\package\tools\generate_operational_report.py --root .\deploy\api\package --client "DASC interno" --period "2026-05"
~~~

## Resultado esperado

Debe generarse:

~~~text
deploy/api/package/reports/informe_operativo_2026-05.md
~~~

## Comprobaciones

El informe debe incluir:

- Cliente o entorno.
- Periodo.
- Ruta revisada.
- Archivo de configuración leído.
- Configuración mínima.
- Variables relevantes enmascaradas.
- Archivos runtime.
- Estado de la base de datos de logs.
- Limitaciones.
- Conclusión.

## Resultado

Pendiente de pegar salida real tras ejecutar la prueba.

## Conclusión

Esta validación permite demostrar que el informe ya no es solo una herramienta interna del repositorio, sino una utilidad incluida en el paquete API.
