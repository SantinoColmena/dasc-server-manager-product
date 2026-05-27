# R-052C - Auditoría de exposición de puertos y Nginx

## Objetivo

Auditar la exposición de puertos del entorno lab-pruebas y la configuración Nginx.

## Estado

Cerrada.

## Puertos detectados

Se detectan escuchando en 0.0.0.0:

- 22 SSH
- 80 Nginx central
- 8080 Nginx panel local
- 8000 dasc-api directo
- 8010 central-support directo

## Resultado Nginx

Nginx valida correctamente con:

- nginx -t OK

Sitios activos:

- dasc-central-support
- dasc-api-local

## Observación

El panel local ya funciona por Nginx en 8080.

El panel central ya funciona por Nginx en 80.

## Riesgo

Los puertos internos 8000 y 8010 siguen expuestos en 0.0.0.0.

En un cliente real deberían quedar como backends internos:

- 127.0.0.1:8000
- 127.0.0.1:8010

o quedar filtrados mediante firewall.

## UFW

UFW está inactivo.

## Conclusión

R-052C queda validada.

La configuración Nginx funciona, pero queda pendiente decidir si se limita la escucha de Uvicorn a localhost o si se usa firewall para cerrar puertos internos.
