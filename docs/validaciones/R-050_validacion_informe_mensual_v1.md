# R-050 - Validación informe mensual automático v1

## Tarea

Informe mensual automático v1.

## Objetivo de validación

Comprobar que existe una primera versión funcional de generación automática de informes mensuales.

## Archivos esperados

~~~text
tools/windows/generate_monthly_report.ps1
docs/informes/R-050_informe_mensual_automatico_v1.md
docs/informes/informe_mensual_v1_2026-05.md
~~~

## Prueba realizada

Comando recomendado:

~~~powershell
powershell -ExecutionPolicy Bypass -File .\tools\windows\generate_monthly_report.ps1 -Cliente "DASC interno" -Periodo "2026-05"
~~~

## Resultado esperado

Debe generarse un informe Markdown en:

~~~text
docs/informes/informe_mensual_v1_2026-05.md
~~~

El informe debe incluir:

- Cliente o entorno.
- Periodo.
- Fecha de generación.
- Rama.
- Commit.
- Versión o tag detectado.
- Estado de Git.
- Últimos commits.
- Resultado de auditoría clean.
- Conclusión.

## Limitaciones aceptadas

Esta primera versión no consulta todavía datos reales de producción.

No incluye todavía:

- Backups reales.
- Restauraciones reales.
- Alertas reales.
- Tickets reales.
- Envío por email.
- PDF automático.

## Estado

R-050 queda en curso hasta generar, revisar y commitear el primer informe v1.
