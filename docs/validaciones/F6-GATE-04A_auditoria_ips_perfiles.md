# F6-GATE-04A - Auditoría de IPs fijas y perfiles de instalación

## Objetivo

Detectar referencias a IPs fijas dentro del repositorio antes de adaptar instaladores a perfiles e IPs reales.

## Estado

En curso.

## Contexto

Hasta ahora se han validado puertas técnicas usando laboratorio con IPs privadas como:

~~~text
192.168.60.10
192.168.60.20
192.168.60.30
~~~

Esto es válido para pruebas, pero no debe ser una dependencia rígida para instalaciones reales.

## Motivo de la puerta

Antes de modificar instaladores, se necesita saber:

- Qué IPs fijas aparecen en instaladores.
- Qué IPs fijas aparecen en herramientas de producto.
- Qué IPs fijas aparecen solo en documentación.
- Qué valores deben convertirse en variables.
- Qué valores deben preguntarse al instalar.

## Herramienta creada

~~~text
tools/windows/audit_fixed_ips.ps1
~~~

## Informe generado

~~~text
docs/auditoria/auditoria_ips_perfiles.md
~~~

## Criterio

Las IPs en documentación o validaciones históricas pueden quedarse si están contextualizadas.

Las IPs en instaladores, scripts de producto o configuración real deben parametrizarse o justificarse.

## Perfiles objetivo

La adaptación futura debe contemplar como mínimo:

| Perfil | Descripción |
|---|---|
| Lite | Un servidor principal y copia externa obligatoria |
| PyME 2 servidores | API/panel + DB/backups o API/backups + DB |
| Pro 3 servidores | API/panel, DB y backups separados |

## Resultado esperado

La puerta se cerrará cuando exista una auditoría clara y se definan las siguientes acciones de parametrización.

## Conclusión

F6-GATE-04A inicia la transición desde laboratorio con IPs fijas hacia instaladores preparados para entornos reales.
