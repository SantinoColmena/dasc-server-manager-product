# R-051G-FIX1 - Eliminar IPs fijas de laboratorio en defaults API

## Objetivo

Corregir los defaults de laboratorio detectados durante la validación global R-051G.

## Estado

Cerrada.

## Problema detectado

Durante la validación global de instaladores adaptables se detectaron IPs fijas dentro de:

- deploy/api/package/main.py

Valores detectados:

- BACKUPS_HOST con default 192.168.60.30
- SERVICIOS_HOST con default 192.168.60.30
- LOGS_DB_HOST con default 192.168.60.20

Estos valores eran válidos para laboratorio, pero no son adecuados como defaults dentro del paquete de despliegue.

## Solución aplicada

Se sustituyen los defaults fijos de laboratorio por defaults locales neutros:

- BACKUPS_HOST -> 127.0.0.1
- SERVICIOS_HOST -> 127.0.0.1
- LOGS_DB_HOST -> 127.0.0.1

## Motivo

Los instaladores y config.env deben ser los responsables de definir las IPs reales según perfil:

- Lite
- Standard
- Pro
- Custom

El código no debe depender de IPs fijas de laboratorio.

## Criterio de validación

El fix queda validado cuando:

- No aparecen 192.168.60.20, 192.168.60.30 ni 192.168.1.250 en deploy.
- main.py conserva sintaxis Python válida.
- Los instaladores siguen con sintaxis Bash válida.
- El entorno activo no se rompe.
