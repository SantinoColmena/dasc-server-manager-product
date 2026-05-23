# R-050 - Informe mensual automático v1

## Objetivo

Crear una primera versión real de informe mensual automático para DASC Server Manager.

## Estado

En curso.

## Enfoque correcto

Esta tarea no se cerrará fingiendo que ya existe un sistema completo de informes comerciales para clientes.

La primera versión se plantea como un informe automático interno generado desde Windows.

## Qué hace la versión v1

El script `tools/windows/generate_monthly_report.ps1` genera un informe Markdown con:

- Cliente o entorno.
- Periodo.
- Fecha de generación.
- Rama actual.
- Commit actual.
- Tag o versión detectada.
- Estado de Git.
- Últimos commits.
- Resultado de auditoría clean.
- Conclusión básica.

## Qué no hace todavía

La versión v1 no hace todavía:

- Consulta real de backups en servidores.
- Consulta real de restauraciones.
- Consulta real de alertas.
- Consulta real de tickets cerrados.
- Exportación automática a PDF.
- Envío automático por email.
- Informe final para cliente no técnico.

## Por qué se hace así

Antes de vender a una PyME hay que tener una base limpia y repetible.

El informe mensual comercial llegará después, cuando el producto pueda recoger datos reales del entorno instalado.

## Uso previsto

Ejemplo:

~~~powershell
powershell -ExecutionPolicy Bypass -File .\tools\windows\generate_monthly_report.ps1 -Cliente "DASC interno" -Periodo "2026-05"
~~~

## Salida esperada

El informe se genera en:

~~~text
docs/informes/informe_mensual_v1_YYYY-MM.md
~~~

## Criterio para cerrar R-050

R-050 se podrá cerrar cuando:

- Exista el script generador.
- Exista documentación de su alcance.
- Se genere al menos un informe v1.
- El informe indique estado del repositorio y auditoría clean.
- Quede claro que no es todavía informe comercial final de cliente.

## Conclusión

R-050 avanza como una mejora real de producto interno.

Más adelante se podrá convertir en informe mensual real para cliente.
