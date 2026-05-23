# R-048 - Primer cliente de pago

## Objetivo

Conseguir el primer cliente de pago para DASC Server Manager o, si no se consigue, obtener feedback real suficiente para ajustar la oferta comercial.

## Estado

En curso.

## Punto de partida

La release candidate `v1.0-rc1` ya está creada y etiquetada.

Esto permite presentar DASC Server Manager como una versión candidata controlada, no como una versión final cerrada.

## Cliente objetivo inicial

El perfil recomendado para el primer cliente es:

- Microempresa o pequeña empresa.
- 5 a 30 empleados.
- Uso de base de datos, aplicación local, servidor propio o datos importantes.
- Sin administrador de sistemas interno.
- Necesidad de backups, restauración, logs y soporte sencillo.
- Preocupación por pérdida de datos, errores humanos o falta de control.

Ejemplos de cliente válido:

- Gestoría.
- Asesoría.
- Academia.
- Clínica pequeña.
- Taller.
- Tienda con TPV o stock.
- Empresa con servidor local.
- Negocio con base de datos MariaDB/MySQL.

## Oferta recomendada para primer cliente

Para no complicar la primera venta, se recomienda ofrecer un piloto de pago controlado.

### Opción recomendada

**DASC PyME Inicial**

Incluye:

- Revisión del entorno.
- Instalación de DASC Server Manager.
- Configuración de backups.
- Configuración de logs.
- Validación de una restauración de prueba.
- Configuración de alertas básicas.
- Informe inicial de estado.
- Soporte limitado durante el primer mes.

Precio orientativo:

- Instalación inicial: 250 € a 500 €.
- Mantenimiento mensual opcional: 39 € a 79 €/mes.

Para el primer cliente real se puede aplicar precio reducido si acepta dar feedback y permitir documentar el caso de uso sin datos sensibles.

## Mensaje comercial principal

DASC Server Manager no se vende como un simple panel técnico.

Se vende como un servicio para que una PyME pueda saber:

- Si sus copias existen.
- Si se pueden restaurar.
- Si algo falla.
- Quién ha realizado acciones importantes.
- Qué estado tiene su servidor.
- Qué debe revisar cada mes.

## Qué no prometer

No se debe prometer:

- Seguridad absoluta.
- Recuperación garantizada en cualquier escenario.
- Soporte ilimitado.
- Sustitución completa de un proveedor IT.
- Cumplimiento legal automático.
- Instalación sin revisar antes el entorno del cliente.

## Proceso comercial

1. Identificar 5 posibles clientes cercanos.
2. Contactar con mensaje simple.
3. Ofrecer revisión inicial gratuita o de bajo coste.
4. Presentar DASC como piloto de pago controlado.
5. Definir alcance por escrito.
6. Instalar solo si el entorno es viable.
7. Validar backup y restauración.
8. Entregar informe inicial.
9. Proponer mantenimiento mensual.
10. Registrar feedback real.

## Criterio de cierre de R-048

R-048 se cerrará si ocurre una de estas dos situaciones:

### Caso A - Éxito

Se consigue un primer cliente de pago.

Debe quedar documentado:

- Tipo de cliente.
- Perfil Lite, PyME o Pro.
- Precio acordado.
- Alcance incluido.
- Fecha de instalación o inicio.
- Primer feedback.
- Riesgos detectados.

### Caso B - No venta, pero aprendizaje válido

No se consigue cliente, pero se obtiene feedback real de posibles clientes.

Debe quedar documentado:

- A quién se contactó.
- Qué objeciones aparecieron.
- Qué precio pareció aceptable o caro.
- Qué parte del producto interesó más.
- Qué habría que cambiar en la oferta.

## Resultado esperado

El resultado ideal de R-048 es conseguir el primer cliente de pago.

El resultado mínimo válido es descubrir si la oferta actual se entiende, si el precio encaja y qué habría que ajustar antes de buscar más clientes.
