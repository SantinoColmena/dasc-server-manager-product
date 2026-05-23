# Informe operativo dentro del paquete API

## Objetivo

Convertir el informe mensual desde una herramienta interna del repositorio hacia una herramienta real incluida en el producto.

## Diferencia con el informe interno

El informe interno anterior se genera desde:

~~~text
tools/windows/generate_monthly_report.ps1
~~~

Ese informe sirve al equipo para revisar el estado del repositorio, commits y auditoría clean.

El nuevo informe operativo se incluye dentro del paquete API:

~~~text
deploy/api/package/tools/generate_operational_report.py
~~~

En una instalación real quedaría disponible en:

~~~text
/opt/dasc/api/tools/generate_operational_report.py
~~~

## Qué aporta este cambio

Este cambio acerca la herramienta al producto real porque:

- Ya no depende de que el cliente entre a GitHub.
- Viaja dentro del paquete instalable de la API.
- Puede ejecutarse desde el servidor instalado.
- Lee configuración del entorno DASC.
- Enmascara valores sensibles.
- Puede consultar la base de datos de logs si está disponible.
- Genera informes dentro de la propia instalación.

## Uso en entorno instalado

Ejemplo en servidor API:

~~~bash
cd /opt/dasc/api
./venv/bin/python tools/generate_operational_report.py --root /opt/dasc/api --client "Cliente demo" --period "2026-05"
~~~

Salida esperada:

~~~text
/opt/dasc/api/reports/informe_operativo_2026-05.md
~~~

## Estado de madurez

Nivel actual:

~~~text
Nivel 2 - Herramienta de producto validada inicial
~~~

Todavía no es una herramienta final de cliente porque:

- No genera PDF.
- No se envía por email.
- No resume todavía en lenguaje completamente no técnico.
- No consulta aún backups reales ni restauraciones reales.
- No está integrada en el panel web.

## Próxima evolución

Para llegar a herramienta lista para cliente deberá:

- Leer historial real de backups.
- Leer última restauración de prueba.
- Incluir alertas enviadas.
- Incluir estado de servicios.
- Generar resumen no técnico.
- Poder entregarse por email, PDF o desde el panel.

## Conclusión

El informe operativo del paquete API es el primer paso real para pasar de una herramienta interna en GitHub a una herramienta integrada en el producto.
